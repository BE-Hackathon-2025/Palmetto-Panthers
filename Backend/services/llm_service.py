import json
import datetime
from Backend.config.bedrock_config import bedrock


# --- Helper: Make Firestore data JSON-safe ---
def _serialize_firestore_data(data):
    """Converts Firestore timestamps and nested maps to JSON-safe format."""
    safe_data = {}
    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            safe_data[key] = value.isoformat()
        elif isinstance(value, dict):
            safe_data[key] = _serialize_firestore_data(value)
        else:
            safe_data[key] = value
    return safe_data


# --- Helper: Compact Financial Summary Context ---
def _build_financial_context(user_data):
    """Summarizes readiness_profile for Claude using short sentences."""
    profile = user_data.get("readiness_profile", {}) or {}
    if not profile:
        return "No financial readiness data provided."

    context_lines = []
    fields = {
        "income": "Monthly Income",
        "current_rent": "Rent",
        "monthly_debts": "Debts",
        "savings": "Savings",
        "dpa_funds": "DPA Funds",
        "credit_score": "Credit Score",
        "target_price_min": "Target Price Min",
        "target_price_max": "Target Price Max",
        "down_payment_percent": "Down Payment %",
        "affordability_fit": "Affordability Fit",
        "readiness_score": "Readiness Score",
        "reserves_months": "Reserves (Months)",
        "eta_weeks": "ETA (Weeks)",
        "city_zip": "ZIP Code",
        "state": "State",
    }

    for key, label in fields.items():
        value = profile.get(key)
        if value not in (None, "", 0):
            context_lines.append(f"{label}: {value}")

    return "; ".join(context_lines) if context_lines else "No valid readiness data found."


# --- Main Chat Model (Claude Sonnet 4.5) ---
def chat_with_claude(user_data, user_input):
    """Generates a natural, concise LLM reply using structured readiness + user input."""
    safe_data = _serialize_firestore_data(user_data)
    readiness_context = _build_financial_context(safe_data)
    summary = user_data.get("summary", "No summary available.")

    # Compact system prompt
    system_prompt = (
        "You are **AURA**, an AI Mortgage Readiness Coach. "
        "Speak like a calm, motivational financial advisor using the user’s verified data.\n\n"
        "If a field is missing or unavailable, simply ignore it — never invent numbers.\n\n"
        "Use this exact structure:\n"
        "**Summary of Situation** – brief recap\n"
        "**Advice** – 2–3 actionable insights using the data\n"
        "**Next Step** – a single practical recommendation"
    )

    # Construct prompt for Claude
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            f"User summary:\n{summary}\n\n"
                            f"Financial readiness context:\n{readiness_context}\n\n"
                            f"User question: {user_input}"
                        ),
                    }
                ],
            }
        ],
    })

    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


# --- Fast Summary Update (Claude Haiku 4.5) ---
def update_summary_with_llm(user_data, user_input, llm_response):
    update_prompt = f"""
You are AURA's memory manager.
Maintain a short factual summary of {user_data.get('name', 'the user')}'s mortgage readiness progress.

Existing summary:
{user_data.get('summary', 'No summary yet.')}

Conversation:
User: {user_input}
Assistant: {llm_response}

Update this summary with any new facts, goals, or progress indicators.
Be concise (3–4 sentences max).
"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 150,
        "system": "You maintain AURA’s internal summary for each user.",
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": update_prompt}]}
        ],
    })

    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]