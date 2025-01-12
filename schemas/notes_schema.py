def noteEntity(items) -> dict:
    return {
        "id": items["_id"],
        "title": items["title"],
        "description": items["description"],
        "created_at": items["created_at"],
        "updated_at": items["updated_at"],
        "deleted_at": items["deleted_at"],
        "important": items["important"], 
        }

def notesEntity(item) -> list:
    return [noteEntity(item) for item in item]

