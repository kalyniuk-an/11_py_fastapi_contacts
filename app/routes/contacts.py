from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import ContactCreate, ContactResponse, ContactUpdate

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
):
    return crud.create_contact(db, contact)


@router.get(
    "/search",
    response_model=list[ContactResponse],
)
def search_contacts(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    return crud.search_contacts(db, query)


@router.get(
    "/birthdays",
    response_model=list[ContactResponse],
)
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
):
    return crud.get_upcoming_birthdays(db)


@router.get(
    "/",
    response_model=list[ContactResponse],
)
def get_contacts(
    db: Session = Depends(get_db),
):
    return crud.get_contacts(db)


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
):
    contact = crud.get_contact(db, contact_id)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return contact


@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
):
    db_contact = crud.get_contact(db, contact_id)

    if db_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    return crud.update_contact(db, db_contact, contact)


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
):
    db_contact = crud.get_contact(db, contact_id)

    if db_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )

    crud.delete_contact(db, db_contact)