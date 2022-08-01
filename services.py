from typing import TYPE_CHECKING, List
import pydantic as _pydantic

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import database as _database
import models as _models
import schemas as _schemas


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


def add_to_db(db: "Session", model: _pydantic.BaseModel):
    db.add(model)
    db.commit()
    db.refresh(model)


def commit_to_db(db: "Session", model: _pydantic.BaseModel):
    db.commit()
    db.refresh(model)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_for_duplicates(email: str, phone_number: str, db: "Session") -> bool:
    db_email = db.query(_models.Contact).filter(_models.Contact.email == email).first()
    db_phone_number = db.query(_models.Contact).filter(_models.Contact.phone_number == phone_number).first()

    if db_email is not None or db_phone_number is not None:
        return True

    return False


async def create_contact(contact: _schemas.CreateContact, db: "Session") -> _schemas.Contact:
    contact = _models.Contact(**contact.dict())
    add_to_db(db=db, model=contact)

    return _schemas.Contact.from_orm(contact)


async def get_all_contacts(db: "Session") -> List[_schemas.Contact]:
    contacts = db.query(_models.Contact).all()
    return list(map(_schemas.Contact.from_orm, contacts))


async def get_contact_by_id(db: "Session", contact_id: int) -> _schemas.Contact:
    contact = db.query(_models.Contact).filter(_models.Contact.id == contact_id).first()
    return contact


async def delete_contact(contact: _models.Contact, db: "Session"):
    db.delete(contact)
    db.commit()


async def update_contact(contact_data: _schemas.CreateContact, contact: _models.Contact, db: "Session") -> _schemas.Contact:
    contact.first_name = contact_data.first_name
    contact.last_name = contact_data.last_name
    contact.email = contact_data.email
    contact.phone_number = contact_data.phone_number

    commit_to_db(db=db, model=contact)
    return _schemas.Contact.from_orm(contact)
