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


@note.post("/",)
async def add_notes(request: Request):
    form = await request.form()
    form_dict = dict(form)
    form_dict["important"]= True if form_dict.get("important") == "on" else False
    form_dict["created_at"] = datetime.now()
    form_dict["updated_at"] = datetime.now()
    print(f"form dict ===> {form_dict}")
    note = connection.notes.notes.insert_one(form_dict)
    return {"Success": True}