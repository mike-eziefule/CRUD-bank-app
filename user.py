import app

# class account:
#     def __init__(self, account_holder, phone_number, gender, country):
#         self.account_holder = account_holder
#         self.phone_number = phone_number
#         self.gender = gender
#         self.country = country

#     def deposit(self, amount):
#         self.balance += amount
            
#     def withdraw(self, amount):
        
#         if amount >= self.balance:
#             print("Insufficient funds!!!")
#         else:
#             self.balance -= amount 
            
#     def get_balance(self):
#         print(f" Your Account balance is: {self.balance}")
          
#     def get_account_details(self):
#         print(f"Account Name: {self.account_holder}\nPhone Number: {self.phone_number}\nGender: {self.gender}\nCountry: {self.country}")     
        
# #inheriting from Account class.
# class SavingsAccount(account):
#     def __init__(self, account_holder, phone_number, gender, country, account_number, account_type, balance):
#         super().__init__(account_holder, phone_number, gender, country)
        
#         self.account_number = account_number
#         self.account_type = account_type
#         self.balance = balance
        
#     def get_account_details(self):
#         print(f"Account Name: {self.account_holder}\nPhone Number: {self.phone_number}\nGender: {self.gender}\nCountry: {self.country}\nAccount Number: {self.account_number}\n Account Type: {self.account_type}\nBalance: {self.balance}\nExtra Details: This is an account for students")
#         # return {
#         #     "Account Name": self.account_holder,
#         #     "Phone Number": self.phone_number,
#         #     "Gender": self.gender,
#         #     "Country": self.country,
#         #     "Account Number": self.account_number,
#         #     "Account Type": self.account_type,
#         #     "Balance": self.balance,
#         #     "Extra Details": "This is an account for students"
#         # }  

# class CurrentAccount(account):

#     def __init__(self, account_holder, phone_number, gender, country, account_number, account_type, balance):
#         super().__init__(account_holder, phone_number, gender, country)
        
#         self.account_number = account_number
#         self.account_type = account_type
#         self.balance = balance
    
#     def get_account_details(self):
        
#         print(f"Account Name: {self.account_holder}\nPhone Number: {self.phone_number}\nGender: {self.gender}\nCountry: {self.country}\nAccount Number: {self.account_number}\nAccount Type: {self.account_type}\nBalance: {self.balance}\nExtra Details: This is an account for students")

#         # return {
#         #     "Account Name": self.account_holder,
#         #     "Phone Number": self.phone_number,
#         #     "Gender": self.gender,
#         #     "Country": self.country,
#         #     "Account Number": self.account_number,
#         #     "Account Type": self.account_type,
#         #     "Balance": self.balance,
#         #     "Extra Details": "This is an account for Business"
#         # } 
   
# Michael = SavingsAccount("Michael Eziefule","08069787293", "Male", "Nigeria", "0719784288", "Savings Account", "1000000")
# print(Michael.get_account_details())

print("WELCOME TO MY BANK PROGRAM")

def program_menu():
    
    menu = input("ENTER 1 TO OPEN AN ACCOUNT\nENTER 2 TO OPEN AN WITHDRAW\nENTER 3 TO OPEN AN DEPOSIT\nENTER 4 TO OPEN AN CHECK BALANCE\nENTER 4 FOR ACCOUNT INFORMATION\nENTER 0 TO EXIT\n\nYOUR SELECTION :")
    menu = int(menu)
    
    if menu is 1:
        print("\nWELCOME TO ACCOUNT OPENING PAGE\n")
        app.open_account()
    elif menu == 2:
        app.withdrawal()   
    elif menu == 3:
        app.deposit()   
    elif menu == 4:
        app.balance()
    elif menu == 5:
        app.information()
    elif menu == 0:
        print("\nGOODBYE!!!\n")
        exit()
    else:
        print("INVALID SELECTION")
        
# program that generates random numbers
program_menu()

def user():
    username=str("Username:")
    username = username.capitalize()
    password = str("Password:")
    def verify_password():
        verify = input("Password Again!!!:")
        if verify != password:
            print("Password incorrect, Try again")
            verify_password()
        else:
            return

