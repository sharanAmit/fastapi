from xmlrpc.client import DateTime

from pydantic import BaseModel
from datetime import datetime

class Notes(BaseModel):
    id: int
    title: str
    description: str
    created_at: str
    updated_at: str
    deleted_at: str
    important: bool



class UserModel(BaseModel):
    id: int
    user_name: str
    user_phone: int
    user_address: str
    device_id: str
    device_type: str
    user_mail: str
    user_password: str
    created_at: datetime.now()
    updated_at: datetime.now()