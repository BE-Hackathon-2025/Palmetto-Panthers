# import json
# from Backend.config.bedrock_config import bedrock

# def get_embedding(text: str):
#     body = json.dumps({"inputText": text})
#     response = bedrock.invoke_model(
#         modelId="amazon.titan-embed-text-v2:0",
#         body=body,
#         contentType="application/json",
#         accept="application/json"
#     )
#     result = json.loads(response["body"].read())
#     return result["embedding"]

import json
from qdrant_client.http import models

from Backend.config.bedrock_config import bedrock


# 1️⃣  Create embedding using Amazon Titan
def get_embedding(text: str):
    try:
        body = json.dumps({"inputText": text})
        response = bedrock.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=body,
            contentType="application/json",
            accept="application/json"
        )
        result = json.loads(response["body"].read())
        return result["embedding"]
    except Exception as e:
        print(f"❌ Embedding generation failed: {e}")
        return None


# 2️⃣  Initialize Qdrant collection
def init_collection():
    try:
        qdrant_client.recreate_collection(
            collection_name="bridge_context",
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
        )
        print("✅ Qdrant collection 'bridge_context' initialized.")
    except Exception as e:
        print(f"❌ Failed to initialize collection: {e}")


# 3️⃣  Search similar vectors
def search_similar(query_vector, top_k=3):
    try:
        search_result = qdrant_client.search(
            collection_name="bridge_context",
            query_vector=query_vector,
            limit=top_k
        )
        return search_result
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []