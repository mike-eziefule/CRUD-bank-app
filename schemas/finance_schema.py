from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Log(BaseModel):
    description: str = 'Over the counter cash withdrawal'
    
class Withdrawal(Log):
    title:str = "Withdrawal"
    
class deposit(Log):
    title:str = "Cash deposit"

class ShowBlog(deposit):
    trans_id: UUID
    date_initiated: datetime
    status: str
    
    class Config:
        orm_mode = True