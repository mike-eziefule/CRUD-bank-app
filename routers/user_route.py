from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user_schema import CreateUser, Update, Edit_Pwd
from services.user_service import UserService
from database_files.model import User, Log
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from core.config import setting
import uuid
from datetime import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

user_router = APIRouter()

#USER REGISTRATION ROUTE
@user_router.post("/register")
async def Sign_up(user_in:CreateUser, db:Session=Depends(UserService.get_db)):
    
    #generate unique user_id and Account number for the customer
    new_user = User(
        account_num = UserService.gen_account_number(),
        current_balance = 0.0, #generates a unique account number starting with 901
        **user_in.dict()
    )
    
    rollcall = db.query(User).all()
    for row in rollcall:
        if row.email == new_user.email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="EMAIL already in use")
        if row.username == new_user.username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="USERNAME already in use, Try another nickname")
        
        if row.account_num == new_user.account_num:
            new_user = User(
                account_num = UserService.gen_account_number(),
                current_balance = 0.0, #generates a unique account number starting with 901
                **user_in.dict()
            )
            
    # save_to_database(database)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # save Log database
    new_log = Log(
        trans_id = uuid.uuid4(),
        date_initiated = datetime.now(),
        amount = 0,
        sender_acct_no = new_user.account_num,
        reciever_acct_no = 'not applicable',
        owner_id = new_user.id,
        status = "SUCCESSFUL",
        title = 'Registration',
        description = 'New user registrated'
    )  
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    return {'message':'Account registered successfully!!!',
            'Your User ID is':new_user.id,
            'Your Username is':new_user.username,
            'Account email':new_user.email,
            'Account number':new_user.account_num,
            'Account Type':new_user.account_type,
            'Opening Balance is':new_user.current_balance
        }

#USER LOGIN ROUTE, TOKEN GENERATION ONLY
@user_router.post("/token")
async def Login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(UserService.get_db)):

    auth_user = db.query(User).all()
    
    for row in auth_user:
        if row.email == form_data.username and row.password == form_data.password:
            data = {'sub': form_data.username}
            jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
            return {"access_token": jwt_token, "token_type": "bearer"}
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = row.account_num,
            reciever_acct_no = 'not applicable',
            owner_id = row.id,
            status = "SUCCESSFUL",
            title = 'Login',
            description = 'User logged in successfully'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="invalid credentials"
        )


#transaction history
@user_router.get("/trans_history",)
async def trans_history(db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = await UserService.decode_token(db, token)
    
    existing_user = db.query(Log).filter(Log.owner_id==user.id)
    if not existing_user.all():
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail= 'No transaction history found'
        )
        
    # save Log database
    new_log = Log(
        trans_id = uuid.uuid4(),
        date_initiated = datetime.now(),
        amount = 0,
        sender_acct_no = 'not applicable',
        reciever_acct_no = 'not applicable',
        owner_id = user.id,
        status = "SUCCESSFUL",
        title = 'History',
        description = 'User viewed transaction history'
    )  
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    return existing_user.all()

#ROUTE TO CHANGE PASSWORD for logged in users
@user_router.put("/change_pwd/{password}")
async def Change_pwd(password:str, input:Edit_Pwd, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):
    
    user = await UserService.decode_token(db, token)
    
    existing_user = db.query(User).filter(User.id==user.id)

    if input.new_password != input.new_password_again:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="New password is does not match"
        )
    #authentication 
    if existing_user.first().password == password:
        
        existing_user.update({User.password : input.new_password})                                       #Alternatively
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = existing_user.first().account_num,
            reciever_acct_no = 'not applicable',
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'Update',
            description = 'User changed password'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Password changed successfully'
        )
        
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Old Password is incorrect, contact the administrator'
        )


#EDITING USER INFORMATION BY User ONLY
@user_router.put("/update/profile",)
async def Update_Profile(password:str, input:Update, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = await UserService.decode_token(db, token)
    
    existing_user = db.query(User).filter(User.id==user.id)
    
    if existing_user.first().password == password:
        # db update reqires a dict input but input:Update is a pydantic model hence the use of jsonable encoder to convert it
        # existing_article = existing_user.update(jsonable_encoder(input))  
        existing_user.update(input.__dict__)     #Alternatively
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = existing_user.first().account_num,
            reciever_acct_no = 'not applicable',
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'Update',
            description = 'User updated profile information'
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
            detail= 'Password is incorrect, contact the administrator'
        )
    

#Disable/freeze an account 
@user_router.put("/freeze/",)
async def disable_account(password:str, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = await UserService.decode_token(db, token)
    
    existing_user = db.query(User).filter(User.id==user.id)
    
    if existing_user.first().password == password:
        existing_user.update({User.status: "FREEZE"})     #Alternatively
        db.commit()
        
        # save Log database
        new_log = Log(
            trans_id = uuid.uuid4(),
            date_initiated = datetime.now(),
            amount = 0,
            sender_acct_no = existing_user.first().account_num,
            reciever_acct_no = 'not applicable',
            owner_id = user.id,
            status = "SUCCESSFUL",
            title = 'BLOCKED',
            description = 'User froze an account'
        )  
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Account successfully disabled, contact admin to enable it again'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Password is incorrect, try again'
        )
