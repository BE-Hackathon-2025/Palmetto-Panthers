import firebase_admin
from firebase_admin import credentials, firestore

def get_firebase_client():
    if not firebase_admin._apps:
        cred = credentials.Certificate("Backend/config/firebase_service_key.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_firebase_client()