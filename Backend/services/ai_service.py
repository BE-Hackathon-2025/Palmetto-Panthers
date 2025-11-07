import json
from Backend.config.bedrock_config import bedrock

def generate_answer(user_query: str, context: str):
    body = json.dumps({
        "prompt": f"\n\nHuman: {user_query}\n\nContext:\n{context}\n\nAssistant:",
        "max_tokens_to_sample": 400,
        "temperature": 0.3
    })
    response = bedrock.invoke_model(
        modelId="anthropic.claude-sonnet-4-5-20250929-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json"
    )
    result = json.loads(response["body"].read())
    return result["completion"]