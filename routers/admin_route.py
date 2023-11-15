from fastapi import APIRouter, Depends, HTTPException, status
from services.user_service import UserService
from database_files.model import User, Log
from sqlalchemy.orm import Session
from routers.user_route import oauth2_scheme
from schemas.user_schema import UpdateAdmin, Reset
import uuid
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
    
#A route to check balance
@admin_router.get("/balance/{account_num}")
async def Check_User_Balance(account_num:int, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
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
    

#EDITING USER INFORMATION BY User ONLY
@admin_router.put("/advance_update/{account_num}")
async def admin_Update_Profile(account_num:int, input:UpdateAdmin, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
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
    
    
#ROUTE TO RESET LOGIN PASSWORD for users admin only
@admin_router.put("/reset_pwd/{account_num}")
async def reset_pwd(account_num:int, input:Reset, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
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

#DELETE MY ACCOUNT Owner ONLY
@admin_router.delete("/delete/{account_num}")
async def Delete_account(account_num:int, db:Session=Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    #authentication
    user =await  UserService.decode_token(db, token)
    
    existing_user = db.query(User).filter(User.account_num==account_num)
    if not existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{account_num} does not exist"
        )
    
    if user.id == 1:
        existing_user.delete()
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
            title = 'Delete Log',
            description = f'Admin deleted {existing_user.first().username } user account'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Account deleted successfully'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admins permission required'
        )
    
    #admin view aLL articles
@admin_router.delete('/delete_all')
async def Delete_all_account(password:str, db:Session=Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    #authentication
    user =await  UserService.decode_token(db, token)
    
    all_user = db.query(User).all()
    
    if not user.id == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= "Admin permission required"
        )
        
    if password == user.password:
        for user in all_user:
            if user.id == 1:
                continue
            db.delete(user)
            db.commit()
        db.close()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = user.account_num,
            reciever_acct_no = "null",
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'Delete Log',
            description = 'User database deleted by administrator'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        return {"message": "All Accounts have been deleted"}
    else: raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail= "INCORRECT PASSWORD"
    )
    