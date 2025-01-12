from typing import Union
from datetime import datetime
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config.db import connection
from models.notes_model import Notes, NotesCreate, NotesUpdate
from schemas.notes_schema import noteEntity, notesEntity

note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/",response_class=HTMLResponse)
async def read_item(request: Request):
    docs = connection.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append(
            {
                "id": doc["_id"],
                "title": doc["title"],
                "description": doc["description"],
                "important": doc["important"],
            }
        )
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


from fastapi import Request, HTTPException
from datetime import datetime


@note.post("/add_notes")
async def add_notes(request: Request):
    form = await request.form()
    form_dict = dict(form)

    # Convert "important" checkbox to a boolean value
    form_dict["important"] = True if form_dict.get("important") == "on" else False

    # Mandatory field validation
    missing_fields = []
    if not form_dict.get("title"):
        missing_fields.append("title")
    if not form_dict.get("description"):
        missing_fields.append("description")
    if not form_dict.get("important"):  # Validate the presence of the 'important' field
        missing_fields.append("important")

    # If any mandatory fields are missing, raise an error
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing or empty mandatory fields: {', '.join(missing_fields)}"
        )

    # Add timestamps
    form_dict["created_at"] = datetime.now()
    form_dict["updated_at"] = datetime.now()

    # Insert into the database
    note = connection.notes.notes.insert_one(form_dict)

    return {"Success": True, "Message": "Note added successfully!"}
