from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user_schema import CreateUser, Update, displayable, Edit_Pwd
from services.user_service import UserService
from database_files.model import User
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from core.config import setting

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
    
    return {'message':'Account registered successfully!!!',
            'Your Username is':new_user.username,
            'Account number':new_user.account_num,
            'Opening Balance is':new_user.current_balance
        }

#USER LOGIN ROUTE, TOKEN GENERATION ONLY
@user_router.post("/token")
async def create_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(UserService.get_db)):

    auth_user = db.query(User).all()
    
    for row in auth_user:
        if row.email == form_data.username and row.password == form_data.password:
            data = {'sub': form_data.username}
            jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
            return {"access_token": jwt_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="invalid credentials"
        )

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
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Password changed successfully'
        )
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Old Password is incorrect, contact the administrator'
        )


#EDITING USER INFORMATION BY User ONLY
@user_router.put("/update/{password}",)
async def Update_Profile(password:str, input:Update, db:Session = Depends(UserService.get_db), token:str=Depends(oauth2_scheme)):

    #authentication
    user = await UserService.decode_token(db, token)
    
    existing_user = db.query(User).filter(User.id==user.id).first()
    
    if existing_user.password == password:
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
            detail= 'Password is incorrect, contact the administrator'
        )