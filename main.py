from typing import TYPE_CHECKING, List
from fastapi import FastAPI, Depends, HTTPException, status
import sqlalchemy.orm as _orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import schemas as _schemas
import services as _services

app = FastAPI()


@app.post("/api/contacts", response_model=_schemas.Contact)
async def create_contact(contact: _schemas.CreateContact, db: _orm.Session = Depends(_services.get_db)):
    is_contact_duplicate = _services.check_for_duplicates(email=contact.email, phone_number=contact.phone_number, db=db)

    if is_contact_duplicate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contact with email or phone number exists.")

    return await _services.create_contact(contact=contact, db=db)


@app.get("/api/contacts", response_model=List[_schemas.Contact])
async def get_all_contacts(db: _orm.Session = Depends(_services.get_db)):
    return await _services.get_all_contacts(db=db)


@app.get("/api/contacts/{contact_id}", response_model=_schemas.Contact)
async def get_contact(contact_id: int, db: _orm.Session = Depends(_services.get_db)):
    contact = await _services.get_contact_by_id(db=db, contact_id=contact_id)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contact


@app.delete("/api/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: _orm.Session = Depends(_services.get_db)) -> dict:
    contact = await _services.get_contact_by_id(db=db, contact_id=contact_id)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    await _services.delete_contact(contact=contact, db=db)

    return {
        "message": "Contact has been deleted"
    }


@app.put("/api/contacts/{contact_id}", response_model=_schemas.Contact)
async def update_contact(
        contact_id: int,
        contact_data: _schemas.CreateContact,
        db: _orm.Session = Depends(_services.get_db)):
    contact = await _services.get_contact_by_id(db=db, contact_id=contact_id)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    is_email_or_phone_duplicate = _services.check_for_duplicates(
        email=contact_data.email,
        phone_number=contact_data.phone_number,
        db=db
    )

    if is_email_or_phone_duplicate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contact with email or phone number exists.")

    return await _services.update_contact(contact_data=contact_data, contact=contact, db=db)
