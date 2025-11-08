from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Backend.services.firebase_service import get_user_data, update_user_summary
from Backend.services.llm_service import chat_with_claude, update_summary_with_llm

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


# --- Request schema ---
class QueryRequest(BaseModel):
    user_id: str
    query: str


# --- AURA Chat Endpoint ---
@router.post("/chat")
async def chat_with_aura(request: QueryRequest):
    """
    Full AURA AI flow:
    1. Load user data from Firestore.
    2. Run the main LLM (Claude Sonnet 4.5) to answer query.
    3. Run Haiku 4.5 to update the user's summary.
    4. Save new summary back to Firestore.
    5. Return only the AI reply (summary is updated internally).
    """
    try:
        # Step 1: Load user profile
        user_data = get_user_data(request.user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found in database.")

        # Step 2: Generate AI response
        response_text = chat_with_claude(user_data, request.query)

        # Step 3: Update user summary with Haiku
        new_summary = update_summary_with_llm(user_data, request.query, response_text)

        # Step 4: Save updated summary to Firestore
        update_user_summary(request.user_id, new_summary)
        print(f"✅ Summary for user '{request.user_id}' successfully updated in Firestore.")

        # Step 5: Return only AI response to frontend
        return {
            "assistant_response": response_text,
            "user_id": request.user_id
        }

    except Exception as e:
        print(f"❌ Error in chat_with_aura: {e}")
        raise HTTPException(status_code=500, detail=str(e))