from azure.identity import ClientSecretCredential
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get values from environment
tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Authenticate using Azure Identity
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Create Azure OpenAI client
client = AzureOpenAI(
    api_key=credential.get_token("https://cognitiveservices.azure.com/.default").token,
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

def ask_openai(question: str) -> str:
    """
    Sends a question to the Azure OpenAI GPT-35 Turbo model and returns the response.
    """
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant working for Cencora."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Example usage:
if __name__ == "__main__":
    user_question = input("Enter your question: ")
    answer = ask_openai(user_question)
    print("\nResponse from Azure OpenAI:\n", answer)
