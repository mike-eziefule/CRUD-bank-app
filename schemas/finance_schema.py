from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Log(BaseModel):
    description: str = 'description'
    
class Withdrawal(Log):
    title:str = "Over the counter Withdrawal "
    
class deposit(Log):
    title:str = "Over the counter Cash deposit"
class Transfer(Log):
    title:str = "P2P Transfer"

class ShowBlog(deposit):
    trans_id: UUID
    date_initiated: datetime
    status: str
    
    class Config:
        orm_mode = True