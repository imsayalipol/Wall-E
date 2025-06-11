from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Upload the file only once
file = client.files.create(
    file=open("Alright.pdf", "rb"),
    purpose="user_data"
)
file_id = file.id

while True:
    user = input("User: ")
        
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_file", "file_id": file_id},
                    {"type": "input_text", "text": user}
                ]
            }
        ]
    )

    # Print the response
    print("GPT:", response.output_text)
    # print("GPT:", response.choices[0].message.content)
