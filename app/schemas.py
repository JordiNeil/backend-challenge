from datetime import date as date_type
from typing import Optional

from pydantic import BaseModel

class RequestGet(BaseModel):
    event_id : int    

class EventBase(BaseModel):
    description : str
    event_date : date_type = date_type.today().strftime(format="%d-%m-%Y")
    event_type : str

class EventCreate(EventBase):    
    pass

class Event(EventBase):
    event_id : int
    customer_id : int

    class Config:
        orm_mode = True

class Customer(BaseModel):
    id : Optional[int]
    first_name : Optional[str] = ''
    last_name : Optional[str] = ''

class RequestCreate(BaseModel):
    customer : Customer
    event : EventCreate  