import logging

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger()
logger.setLevel(logging.WARNING)



app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/read_event/", response_model=List[schemas.Event])
def read_event(event_id: int=None, customer_id: int = None, db: Session = Depends(get_db)):
    """Retrieve events information, by event id or customer id

    Args:
        event_id (int, optional): Id of the event needed to be retrieved. Defaults to None.
        customer_id (int, optional): Id of the customer for whom the events are to be returned. Defaults to None.
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Raises:
        HTTPException: Event not found
        HTTPException: Event if or customer id is required

    Returns:
        List[Event]: List of events for custormer id or event id
    """
    if event_id is None and customer_id is None:
        raise HTTPException(
            status_code=400, 
            detail="Event id or customer id is required")
    elif event_id is not None:
        db_event =  [crud.get_event(db, event_id=event_id)]
        if db_event is None:
            raise HTTPException(
                status_code=404, 
                detail="Event not found")        
    else:
        db_events = crud.get_events_by_customer(
            db, 
            customer_id=customer_id)

        return db_events
    
        

    return db_event

@app.post("/create_event/", response_model=schemas.Event)
def save_event(request: schemas.RequestCreate, db: Session = Depends(get_db)):    
    """Create an event, if request specify any customer id, the event is going to be added
    to that customer, if don't, create customer with information (first name and last name)     

    Args:
        request (schemas.RequestCreate): Request model that lets specify for required fields 
        db (Session, optional): Database Session for connection . Defaults to Depends(get_db).

    Returns:
        Event: Created event
    """
    db_customer_id = crud.get_customer(
        db, 
        customer_id=request.customer.id)

    if db_customer_id is None:
        customer = schemas.Customer(
            first_name=request.customer.first_name, 
            last_name=request.customer.last_name)
        new_customer = crud.create_customer(db, customer=customer)
        request.customer =  new_customer

    return crud.create_event(
        db=db, 
        event=request.event, 
        customer_id=request.customer.id)      
  
