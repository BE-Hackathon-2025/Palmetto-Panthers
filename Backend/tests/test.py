import json
import firebase_admin
from firebase_admin import credentials, firestore
from Backend.config.bedrock_config import bedrock

# --- Firebase Setup ---
if not firebase_admin._apps:
    cred = credentials.Certificate("Backend/config/firebase_service_key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

USER_ID = "aman"  # change if needed

# --- Load user once ---
def get_user_data():
    doc_ref = db.collection("users").document(USER_ID)
    doc = doc_ref.get()
    if not doc.exists:
        raise Exception(f"❌ User '{USER_ID}' not found in Firestore.")
    data = doc.to_dict()
    print(f"✅ Loaded user '{USER_ID}' data.\n")
    return data

# --- Save updated summary ---
def update_summary(new_summary):
    db.collection("users").document(USER_ID).update({"summary": new_summary})
    print("✅ Summary updated in Firebase.\n")

# --- Claude (Main Chat: Sonnet 4.5) ---
def chat_with_claude(user_data, user_input):
    # Flatten the user's structured profile into readable context for LLM
    profile_text = f"""
User Financial Profile:
- Name: {user_data.get('name', 'Unknown')}
- Credit Score: {user_data.get('credit_score', 'N/A')}
- Monthly Income: ${user_data.get('monthly_income', 'N/A')}
- Monthly Debt: ${user_data.get('monthly_debt', 'N/A')}
- Monthly Rent: ${user_data.get('monthly_rent', 'N/A')}
- Down Payment Savings: ${user_data.get('down_payment_savings', 'N/A')}
- Emergency Savings: {user_data.get('emergency_savings_months', 'N/A')} months
- Expected Home Price: ${user_data.get('expected_home_price', 'N/A')}
- Employment Status: {user_data.get('employment_status', 'N/A')}
- Years Stable Income: {user_data.get('years_stable_income', 'N/A')}
- Readiness Score: {user_data.get('readiness_score', 'N/A')} / {user_data.get('qualification_threshold', 'N/A')}
- Summary: {user_data.get('summary', 'No summary available')}
    """

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 400,
        "system": (
            "You are a financial readiness advisor that helps users become mortgage-ready. "
            "Use the given financial data and conversation context to give personal, actionable advice."
        ),
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": f"{profile_text}\n\nUser question: {user_input}"}]}
        ],
    })

    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/global.anthropic.claude-sonnet-4-20250514-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    response_json = json.loads(response["body"].read())
    return response_json["content"][0]["text"]

# --- Claude (Summary Update: Haiku 4.5) ---
def update_summary_with_llm(user_data, user_input, llm_response):
    update_prompt = f"""
Current summary:
{user_data.get('summary', 'No summary yet.')}

User data:
- Credit Score: {user_data.get('credit_score')}
- Readiness Score: {user_data.get('readiness_score')}
- Income: ${user_data.get('monthly_income')}
- Debt: ${user_data.get('monthly_debt')}
- Rent: ${user_data.get('monthly_rent')}
- Down Payment: ${user_data.get('down_payment_savings')}
- Emergency Fund: {user_data.get('emergency_savings_months')} months
- Employment: {user_data.get('employment_status')}
- Years Stable Income: {user_data.get('years_stable_income')}

User said: {user_input}
Assistant responded: {llm_response}

Update this summary concisely (2–3 sentences max), adding any new facts mentioned by the user.
"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 150,
        "system": "You maintain a short evolving summary of what the user has shared about their financial situation and goals.",
        "messages": [{"role": "user", "content": [{"type": "text", "text": update_prompt}]}],
    })

    # ✅ Faster model for background summary update
    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    response_json = json.loads(response["body"].read())
    return response_json["content"][0]["text"]

# --- Chat Session ---
if __name__ == "__main__":
    user_data = get_user_data()
    print("💬 Chat started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Ending chat.")
            break

        # Claude Sonnet for main reply
        llm_response = chat_with_claude(user_data, user_input)
        print(f"\nAssistant: {llm_response}\n")

        # Haiku updates summary after each turn
        new_summary = update_summary_with_llm(user_data, user_input, llm_response)
        update_summary(new_summary)

        # keep memory updated locally
        user_data["summary"] = new_summary