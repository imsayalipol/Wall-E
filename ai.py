from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Upload the file only once
file = client.files.create(
    file=open("DK_Space_Visual_Encyclopedia.pdf", "rb"),
    purpose="user_data"
)
file_id = file.id

while True:
    user = input("User: ")

    response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                
                    {   "role": "system",
                        "content": "Act as a science teacher and explain to a 7 year old about the book uploaded. Also make sure answers \
                                    should be about the subject i.e.science, astronomy, astrophysics, planetary science,cosmology strictly. If asked any other question \
                                        other tha the topic tell them this is not realted to subject"
                    },
                
                    {  "role": "user",
                        "content": [
                            {"type": "input_file", "file_id": file_id},
                            {"type": "input_text", "text": user}
                        ]
                    }
                
            ]
        )

    # Print the response
    print("GPT:", response.output_text)
