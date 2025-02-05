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
from datetime import datetime, timedelta, UTC
from config.tokenize import decode_access_token, create_access_token, oauth2_scheme, get_current_user
import httpx
import random
import os
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
def generate_otp():
    return str(random.randint(100000, 999999))

# Fast2SMS API Key (Get from Fast2SMS Dashboard)
FAST2SMS_API_KEY = "oRidPJQ1muTa4zsgBSlcyqVhYxWwfD7NtCUkZE2K8nIGj5XLH0oqrMzA1jWLCPImVfnQZTbkXSRwUuYt"
# OTP Expiry Time (in minutes)
OTP_EXPIRY_MINUTES = 5
@note.post("/send_otp")
async def send_otp(request: Request):
    form = await request.form()
    phone = form.get("user_phone")
    if not phone:
        raise HTTPException(status_code=400, detail="Phone number is required")
    otp = generate_otp()
    expiry_time = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    # Save OTP in DB with timestamp
    connection.OTP.OTP.insert_one({"phone": phone, "otp": otp, "expires_at": expiry_time})
    # Send OTP via Fast2SMS
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.fast2sms.com/dev/bulkV2",
            headers={"authorization": FAST2SMS_API_KEY},
            data={
                "route": "otp",
                "message": f"Your OTP is {otp}",
                "language": "english",
                "flash": 0,
                "numbers": phone
            }
        )
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("return", False):  # Fast2SMS returns "return": True on success
                print(f"OTP {otp} sent to {phone}")
                return {"success": True, "message": "OTP sent successfully!"}
            else:
                raise HTTPException(status_code=500, detail="Failed to send OTP. Please try again.")

        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to send OTP. SMS API error.")

@note.post("/verify_otp")
async def verify_otp(request: Request):
    data = await request.json()
    phone = data.get("phone")
    otp_entered = data.get("otp")

    if not phone or not otp_entered:
        raise HTTPException(status_code=400, detail="Phone number and OTP are required")

    # Fetch OTP from DB
    otp_record = connection.find_one({"phone": phone}, sort=[("expires_at", -1)])

    if not otp_record or otp_record["otp"] != otp_entered:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.now() > otp_record["expires_at"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    return {"success": True, "message": "OTP verified successfully!"}

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
    if not form_dict.get("user_otp"):
        missing_fields.append("user_otp")
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
):
    form = await request.form()
    header =  request.headers
    token = header["authorization"]
    print(token)
    form_dict = dict(form)
    form_dict["important"] = True if form_dict.get("important") == "on" else False
    decryptToken = decode_access_token(token)
    # tokenTime = datetime.fromtimestamp(decryptToken["exp"])
    # if tokenTime  >= datetime.now(UTC):
    #     print(decryptToken["id"])
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
    form_dict["created_at"] = datetime.now()
    form_dict["updated_at"] = datetime.now()
    form_dict["userId"] = decryptToken["id"]
    note = connection.notes.notes.insert_one(form_dict)

    return {"Success": True, "Message": "Note added successfully!"}
