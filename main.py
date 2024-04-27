from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import contactModel
import contactSchema

app = FastAPI()
contactModel.Base.metadata.create_all(engine)


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return "Hello ADz Community"


@app.get("/contacts")
def getContacts(db: Session = Depends(getDb)):
    contacts = db.query(contactModel.Contact).all()

    return {"contacts": contacts}


@app.get("/contacts/{contactId}")
def getContact(contactId: int, db: Session = Depends(getDb)):
    contact = db.query(contactModel.Contact).filter(
        contactModel.Contact.id == contactId).first()

    return contact


@app.post("/contacts")
def createContact(request: contactSchema.Contact, db: Session = Depends(getDb)):
    contact = contactModel.Contact(
        name=request.name, email=request.email, phone=request.phone)
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


@app.put("/contacts/{contactId}")
def updateContact(contactId: int, request: contactSchema.Contact, db: Session = Depends(getDb)):
    contact = db.query(contactModel.Contact).filter(contactModel.Contact.id == contactId).update(
        {"name": request.name, "email": request.email, "phone": request.phone}
    )
    db.commit()

    return contact


@app.delete("/contacts/{contactId}")
def deleteContact(contactId: int, db: Session = Depends(getDb)):
    contact = db.query(contactModel.Contact).filter(
        contactModel.Contact.id == contactId
    ).delete()
    db.commit()

    return "Contact deleted"
