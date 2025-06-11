from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

while True :
    user=input("User: ")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[         
            {"role": "user", "content": user}]
    )

    # Print response
    print("GPT:", response.choices[0].message.content)