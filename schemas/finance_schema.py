from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Log(BaseModel):
    description: str = None
    
class Withdrawal(Log):
    title:str = "Cash withdrawal"
    
class deposit(Log):
    title:str = "Cash deposit"

class ShowBlog(deposit):
    trans_id: UUID
    date_initiated: datetime
    status: str
    
    class Config:
        orm_mode = True