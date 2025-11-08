from Backend.config.firebase_config import db

def get_user_data(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise ValueError(f"User '{user_id}' not found.")

def update_user_summary(user_id: str, new_summary: str):
    db.collection("users").document(user_id).update({"summary": new_summary})
    return True