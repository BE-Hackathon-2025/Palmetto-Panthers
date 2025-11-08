import json
import firebase_admin
from firebase_admin import credentials, firestore
from Backend.config.bedrock_config import bedrock

# --- Firebase Setup ---
if not firebase_admin._apps:
    cred = credentials.Certificate("Backend/config/firebase_service_key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

USER_ID = "aman"  # active user doc id

# --- Helpers ---
def get_user_data():
    doc_ref = db.collection("users").document(USER_ID)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        print(f"✅ Loaded user '{USER_ID}' data.\n")
        return data
    else:
        raise Exception(f"User '{USER_ID}' not found in Firestore.")


def update_summary(new_summary):
    db.collection("users").document(USER_ID).update({"summary": new_summary})
    print("✅ Summary updated in Firebase.\n")


# --- Main Chat (Claude Sonnet 4.5) ---
# def chat_with_claude(user_data, user_input):
#     """
#     Sends the conversation to Claude Sonnet 4.5 using the user's full financial context.
#     """
#     context = json.dumps({
#         "name": user_data.get("name", "Unknown"),
#         "income": user_data.get("income", "Not provided"),
#         "employment_status": user_data.get("employment_status", "Unknown"),
#         "credit_score": user_data.get("credit_score", "Not available"),
#         "debts": user_data.get("debts", []),
#         "savings": user_data.get("savings", "Not available"),
#         "readiness_score": user_data.get("readiness_score", "Not calculated"),
#         "location": user_data.get("location", "Unknown"),
#         "goals": user_data.get("goals", "Unknown"),
#         "summary": user_data.get("summary", "No summary found.")
#     }, indent=2)

#     body = json.dumps({
#         "anthropic_version": "bedrock-2023-05-31",
#         "max_tokens": 400,
#         "system": (
#             "You are a financial readiness advisor helping users improve their mortgage readiness. "
#             "Use the provided user data to give personalized, actionable responses."
#         ),
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": f"User profile:\n{context}\n\nUser question: {user_input}"}
#                 ]
#             }
#         ],
#     })

#     response = bedrock.invoke_model(
#         modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/global.anthropic.claude-sonnet-4-20250514-v1:0",
#         body=body,
#         contentType="application/json",
#         accept="application/json",
#     )
#     response_json = json.loads(response["body"].read())
#     return response_json["content"][0]["text"]
def chat_with_claude(user_data, user_input):
    """
    Sends the conversation to Claude Sonnet 4.5 using the user's full financial context.
    """

    context = json.dumps({
        "name": user_data.get("name", "Unknown"),
        "monthly_income": user_data.get("monthly_income", "Not provided"),
        "monthly_debt": user_data.get("monthly_debt", "Unknown"),
        "monthly_rent": user_data.get("monthly_rent", "Unknown"),
        "credit_score": user_data.get("credit_score", "Not available"),
        "down_payment_savings": user_data.get("down_payment_savings", "Unknown"),
        "emergency_savings_months": user_data.get("emergency_savings_months", "Unknown"),
        "expected_home_price": user_data.get("expected_home_price", "Unknown"),
        "employment_status": user_data.get("employment_status", "Unknown"),
        "years_stable_income": user_data.get("years_stable_income", "Unknown"),
        "readiness_score": user_data.get("readiness_score", "Not calculated"),
        "qualification_threshold": user_data.get("qualification_threshold", "N/A"),
        "summary": user_data.get("summary", "No summary found.")
    }, indent=2)

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "system": (
            "You are **AURA**, an AI Mortgage Readiness Coach and financial advisor. "
            "You act like a calm, knowledgeable professional who understands personal finance deeply. "
            "Your tone should be warm, motivational, and data-driven — like a private financial coach guiding a real client.\n\n"
            "Guidelines:\n"
            "1. Always ground your advice in the user’s actual numbers and context.\n"
            "2. Focus on actionable, step-by-step improvement strategies (credit, savings, debt management, housing options).\n"
            "3. When the user asks a question, answer it clearly, then end with a short next-step recommendation.\n"
            "4. Never generalize — speak *to* the user, not *about* users.\n"
            "5. Structure each reply in sections:\n"
            "   **Summary of Situation**, **Advice**, and **Next Step**.\n"
            "6. Avoid repetition or filler words like 'as an AI model'. You are their personal financial readiness advisor."
        ),
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"User profile:\n{context}\n\nUser question: {user_input}"
                    }
                ]
            }
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

# --- Summary Update (Claude Haiku 4.5) ---
# def update_summary_with_llm(user_data, user_input, llm_response):
#     """
#     Uses Claude Haiku 4.5 for faster, cheaper summary updates.
#     """

#     update_prompt = (
#         f"Current user summary:\n{user_data.get('summary', 'None')}\n\n"
#         f"User context:\n"
#         f"- Name: {user_data.get('name', 'Unknown')}\n"
#         f"- Income: {user_data.get('income', 'Unknown')}\n"
#         f"- Readiness score: {user_data.get('readiness_score', 'Unknown')}\n"
#         f"- Debts: {user_data.get('debts', 'Unknown')}\n"
#         f"- Goals: {user_data.get('goals', 'Unknown')}\n\n"
#         f"Conversation:\n"
#         f"User: {user_input}\n"
#         f"Assistant: {llm_response}\n\n"
#         f"Please update the summary with any new facts about the user. "
#         f"Keep it concise (2-3 sentences max)."
#     )

#     body = json.dumps({
#         "anthropic_version": "bedrock-2023-05-31",
#         "max_tokens": 150,
#         "system": "You maintain a running summary of what the user says about themselves for a mortgage readiness assistant.",
#         "messages": [{"role": "user", "content": [{"type": "text", "text": update_prompt}]}],
#     })

#     # 👇 Haiku model used here
#     response = bedrock.invoke_model(
#         modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0",
#         body=body,
#         contentType="application/json",
#         accept="application/json",
#     )

#     response_json = json.loads(response["body"].read())
#     return response_json["content"][0]["text"]
def update_summary_with_llm(user_data, user_input, llm_response):
    """
    Uses Claude Haiku 4.5 for faster, cheaper summary updates.
    """

    update_prompt = f"""
You are the memory manager for AURA, an AI mortgage readiness advisor.
Your job is to maintain an evolving, factual summary of the user’s financial situation and goals.

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

Conversation:
User said: {user_input}
Assistant replied: {llm_response}

Task:
Update the summary by adding any new facts, goals, or plans mentioned by the user.
Keep it concise (3–4 sentences max). Do not restate old data unless updated.
End with an estimated mortgage readiness timeline if relevant.
"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 150,
        "system": "You maintain AURA’s internal summary of each user's evolving financial and housing profile.",
        "messages": [{"role": "user", "content": [{"type": "text", "text": update_prompt}]}],
    })

    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    response_json = json.loads(response["body"].read())
    return response_json["content"][0]["text"]


# --- Chat Loop ---
if __name__ == "__main__":
    user_data = get_user_data()
    print("💬 Chat started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Ending chat.")
            break

        # Get Claude Sonnet response
        llm_response = chat_with_claude(user_data, user_input)
        print(f"\nAssistant: {llm_response}\n")

        # Update summary using Haiku
        new_summary = update_summary_with_llm(user_data, user_input, llm_response)
        update_summary(new_summary)

        # refresh summary locally
        user_data["summary"] = new_summary