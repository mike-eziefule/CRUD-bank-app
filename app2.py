from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID
import app
import random

app = FastAPI()

class User(BaseModel):
    username: str
    firstname: str
    lastname: str
    Telephone: str
    email: str
    password: str
    gender: str = None
    age: int = None
    location: str= None
    account_type: str = "Saving Account"
    
class createUser(User):
    id: UUID
    account_num: int

database:dict[str, createUser] = {}

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
    return database

@app.get("/Users/{account_num}")
def user(account_num:int):
    user = database.get(account_num)
    if user:
        return user
    return {"message":"user not found"}

@app.post("/Create_users")
def new_User(user_in: User):    
    new_user = createUser(
        id = UUID(int=(len(database)+1)),
        account_num = gen_account_number(),
        **user_in.dict()
    )
    database[new_user.username] = new_user
    
    return new_user    