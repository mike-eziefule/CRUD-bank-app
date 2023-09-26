from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID
import random, json

app = FastAPI()

class User(BaseModel):
    account_type: str = "Savings Account"
    firstname: str
    lastname: str
    Telephone: str
    email: str
    gender: str
    age: int
    Address: str
    
class UserEdit(BaseModel):
    firstname: str
    lastname: str
    Telephone: str
    gender: str
    age: int
    Address: str
class login(User):
    username: str
    password: str
    password_auth: str = None

class Edit_Pwd(BaseModel):
    username: str
    password: str
    password_auth: str = None

class createUser(login):
    id: UUID
    account_num: str
    account_balance: float = 0.0

database: dict[str, createUser] = {}
# myjson = database.json()

# filename = 'data/database.json'

# def save_to_database(database):
#     with open(filename, 'a') as file:
#         json.dump(myjson, file, indent=4)
#         pass
        
# def read_from_database():
#     with open(myjson, 'r') as file:
#         data = json.load(file)
#         return data

#function to create 10 digits number where the first 3-digit is can be controlled
def gen_account_number():
    random_numbers = [901]
    for _ in range(7):
        x = random.randint(0, 9)
        random_numbers.append(x)
    return (''.join(map(str,random_numbers)))

#function to check if account number exists in database
def check_account_number(account_num:str,):
    target = database.get(account_num)
    if not target:
        return False
    return True

@app.get("/")
def home():
    return "welcome to Ezzi Bank"

@app.get("/users/all")
def get_all_users():
    if database == {}:
        return {"message":"Database is empty"}
    return database

@app.post("/users/signup/")
async def Sign_up(user_in: login):
    
    #generate unique user_id and Account number for the customer
    new_user = createUser(
        id = UUID(int=(len(database)+1)),
        account_num = gen_account_number(),
        account_balance = 0.0, #generates a unique account number starting with 901
        **user_in.dict()
    )
    #authenticate password
    if user_in.password != user_in.password_auth:
        return {'error':'password does not match'}
    
    #checks if the generated account number exists
    if check_account_number(str(new_user.account_num)) == True:
        return {'error':'account number has been taken, Try again'}
    
    #save new user information in database and hashed under account number
    database[new_user.account_num] = new_user
    # save_to_database(database)
    
    return {"message": "Saved in database DB successfully", "Data" : new_user}

#A route to find customer information with customer account number
@app.get("/users/signin/{account_num}")
def Get_User_profile(account_num:str, password_in:str):
    target = database.get(str(account_num))
    if not target:
        return {"message":"user not found", "data":target}
    #check if user password is correct
    if target.password != password_in:
        return {"message":"password incorrect, Try again"}
    
    return {"Welcome": target.username,
            "data": target}

#A route to find customer information with customer account number
@app.get("/users/signin/balance/{account_num}")
def Check_Balance(account_num:str, password_in:str):
    target = database.get(str(account_num))
    if not target:
        return {"message":"user not found", "data":target}
    
    #check if user password is correct
    if target.password != password_in:
        return {"message":"password incorrect, Try again"}
    
    return {"Welcome": target.username,
            "Your Account Balance is": "NGN {:,.2f}".format(target.account_balance) }

#route to edit some allowed details in customers profile
@app.put("/users/signin/update/{account_num}")
def Update_profile(account_num:str, data_in:UserEdit):
    target = database.get(str(account_num))
    if not target:
        return {"message":"user not found", "data": "null"}
    
    target.firstname = data_in.firstname
    target.lastname = data_in.lastname
    target.Telephone = data_in.Telephone
    target.gender = data_in.gender
    target.age = data_in.age
    target.Address = data_in.Address
    
    return {"Message": "Profile updated Successfully!!!",
        "data" : target}

#route to update password
@app.put("/users/profile/ChangePassword/{account_num}")
def change_password(account_num:str, data_in:Edit_Pwd):
    target = database.get(str(account_num))
    if not target:
        return {"message":"user not found", "data": "Try Again"}
    
    if data_in.password != data_in.password_auth:
        return {'error':'password does not match'}
    
    target.username = data_in.username
    target.password = data_in.password
    target.password_auth = data_in.password_auth
    
    return {'success':"Username and Password updated successfully!!!"}

#route to delete a user from the database
@app.delete("/users/profile/delete/{account_num}")
def delete_User(account_num:str, password_in):
    target = database.get(str(account_num))
    if not target:
        return {"message": "User not found"}
    
    #check if user password is correct
    if target.password != password_in:
        return {"message":"password incorrect, Try again"}
    
    del database[target.accounts_num]
    
    return {"message": "User Deleted Successfully!!!"}

@app.put("/user/deposit/{account_num}")
def Deposit(account_num: str, amount: float):
    target = database.get(str(account_num))
    if not target:
        return {"message": "Enter a correct Account Number"}
    target.account_balance += amount
    return {"message": "Your Deposit of  was successfully", 
            "Amount deposited": amount, 
            "Available Balance is": "NGN {:,.2f}".format(target.account_balance)
            }
    
@app.put("/user/signin/withdrawal/{account_num}")
def Withdrawal(account_num:str, password_in:str, amount: float):
    target = database.get(str(account_num)) #Call the existing database

    if not target:
        return {"message": "Enter a correct Account Number"}
    if target.password != password_in:
        return {"message":"password incorrect, Try again"}
    if target.account_balance < amount:
        return {"message": "Insufficient funds!!!"}
    if amount <= 5000:
        charges = 10.75
    elif amount > 5000 and amount <= 50000:
        charges = 26.88
    else: charges = 53.75

    deductables = amount + charges
    if target.account_balance < deductables:
        return {"message": "Insufficient funds!",
                "error": "Bank charges may apply"}
    target.account_balance -= deductables
    newbalance = "NGN {:,.2f}".format(target.account_balance)
    return {"message": "Withdrawal of  was successfully", 
            "Amount Withdrawn": amount,
            "Bank Charges" : charges,
            "Available Balance is": newbalance
            }
@app.put("/users/signin/transfer")
def transfer(sender_account:str, recipient_account:str, password_in:str, amount:float):
    sender = database.get(str(sender_account))
    recipient = database.get(str(recipient_account))
    
    if not sender:
        return {"message":"Enter a correct Account Number and Password"}
    if not recipient:
        return {"message":"Enter a correct Account Number and Password"}
    if sender.password != password_in:
        return {"message":"password incorrect, Try again"}
    
    #add bank charges to transaction
    if amount <= 5000:
        charges = 10.75
    elif amount > 5000 and amount <= 50000:
        charges = 26.88
    else: charges = 53.75
    #calculate total deductable
    payable = amount + float(charges)
    
    if sender.account_balance < payable:
        return {"message": "Insufficient funds!!!"}
    
    #Debit Action
    sender.account_balance -= payable
    #Action Credit
    recipient.account_balance += amount
    
    return {"message": "Transaction Successful!!!",
            "sender": sender.username,
            "recipient": recipient.username,
            "amount": "NGN {:,.2f}".format(amount),
            "Bank Deduction": "NGN {:,.2f}".format(charges),
            "Available balance is": "NGN {:,.2f}".format(sender.account_balance)
            }