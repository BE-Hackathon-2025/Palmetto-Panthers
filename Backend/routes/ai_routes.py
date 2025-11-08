from fastapi import APIRouter
from Backend.services.embedding_service import get_embedding
from Backend.services.ai_service import generate_answer

router = APIRouter()

@router.post("/ai/query")
def query_ai(user_query: str):
    # Step 1: Embed user query
    query_emb = get_embedding(user_query)

    # Step 2: Search Qdrant
    results = qdrant.search(
        collection_name="resources",
        query_vector=query_emb,
        limit=3
    )

    # Step 3: Create context from matched posts
    context = "\n".join([r.payload.get("title", "") for r in results])

    # Step 4: Generate final AI answer
    answer = generate_answer(user_query, context)
    return {"response": answer, "matches": [r.payload for r in results]}