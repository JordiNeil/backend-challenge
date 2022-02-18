from sqlalchemy.orm import Session

import models, schemas

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.event_id == event_id).first()

def get_events_by_customer(db: Session, customer_id: int):
    return db.query(models.Event).filter(models.Event.customer_id == customer_id).all()

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def create_event(db: Session, event: schemas.EventCreate, customer_id: int):
    db_event = models.Event(
        **event.dict(),
        customer_id=customer_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event

def create_customer(db: Session, customer: schemas.Customer):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer