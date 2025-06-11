from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

file = client.files.create(
    file=open("Alright.pdf", "rb"),
    purpose="user_data"
)

file_id = file.id

while True :
    user=input("User: ")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[         
            {
                "role": "user", 
                "content": [
                    { "type":  "input_file", "file_id": file.id},
                    { "type": "input_text", "text": user}
                ]
            }
        ]
    )

    # Print response
    print("GPT:", response.choices[0].message.content)