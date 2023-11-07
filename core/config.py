import os
from pathlib import Path

from dotenv import load_dotenv
env_path = Path(".") / "settings.env"
load_dotenv(dotenv_path=env_path)


class Settings:
    #metadata needs
    TITLE = "Ezzy Bank"
    VERSION = "0.0.1"
    CONTACT = {
        'Name': 'Michael Eziefule',
        'Student ID': 'ALT/SOE/022/5063',
        'email': 'mike.eziefule@gmail.com',
        'github': 'https://github.com/mike-eziefule',
        'Location': 'Abuja, Nigeria'
    }
    DESCRIPTION = """ ### OVERVIEW 
#### Welcome to my banking simulation api.

* The fundamental concept is that anyone visiting the blog should be able to:
    * create an account, login and log out at will,
    * read blog posts written by them and/or other user,
    * create, edit and delete blog entries created by them but restricted from modifying or deleting posts from others users.
* perform authentication where a user credentials is verified before they login.
* perform authorization where a user cannot alter the intellectual property of others.
* save registration details and blog posts created at all times.

##### Created in October 2023 for Altschool Africa

    """
    TAGS = [
        {'name': 'Users',
        'description': 'This are the users related routes'
        },
        {'name': 'Transactions',
        'description': 'Transaction history route'
        },
        {'name': 'Admin',
        'description': 'This is the Administrators routes, It was created to help me clear my database during testing'
        }
    ]
    
    SECRET_KEY = "ffec249609fbdbc97f82bfe593d1e45cec19ad2591af315096665512564df9af"
    ALGORITHM = "HS256"
    
setting = Settings()