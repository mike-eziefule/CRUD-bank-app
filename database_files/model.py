from database_files.engine import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, DateTime, Uuid
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'USER'
    
    id = Column(Integer, primary_key=True, index = True)
    firstname = Column(String, nullable= False)
    lastname = Column(String, nullable= False)
    username = Column(String, unique=True, nullable= False)
    address = Column(String(120), nullable= False)
    dob = Column(Date, nullable= False)
    account_type = Column(String, nullable= False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable= False)
    telephone = Column(String, nullable= False)
    gender = Column(String, nullable= False)
    account_num = Column(String, unique=True, nullable= False)
    current_balance = Column(Float, nullable= False)
    status = Column(String, default= "ACTIVE")
    
    transactions = relationship("Log", back_populates = "owner")


class Log(Base):
    __tablename__ = 'LOG'
    
    id = Column(Integer, primary_key=True, index = True)
    status = Column(String, default= "SUCCESS")
    trans_id= Column(Uuid, unique= True, nullable= False)
    date_initiated = Column(DateTime, nullable= False)
    title = Column(String, nullable= False)
    description = Column(String(120), nullable= False)
    sender_acct_no = Column(String, nullable= False)
    reciever_acct_no = Column(String, nullable= False)
    amount = Column(Float, nullable= False)
    
    owner_id = Column(Integer, ForeignKey("USER.id"))
    owner = relationship("User", back_populates = "transactions")
