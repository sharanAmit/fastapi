

from pydantic import BaseModel
from pymongo import MongoClient

# app.mount("/templates", templates, name="templates")

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

connection  = MongoClient("mongodb+srv://silentn391:0Q3MWwJ8smtSBbmH@cluster0.d8mm3.mongodb.net")
# db = connection.test
# collection = db.items





# class User(BaseModel):
#     name: str
#     age: int


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.post("/users")
# def create_user(user: User, q: Union[str, None] = None):
#     return {"user": user.dict(), "q": q}


# @app.put("/users/{user_id}")
# def update_user(user_id: int, user: User):
#     return {"user_id": user_id, "user": user.dict()}


# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):        
#     return {"user_id": user_id} 