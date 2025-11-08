import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("Backend/config/firebase_service_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_user_data(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise Exception(f"User '{user_id}' not found.")

def update_user_summary(user_id: str, new_summary: str):
    db.collection("users").document(user_id).update({"summary": new_summary})
    print("✅ Summary updated in Firebase.\n")