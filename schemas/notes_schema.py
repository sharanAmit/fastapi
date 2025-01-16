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


def userRegistrationEntity(users) -> dict:
    return {
        "id": users["_id"],
        "user_name": users["user_name"],
        "user_phone": users["user_phone"],
        "user_address": users["user_address"],
        "device_id": users["device_id"],
        "device_type": users["device_type"],
        "user_mail": users["user_mail"],
        "user_password": users["user_password"],
        "created_at": users["created_at"],
        "updated_at": users["updated_at"],
        "deleted_at": users["deleted_at"],
    }

def usersEntity(item) -> list:
    return [userRegistrationEntity(item) for item in item]