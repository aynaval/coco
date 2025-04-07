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

def get_azure_openai_token() -> str:
    """
    Authenticates using Azure credentials and retrieves an access token.
    """
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    token = credential.get_token("https://cognitiveservices.azure.com/.default").token
    return token

def ask_openai_with_token(token: str, question: str) -> str:
    """
    Uses a provided token to send a question to Azure OpenAI and return the response.
    """
    client = AzureOpenAI(
        api_key=token,
        api_version="2024-02-01",
        azure_endpoint=endpoint
    )
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

    token = get_azure_openai_token()
    print(token)
    print(type(token))
    token1 = input("Enter your token value: ")
    question = input("Enter your question: ")
    answer = ask_openai_with_token(token1, question)
    print("\nResponse from Azure OpenAI:\n", answer)
