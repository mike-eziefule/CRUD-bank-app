from fastapi import APIRouter, Depends, HTTPException, status
# from schemas.user_schema import CreateUser, displayable
from schemas.finance_schema import deposit, Withdrawal
from services.user_service import UserService
from database_files.model import Log, User
from sqlalchemy.orm import Session
from routers.user_route import oauth2_scheme
from sqlalchemy import func

from uuid import UUID
from datetime import datetime

finance_router = APIRouter()

@finance_router.get("/")
def get_log():
    return "logs"

#A route to check balance by logged in users ONLY
@finance_router.get("/balance")
async def Check_Balance(db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    user = await UserService.decode_token(db, token)
    
    existing_user = db.query(User).filter(User.account_num == user.account_num)
    
    if existing_user.first():
        
        return { "Welcome ": user.username,
                "Your Account Balance is": " NGN {:,.2f}".format(existing_user.first().current_balance) 
                }
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="ACCOUNT NOT FOUND"
        )

#over the counter deposit, admin only
@finance_router.put("/Cash_deposit/{amount}")
async def Cash_Deposit(amount:float, reciever_acct_no:int, input:deposit, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    user = await UserService.decode_token(db, token)
    
    #verify admin status
    if user.id is not 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin permission required'
        )
    #verify reciepient account
    recipient_user = db.query(User).filter(User.account_num == reciever_acct_no)
    if not recipient_user.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'RECIEPIENT ACCOUNT NOT FOUND'
        )
    
    sending_acct = db.query(User).filter(User.id == 1)
    if sending_acct.first().current_balance < amount:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'INSUFFICIENT FUNDS'
        )  
    else:
        sending_acct.update({User.current_balance : User.current_balance - amount})                                      #Alternatively
        db.commit()
    
    if recipient_user.first().status != "ACTIVE":
        #initiate reversal
        sending_acct.update({User.current_balance : User.current_balance + amount})                                      #Alternatively
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'RECIPIENT INACTIVE'
        )
    else:
        recipient_user.update({User.current_balance : User.current_balance + amount})                                      #Alternatively
        db.commit()

    
    # new_log = Log(trans_id = UUID(int(length + 1)),
    #                 date_initiated = datetime.now(),
    #                 amount = amount,
    #                 sender = user.username,
    #                 owner_id = user.id,
    #                 **input.__dict__
    # )
    
    # # save to database
    # db.add(new_log)
    # db.commit()
    # db.refresh(new_log)
    
        return {'message':'Deposit successful!!!',
                'Amount Deposited:':" NGN {:,.2f}".format(amount),
                'recipient Account:':recipient_user.first().account_num,
                'recipient Name:':recipient_user.first().firstname + ' ' + recipient_user.first().lastname
    }

#over the counter withdrawal, admin only
@finance_router.put("/Withdrawal/{amount}")
async def Cash_Withdrawal(amount:float, sender_acct_no:str, input:Withdrawal, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    user = await UserService.decode_token(db, token)
    
    #verify admin status
    if user.id is not 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin permission required'
        )
    #verify reciepient account is admin and active
    recipient_user = db.query(User).filter(User.id == 1)
    if not recipient_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  
            detail= 'RECIEPIENT ACCOUNT NOT FOUND'
        )
    
    #verify sender/deductable account has enough money
    sending_acct = db.query(User).filter(User.account_num == sender_acct_no)
    if sending_acct.first().current_balance < amount:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'INSUFFICIENT FUNDS'
        )  
    else: #deduct sending account
        sending_acct.update({User.current_balance : User.current_balance - amount})                                      #Alternatively
        db.commit()
    
    #verify recipient_user is active
    if recipient_user.first().status != "ACTIVE":
        sending_acct.update({User.current_balance : User.current_balance + amount})                                      #Alternatively
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'RECIPIENT ACCOUNT IS INACTIVE'
        )
    else:
        recipient_user.update({User.current_balance : User.current_balance + amount})                                      #Alternatively
        db.commit()
    
        return {'message':'Withdrawal successful!!!',
                'Amount Withdrawn:':" NGN {:,.2f}".format(amount),
                'Customer Account:':sending_acct.first().account_num,
                'Customer Name:':sending_acct.first().firstname + ' ' + sending_acct.first().lastname
        }





#intrabank Transfer, users only
@finance_router.put("/transfer/{amount}")
async def Transfer(amount:float, reciever_acct_no:int, password:str, input:Withdrawal, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    user = await UserService.decode_token(db, token)
    
    #verify and set sending accont
    sending_acct = db.query(User).filter(User.id == user.id)
    #verify and set reciever account
    recipient_user = db.query(User).filter(User.account_num == reciever_acct_no)

    #verify if entered password is correct
    if password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  
            detail= 'PASSWORD IS INCORRECT'
        )
    
    #verify if sending account is active
    if sending_acct.first().status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  
            detail= 'YOUR ACCOUNT HAS BEEN DISABLED'
        )
    
    #verify sender/deductable account has enough money
    if sending_acct.first().current_balance < amount:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'INSUFFICIENT FUNDS!!!'
        )
    else:   #deduct sending account
        sending_acct.update({User.current_balance : User.current_balance - amount})                                    #Alternatively
        db.commit()
    
    #verify reciepients account number
    if not recipient_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  
            detail= 'ACCOUNT NUMBER IS INCORRECT'
        )
    
    #verify recipient_user is active
    if recipient_user.first().status != "ACTIVE":
        #initiate reversal
        sending_acct.update({User.current_balance : User.current_balance + amount})                                      #Alternatively
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'RECIPIENT ACCOUNT IS INACTIVE'
        )
    else:
        #credit reciepient
        recipient_user.update({User.current_balance : User.current_balance + amount})                                      #Alternatively
        db.commit()
        return {'message':'Transfer successful!!!',
                'Amount Withdrawn:':" NGN {:,.2f}".format(amount),
                'Receiving Account:':recipient_user.first().account_num,
                'Receivers Name:':recipient_user.first().firstname + ' ' + recipient_user.first().lastname
        }


# @app.put("/users/signin/transfer")
# def transfer(sender_account:str, recipient_account:str, password_in:str, amount:float):
#     sender = database.get(str(sender_account))
#     recipient = database.get(str(recipient_account))
    
#     if not sender:
#         return {"message":"Enter a correct Account Number and Password"}
#     if not recipient:
#         return {"message":"Enter a correct Account Number and Password"}
#     if sender.password != password_in:
#         return {"message":"password incorrect, Try again"}
    
#     #add bank charges to transaction
#     if amount <= 5000:
#         charges = 10.75
#     elif amount > 5000 and amount <= 50000:
#         charges = 26.88
#     else: charges = 53.75
#     #calculate total deductable
#     payable = amount + float(charges)
    
#     if sender.account_balance < payable:
#         return {"message": "Insufficient funds!!!"}
    
#     #Debit Action
#     sender.account_balance -= payable
#     #Action Credit
#     recipient.account_balance += amount
    
#     return {"message": "Transaction Successful!!!",
#             "sender": sender.username,
#             "recipient": recipient.username,
#             "amount": "NGN {:,.2f}".format(amount),
#             "Bank Deduction": "NGN {:,.2f}".format(charges),
#             "Available balance is": "NGN {:,.2f}".format(sender.account_balance)
#             }