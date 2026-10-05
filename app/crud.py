from datetime import date, timedelta

from sqlalchemy.orm import Session

from app import models
from app.schemas import ContactCreate, ContactUpdate


def get_contacts(db: Session):
    return db.query(models.Contact).all()


def get_contact(db: Session, contact_id: int):
    return (
        db.query(models.Contact)
        .filter(models.Contact.id == contact_id)
        .first()
    )


def create_contact(db: Session, contact: ContactCreate):
    db_contact = models.Contact(**contact.model_dump())

    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)

    return db_contact


def update_contact(db: Session, db_contact: models.Contact, contact: ContactUpdate):
    for field, value in contact.model_dump().items():
        setattr(db_contact, field, value)

    db.commit()
    db.refresh(db_contact)

    return db_contact


def delete_contact(db: Session, db_contact: models.Contact):
    db.delete(db_contact)
    db.commit()


def search_contacts(db: Session, query: str):
    search = f"%{query}%"

    return (
        db.query(models.Contact)
        .filter(
            (models.Contact.first_name.ilike(search))
            | (models.Contact.last_name.ilike(search))
            | (models.Contact.email.ilike(search))
        )
        .all()
    )


def get_upcoming_birthdays(db: Session):
    today = date.today()
    end_date = today + timedelta(days=7)

    contacts = db.query(models.Contact).all()

    upcoming = []

    for contact in contacts:
        birthday = contact.birthday.replace(year=today.year)

        if today <= birthday <= end_date:
            upcoming.append(contact)

    return upcoming