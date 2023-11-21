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

*Ezzy Bank is a cutting-edge fintech API, crafted with precision using FastAPI and Python. Empowering seamless financial transactions, secure data handling, and rapid integration. Our API is designed to elivate your fintech solutions to new heights. Experiencing efficiency and reliability at its core as you embark on a finincial journey of unparalleled financial innovation with our robust FASTAPI-powered platform...
<a href="https://github.com/mike-eziefule/CRUD-bank-app#readme" target="_blank">Read more</a>*


##### Created in November 2023

    """
    TAGS = [
        {'name': 'Users',
        'description': 'This are the users related routes'
        },
        {'name': 'Transactions',
        'description': 'Transaction history route'
        },
        {'name': 'Admin',
        'description': 'This is the Administrators routes, The first user to login becomes the admin'
        }
    ]
    
    SECRET_KEY = "ffec249609fbdbc97f82bfe593d1e45cec19ad2591af315096665512564df9af"
    ALGORITHM = "HS256"
    
setting = Settings()