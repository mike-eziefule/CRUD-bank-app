
# username= input(str("Username:"))
# username = username.capitalize()
# password = input(str("Password:"))

def verify_password():
        verify = input("Password Again!!!:")
        if verify != password:
            print("Password incorrect, Try again")
            verify_password()
        else:
            print("Password correct")
            return 
        
verify_password()
