import json
from Backend.config.bedrock_config import bedrock

# --- Main Chat Model (Claude Sonnet 4.5) ---
def chat_with_claude(user_data, user_input):
    context = json.dumps(user_data, indent=2)
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "system": (
            "You are **AURA**, an AI Mortgage Readiness Coach. "
            "Act like a calm, motivational financial advisor who tailors insights using the user's real data.\n\n"
            "Follow this format:\n"
            "**Summary of Situation** – concise recap\n"
            "**Advice** – 2–3 actionable insights grounded in user data\n"
            "**Next Step** – single practical recommendation"
        ),
        "messages": [{
            "role": "user",
            "content": [{"type": "text", "text": f"User data:\n{context}\n\nUser question: {user_input}"}],
        }],
    })

    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/global.anthropic.claude-sonnet-4-20250514-v1:0",
        body=body, contentType="application/json", accept="application/json"
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


# --- Fast Summary Update (Claude Haiku 4.5) ---
def update_summary_with_llm(user_data, user_input, llm_response):
    update_prompt = f"""
You are AURA's memory manager.
Maintain a short factual summary of {user_data.get('name')}’s mortgage readiness progress.

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
        "messages": [{"role": "user", "content": [{"type": "text", "text": update_prompt}]}],
    })

    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:us-east-2:747034604167:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0",
        body=body, contentType="application/json", accept="application/json"
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]