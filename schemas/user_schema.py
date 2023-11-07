from pydantic import BaseModel, EmailStr
from datetime import date

class User(BaseModel):
    firstname: str
    lastname: str
    username: str
    address: str

class CreateUser(User):
    dob: date
    account_type: str = "Savings Account"
    email: EmailStr
    password: str
    telephone: str
    gender: str

class Update(User):
    pass

class UpdateAdmin(User):
    dob: date
    account_type: str = "Savings Account"
    telephone: str
    gender: str

class SaveAccount(CreateUser):
    account_num: int
    avail_balance: float

class login(BaseModel):
    email: EmailStr
    password: str

class Edit_Pwd(BaseModel):
    new_password: str
    new_password_again: str
    
class Reset(BaseModel):
    new_password: str
    new_password_again: str
    email: EmailStr


class displayable(User):
    account_num: str
    avail_balance: int
    dob: date
    account_type: str
    email: EmailStr