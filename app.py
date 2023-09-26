# import random

# def gen_account_number():
#     random_numbers = [901]
#     for _ in range(0, 7):
#         x = random.randint(0, 9)
#         random_numbers.append(x)
#     return (''.join(map(str,random_numbers)))

# # gen_account_number()

# #ACCOUNT SELECTOR FINCTIONS
# def account_selector():
#     type = input("CHOOSE AN ACCOUNT TYPE(savings/current): ")
#     type = type.lower()
    
#     if type == "savings":
#         return "savings"
#     elif type == "current":
#         return "current"
#     else: print("\nINVALID INPUT, TRY AGAIN!!!\n")
#     account_selector()



# #ACCOUNT OPENING FUNCTIONS
# def open_account():
#     # print("PLEASE SELECT YOUR ACCOUNT TYPE\n")
#     # account_selector()
#     list_account = {}
    
#     firstname = input("TYPE IN YOUR FIRST NAME:").capitalize()
#     lastname = input("TYPE IN YOUR LAST NAME:").capitalize()
#     def verify_phone():
#         num = input(str("TYPE IN YOUR PHONE NUMBER:"))
#         if len(num) < 11:
#             print("INVALID PHONE NUMBER, TRY AGAIN!!!")
#             verify_phone()
#         return num
#     phone_number = verify_phone()
#     account_number = gen_account_number()
#     account_type = account_selector()
#     locations = input("TYPE IN YOUR LOCATION:")
#     genders = input("TYPE IN YOUR GENDER(Male/Female):")
    
#     print(f"\nYOUR {account_type} ACCOUNT HAS BEEN CREATED, FIND DETAILS BELOW!!!!\n")
#     print(f"Firstname: {firstname}\nLastname: {lastname}\nPhone_number: {phone_number}\nAccount_number:{account_number}\nAccount type: {account_type}")
    
#     file = open("data/Client_database.csv", "a")
#     file.write("")
    
    
#     return {"firstname": firstname, "lastname": lastname, "phone_number": phone_number,"account_number":account_number, "account_type": account_type}

# #withdrawal function   
# def withdrawal():
#     print("WITHDRAWAL PAGE")
#     return

# #deposit function
# def deposit():
#     print("DEPOSIT PAGE")
#     return

# #deposit function
# def deposit():
#     print("WITHDRAWAL PAGE")
#     return
# #deposit function
# def deposit():
#     print("WITHDRAWAL PAGE")
#     return
# #Check balance function
# def balance():
#     print("CHECK BALANCE PAGE")
#     return

# #information function
# def information():
#     print("PROFILE PAGE")
#     return