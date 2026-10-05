from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_data: str | None = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int

    model_config = ConfigDict(from_attributes=True)