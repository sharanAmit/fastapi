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
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import jwt
from datetime import datetime, timedelta




note = APIRouter()
# templates = Jinja2Templates(directory="templates")

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper to decode JWT
def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
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
    print(f"user type printing ===> {user}")
    return {"Success": True, "Message": "Note added successfully!"}


@note.post("/add_notes")
async def add_notes(
    request: Request,
    token: str = Depends(oauth2_scheme)
):
    # here Decode token to authenticate user
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

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

    # Insert into the database
    note = connection.notes.notes.insert_one(form_dict)

    return {"Success": True, "Message": "Note added successfully!"}