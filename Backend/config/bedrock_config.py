import boto3, os
from dotenv import load_dotenv

load_dotenv()

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)