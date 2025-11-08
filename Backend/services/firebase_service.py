# from Backend.config.firebase_config import db

# def get_user_data(user_id: str):
#     doc = db.collection("users").document(user_id).get()
#     if doc.exists:
#         return doc.to_dict()
#     else:
#         raise ValueError(f"User '{user_id}' not found.")

# def update_user_summary(user_id: str, new_summary: str):
#     db.collection("users").document(user_id).update({"summary": new_summary})
#     return True

from Backend.config.firebase_config import db
from datetime import datetime

def _sanitize_firestore_data(data: dict) -> dict:
    """Convert Firestore timestamps and other non-JSON types into serializable formats."""
    clean_data = {}
    for key, value in data.items():
        # Firestore timestamps / datetime
        if hasattr(value, "isoformat"):
            clean_data[key] = value.isoformat()
        # Nested dicts (for safety)
        elif isinstance(value, dict):
            clean_data[key] = _sanitize_firestore_data(value)
        else:
            clean_data[key] = value
    return clean_data


def get_user_data(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return _sanitize_firestore_data(data)
    else:
        raise Exception(f"User '{user_id}' not found.")


def update_user_summary(user_id: str, new_summary: str):
    """Safely update the user's summary field."""
    db.collection("users").document(user_id).update({"summary": new_summary})
    print(f"✅ Summary updated for {user_id}")
    return True
