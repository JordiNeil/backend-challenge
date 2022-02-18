from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    events = relationship("Event", back_populates="owner")


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True)
    description = Column(String)
    event_date = Column(Date)
    event_type = Column(String)
    customer_id =  Column(Integer, ForeignKey('customer.id'))

    owner = relationship("Customer", back_populates="events")
