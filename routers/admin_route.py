from fastapi import APIRouter, Depends, HTTPException, status
from services.user_service import UserService
from database_files.model import User, Log
from sqlalchemy.orm import Session
from routers.user_route import oauth2_scheme
from schemas.user_schema import UpdateAdmin, Reset
from schemas.finance_schema import deposit, Withdrawal
import uuid
from uuid import UUID
from datetime import datetime

admin_router = APIRouter()

#view aLL USERS, admin ONLY
@admin_router.get('/user_inventory')
async def user_list(db:Session=Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    user = await UserService.decode_token(db, token)
    
    all_Users = db.query(User).all()

    if not all_Users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="List is empty"
        )
    
    if  user.id == 1:
        return all_Users
    
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin permission required'
        )
    
#find transaction by uuid (3709dab9-159a-44dd-9683-c4d6f89b6b5e), admin ONLY
@admin_router.get('/history/{trans_id}')
async def find_transaction(trans_id:UUID, db:Session=Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    user = await UserService.decode_token(db, token)
    
    query_log = db.query(Log).filter(Log.trans_id == trans_id)
    
    if not query_log.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="transaction not found"
        )
    
    if  user.id == 1:
        return query_log.all()
    
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin permission required'
        )
    
#A route to check user balance
@admin_router.get("/balance/{account_num}")
async def Check_User_Balance(account_num:str, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    user = await UserService.decode_token(db, token)
    
    existing_user = db.query(User).filter(User.account_num == account_num)
    
    if not existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="ACCOUNT NOT FOUND"
        )
    
    if  user.id == 1:
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = user.account_num,
            reciever_acct_no = existing_user.first().account_num,
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'Enquiry',
            description = 'Admin checked account balance'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        
        return { "Account Holder": existing_user.first().firstname + " " + existing_user.first().lastname,
                "Your Account Balance is": " NGN {:,.2f}".format(existing_user.first().current_balance) 
                }
        
    
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin permission required'
        )



#Capital deposit, admin only
@admin_router.put("/capital/{amount}")
async def credit_admin(amount:float, password:str, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    user = await UserService.decode_token(db, token)
    verify_admin = db.query(User).filter(User.id == user.id)

    #verify admin status
    if user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin permission required'
        )
    
    #verify admin passworf
    if verify_admin.first().password != password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin password incorrect'
        )
        
    verify_admin.update({User.current_balance : User.current_balance + amount})
    db.commit()
    
            
    # save Log database
    new_log = Log(
        trans_id = uuid.uuid4(),
        date_initiated = datetime.now(),
        amount = amount,
        sender_acct_no = "CENTRAL BANK OF NIGERIA",
        reciever_acct_no = verify_admin.first().account_num,
        owner_id = user.id,
        status = "SUCCESSFUL",
        title = "Capital",
        description = "Branch kick of capital"
    )  
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    return {'message':'Deposit successful!!!',
            'Amount Deposited:':" NGN {:,.2f}".format(amount),
            'recipient Account:':verify_admin.first().account_num,
            'recipient Name:':verify_admin.first().firstname + ' ' + verify_admin.first().lastname
        }





#over the counter deposit, admin only
@admin_router.put("/Cash_deposit/{amount}")
async def Cash_Deposit(amount:float, reciever_acct_no:str, input:deposit, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    user = await UserService.decode_token(db, token)
    
    #verify admin status
    if user.id != 1:
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
        sending_acct.update({User.current_balance : User.current_balance - amount})
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
            
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = amount,
            sender_acct_no = sending_acct.first().account_num,
            reciever_acct_no = recipient_user.first().account_num,
            owner_id = user.id,
            status = "SUCCESSFUL",
            **input.__dict__
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
    
        return {'message':'Deposit successful!!!',
                'Amount Deposited:':" NGN {:,.2f}".format(amount),
                'recipient Account:':recipient_user.first().account_num,
                'recipient Name:':recipient_user.first().firstname + ' ' + recipient_user.first().lastname
        }

#over the counter withdrawal, admin only
@admin_router.put("/Withdrawal/{amount}")
async def Cash_Withdrawal(amount:float, sender_acct_no:str, input:Withdrawal, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    user = await UserService.decode_token(db, token)
    
    #verify admin status
    if user.id != 1:
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
        sending_acct.update({User.current_balance : User.current_balance - amount}) 
        db.commit()
    
    #verify recipient_user is active
    if recipient_user.first().status != "ACTIVE":
        sending_acct.update({User.current_balance : User.current_balance + amount})                                    
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'RECIPIENT ACCOUNT IS INACTIVE'
        )
    else:
        recipient_user.update({User.current_balance : User.current_balance + amount})                                      
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = amount,
            sender_acct_no = sending_acct.first().account_num,
            reciever_acct_no = recipient_user.first().account_num,
            owner_id = user.id,
            status = "SUCCESSFUL",
            **input.__dict__
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
    
        return {'message':'Withdrawal successful!!!',
                'Amount Withdrawn:':" NGN {:,.2f}".format(amount),
                'Customer Account:':sending_acct.first().account_num,
                'Customer Name:':sending_acct.first().firstname + ' ' + sending_acct.first().lastname
        }



#EDITING USER INFORMATION BY administrator
@admin_router.put("/advance_update/{account_num}")
async def admin_Update_Profile(account_num:str, input:UpdateAdmin, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    #authentication
    user = await UserService.decode_token(db, token)
    
    existing_user = db.query(User).filter(User.account_num==account_num)
    if not existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with:{account_num} not found"
        )
    
    if  user.id == 1:
        existing_user.update(input.__dict__)                    #Alternatively
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = user.account_num,
            reciever_acct_no = existing_user.first().account_num,
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'Update Log',
            description = f'Admin edited user{existing_user.first().username } [profile information'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Information updated successfully'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin permission required'
        )
    
    
#ROUTE TO RESET USER LOGIN PASSWORD BY admin only
@admin_router.put("/reset_password/{account_num}")
async def reset_password(account_num:str, input:Reset, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    user = await UserService.decode_token(db, token)

    existing_user = db.query(User).filter(User.account_num==account_num)
    if not existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="ACCOUNT NOT FOUND"
        )

    if input.new_password != input.new_password_again:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="New password is does not match"
        ) 
    if user.id == 1:
        
        existing_user.update(input.__dict__)                                       #Alternatively
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = user.account_num,
            reciever_acct_no = existing_user.first().account_num,
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'Edit Log',
            description = f'Password of{existing_user.first().username } resetted by Administrator'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Information updated successfully'
        )
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admin permission required'
        )
    
#Admin Disable/freeze an account 
@admin_router.put("/freeze/")
async def freeze_account(password:str, account_num:str, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = await UserService.decode_token(db, token)
    
    admin_user = db.query(User).filter(User.id== 1)
    complainer = db.query(User).filter(User.account_num == account_num)

    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Admin permission required"
        )
    
    if admin_user.first().password == password:
    
        complainer.update({User.status: "FREEZE"})     #Alternatively
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = 'not applicable',
            reciever_acct_no = complainer.first().account_num,
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'BLOCKED',
            description = f'Admin froze {complainer.first().username} account'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Account successfully Disabled'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Password is incorrect, try again'
        )
    
    
# admin Enable/unfreeze an account 
@admin_router.put("/unfreeze/")
async def unfreeze_account(password:str, account_num:str, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = await UserService.decode_token(db, token)
    
    admin_user = db.query(User).filter(User.id== 1)
    complainer = db.query(User).filter(User.account_num == account_num)

    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Admin permission required"
        )
    
    if admin_user.first().password == password:
    
        complainer.update({User.status: "ACTIVE"})     #Alternatively
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = 'not applicable',
            reciever_acct_no = complainer.first().account_num,
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'UNBLOCKED',
            description = f'Admin unfroze {complainer.first().username} account'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Account successfully enabled'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Password is incorrect, try again'
    )


#admin delete specific users
@admin_router.delete("/delete/{account_num}")
async def Delete_account(account_num:str, admin_password:str, db:Session=Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    #authentication
    user = await UserService.decode_token(db, token)
    
    querry_admin = db.query(User).filter(User.id == user.id)
    querry_user = db.query(User).filter(User.account_num == account_num)
    
    if not querry_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{account_num} does not exist"
        )
        
    if user.password != admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Admin Password incorrect"
        )
    
    if user.id == 1:
        #return balance to admin account
        querry_admin.update({User.current_balance : User.current_balance + querry_user.first().current_balance}) 
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = querry_user.first().current_balance,
            sender_acct_no = querry_user.first().account_num,
            reciever_acct_no = querry_admin.first().account_num,
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'Delete Log',
            description = f'Admin deleted {querry_user.first().username } user account'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        #perform delete operation
        querry_user.delete()
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Account deleted successfully'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admins permission required'
        )

#admin delete all users except admin account
@admin_router.delete('/delete_users')
async def Delete_users(admin_password:str, db:Session=Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    #authentication
    user =await  UserService.decode_token(db, token)
    
    if user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Admin permission required"
        )
    
    all_user = db.query(User).all()
    admin = db.query(User).filter(User.id == user.id)
        
    if admin_password == admin.first().password:
        
        for row in all_user:
            if row.id == 1:
                continue
            
            #return balance to admin account
            admin.update({User.current_balance : User.current_balance + row.current_balance}) 
            db.commit()
            
            #save Log database
            new_log = Log(
                trans_id = uuid.uuid4(),
                date_initiated = datetime.now(),
                amount = 0,
                sender_acct_no = 'not applicable',
                reciever_acct_no = "not applicable",
                owner_id = user.id,
                status = "SUCCESSFUL",
                title = 'Delete USER',
                description = 'User database CLEARED by administrator'
            )
            db.add(new_log)
            db.commit()
            db.refresh(new_log)
            
            
            #perform delete operation
            db.delete(row)
            db.commit()
        db.close()
        
        
        
        return {"message": "All Accounts have been deleted"}
    else: raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail= "INCORRECT PASSWORD"
    )
    
#admin delete log data
@admin_router.delete('/delete_log')
async def Delete_transaction_Log(password:str, db:Session=Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    #authentication
    user = await  UserService.decode_token(db, token)
    
    all_log = db.query(Log).all()
    
    if not user.id == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Admin permission required"
        )
    
    print(user.password)
    
    if password == user.password:
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = "not applicable",
            reciever_acct_no = "not applicable",
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'Delete Log',
            description = 'Log entries cleared by administrator'
        )
        
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        for entry in all_log:
            db.delete(entry)
            db.commit()
        db.close()
        
        return {"message": "All Log history have been deleted"}
    
    else: raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail= "INCORRECT PASSWORD"
    )
