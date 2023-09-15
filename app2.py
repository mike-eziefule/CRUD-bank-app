from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID
import app
import random

app = FastAPI()

class User(BaseModel):
    
    firstname: str
    lastname: str
    Telephone: str
    email: str
    password: str
    gender: str = None
    age: int = None
    Address: str= None
    account_type: str = "Saving Account"
    
class createUser(User):
    id: UUID
    account_num: int
    username: str
    
# class Database(BaseModel):
#     database:list[createUser]
    
SavingsDB:dict[str, createUser] = {} # dictionary to store saving accounts
CurrentDB:dict[str, createUser] = {} # dictionary to store current
database:dict[str, createUser] = {} # dictionary to store

def gen_account_number():
    random_numbers = [901]
    for _ in range(0, 7):
        x = random.randint(0, 9)
        random_numbers.append(x)
    return (''.join(map(str,random_numbers)))

@app.get("/")
def home():
    return "welcome page"

@app.get("/Users")
def all_users():
    if database == {}:
        return {"message":"List is empty"}
    return database

@app.get("/Users/{account_num}")
def get_Account_info(account_num):
    user = database.get(int(account_num))

    if not user:
        return {"message":"user not found"}
    
    return user

@app.post("/Create_users")
def new_User(user_in: User):
    new_user = createUser(
        id = UUID(int=(len(database)+1)),
        username = user_in.firstname.capitalize()+'.'+user_in.lastname[0].upper(), #generate a user name from First and Last names
        account_num = gen_account_number(), #generates a unique account number starting with 901
        **user_in.dict()
    )
    database[new_user.account_num] = new_user
    
    if new_user.account_type == "Savings Account":
        SavingsDB[new_user.account_num] = new_user
        return {"message": "Saved in Savings Account DB",
            "account Information": new_user}
    elif new_user.account_type == "Current Account":
        CurrentDB[new_user.account_num] = new_user
        return {"message": "Saved in Current Account DB",
        "account Information": new_user}
    else:
        return "Account type not found"