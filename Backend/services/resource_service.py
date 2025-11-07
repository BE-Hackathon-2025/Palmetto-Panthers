from firebase_admin import firestore
from Backend.config.qdrant_config import qdrant
from Backend.services.embeddings_service import get_embedding
from qdrant_client.http import models
import uuid

db = firestore.client()

def add_resource(resource):
    # Save to Firestore
    doc_ref = db.collection("posts").document()
    doc_ref.set(resource)
    
    # Create embedding + save in Qdrant
    text = f"{resource['title']} {resource['description']}"
    emb = get_embedding(text)
    qdrant.upsert(
        collection_name="resources",
        points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=emb,
                payload={"id": doc_ref.id}
            )
        ]
    )
    return {"message": "Resource added successfully", "id": doc_ref.id}