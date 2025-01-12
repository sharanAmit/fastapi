from pydantic import BaseModel


class Notes(BaseModel):
    id: int
    title: str
    description: str
    created_at: str
    updated_at: str
    deleted_at: str
    important: bool

class NotesCreate(BaseModel):
    id: int
    title: str
    description: str

class NotesUpdate(BaseModel):
    id: int
    title: str
    description: str