import random
from jose import jwt
from fastapi import HTTPException, status
from database_files.engine import sessionLocal
from typing import Generator
from core.config import setting
from database_files.model import User


class UserService:
    
    @staticmethod
    def get_db() -> Generator:
        try:
            db = sessionLocal()
            yield db
        finally:
            db.close()
    
    #function to create 10 digits number where the first 3-digit is can be controlled
    @staticmethod
    def gen_account_number():
        random_numbers = [901]
        for _ in range(7):
            x = random.randint(0, 9)
            random_numbers.append(x)
        return (''.join(map(str,random_numbers)))
    #this block of codes recieves an encoded token(which carries some relevant data like email address of the user),
    # decodes it, then returns the username/email address.
    #Afterwards, it performs some validation with the decoded email against the email address on the database
    
    async def decode_token(db, token):
        try:
            payload = jwt.decode(token, setting.SECRET_KEY, algorithms =[setting.ALGORITHM])
            username:str = payload.get("sub") #"sub" is a field holding the username/email address
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid Email credentials")
            
            #Querry the sub(email) from to token against the stored email
            user = db.query(User).filter(User.email==username).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="User is not authorized")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Unable to verify credentials")
        
        #if successful, return the user as authenticated, for further processing.
        return user
