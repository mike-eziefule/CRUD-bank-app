from fastapi import APIRouter, Depends, HTTPException, status
from services.user_service import UserService
from database_files.model import User
from sqlalchemy.orm import Session
from routers.user_route import oauth2_scheme
from schemas.user_schema import UpdateAdmin, Reset

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
        # db update reqires a dict input but input:BlogCreate is a pydantic model hence the use of jsonable encoder to convert it
        # existing_article = existing_article.update(jsonable_encoder(input))  
        existing_user.update(input.__dict__)                    #Alternatively
        db.commit()
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
        
    if db.query(User).filter(User.email == input.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email already in use"
        )
    
    #authentication 
    if user.id == 1:
        
        existing_user.update(input.__dict__)                                       #Alternatively
        db.commit()
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
        # db update reqires a dict input but input:BlogCreate is a pydantic model hence the use of jsonable encoder to convert it
        # existing_article = existing_article.update(jsonable_encoder(input))  
        existing_user.delete()                   #Alternatively
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Account deleted successfully'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Admins permission required'
        )