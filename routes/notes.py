from typing import Union

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


@note.post("/add_notes",)
async def add_notes(request: Request):
    form = await request.form()
    form_dict = dict(form)
    note = connection.notes.notes.insert_one(form_dict)
    return {"Success": True}