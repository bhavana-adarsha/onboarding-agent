import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "arn:aws:bedrock:us-east-1:987956624895:inference-profile/global.anthropic.claude-haiku-4-5-20251001-v1:0"

response = client.converse(
    modelId=MODEL_ID,
    messages=[
        {"role": "user", "content": [{"text": "Reply with exactly: Bedrock is working"}]}
    ],
    inferenceConfig={"maxTokens": 50},
)

print(response["output"]["message"]["content"][0]["text"])
usage = response["usage"]
print(f"Tokens in: {usage['inputTokens']}, out: {usage['outputTokens']}")