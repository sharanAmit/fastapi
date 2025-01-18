# from typing import Union
from fastapi import APIRouter, FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
from fastapi import Request, HTTPException, Depends
from datetime import datetime
from config.db import connection
# from models.notes_model import Notes, NotesCreate, NotesUpdate
# from schemas.notes_schema import noteEntity, notesEntity
from fastapi import Request, HTTPException, Depends
from datetime import datetime, timedelta
from config.tokenize import decode_access_token, create_access_token, oauth2_scheme, get_current_user

note = APIRouter()
# templates = Jinja2Templates(directory="templates")

@note.get("/get_notes")
async def read_item():
    # Fetch all documents from the notes collection
    docs = connection.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append(
            {
                "id": str(doc["_id"]),  # Convert ObjectId to string
                "title": doc["title"],
                "description": doc["description"],
                "important": doc["important"],
            }
        )

    return newDocs

@note.post("/login")
async  def login (request: Request):
    form = await  request.form()
    form_dict = dict(form)
    missing_fields = []
    if not form_dict.get("user_phone"):
        missing_fields.append("user_phone")
    if not form_dict.get("user_password"):
        missing_fields.append("user_password")

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing or empty mandatory fields: {', '.join(missing_fields)}"
        )
    # filter = {"_id": }
    user = connection.user.user.find_one(form_dict)
    token = create_access_token({"id": str(user["_id"])})
    print(f"user type printing ===> {user}")
    return {"Success": True, "Message": "User Registered successfully!", "token": token}

@note.post("/user_registration")
async def user_registration(request: Request):
    form = await request.form()
    form_dict = dict(form)
    missing_fields = []
    if not form_dict.get("user_name"):
        missing_fields.append("user_name")
    if not form_dict.get("user_phone"):
        missing_fields.append("user_phone")
    if not form_dict.get("user_address"):
        missing_fields.append("user_address")
    if not form_dict.get("device_id"):
        missing_fields.append("device_id")
    if not form_dict.get("user_password"):
        missing_fields.append("user_password")

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing or empty mandatory fields: {', '.join(missing_fields)}"
        )
    form_dict["created_at"] = datetime.now()
    form_dict["updated_at"] = datetime.now()

    user = connection.user.user.insert_one(form_dict)
    token = create_access_token({"id":str(user.inserted_id)})
    print(f"user type printing ===> {type(user.inserted_id)}")
    return {"Success": True, "Message": "User Registered successfully!", "token": token}


@note.post("/add_notes")
async def add_notes(
    request: Request,
    current_user: str = Depends(get_current_user)  # Use token validation function
):
    form = await request.form()
    form_dict = dict(form)
    print("apple")
    form_dict["important"] = True if form_dict.get("important") == "on" else False

    # Mandatory field validation
    missing_fields = []
    if not form_dict.get("title"):
        missing_fields.append("title")
    if not form_dict.get("description"):
        missing_fields.append("description")
    if not form_dict.get("important"):
        missing_fields.append("important")

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing or empty mandatory fields: {', '.join(missing_fields)}"
        )

    # Add timestamps
    form_dict["created_at"] = datetime.now()
    form_dict["updated_at"] = datetime.now()

    # Associate the note with the authenticated user
    form_dict["username"] = current_user  # Attach the user info to the note

    # Insert into the database
    note = connection.notes.notes.insert_one(form_dict)

    return {"Success": True, "Message": "Note added successfully!"}
