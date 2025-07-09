from dotenv import load_dotenv
import os
from openai import OpenAI
import logging

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """Act as a science teacher and explain things to a 10-year-old.
Only respond about topics related to science, math, astronomy, astrophysics,
planetary science, and cosmology. If asked anything else, say it's unrelated."""

# return file ID for PDF file
def upload_file(file_path):
    try:
        with open(file_path, "rb") as f:
            file = client.files.create(
                file=f,
                purpose="user_data"
                )
        return file.id
    except Exception as e:
        print("Error while uploading file:", e)
        return None

# repsonse from GPT for PDF 
def get_response(question, file_id):        
    try:
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    
                        {   "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                    
                        {  "role": "user",
                            "content": [
                                {"type": "file", "file" : {"file_id": file_id}},
                                {"type": "text", "text": question}
                            ]
                        }                    
                ]
            )        
        
        content = response.choices[0].message.content
        # print(content)
        return content
        
    except Exception as e:
        print("Failed to get response:", e)
        return "I can't help with that right now."
 
# response to text-only inputs
def message_only(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )        
        
        content = response.choices[0].message.content
        # print(content)
        return content
    
    except Exception as e:
        print("Error handling message:", e)
        return "I can't help with that right now."
    
# image analyzer
def image_upload(question, base64_image, file_ext):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{file_ext};base64,{base64_image}",                                
                            }
                        },
                    ],
                }
            ],            
        )

        content = response.choices[0].message.content
        # print(content)
        return content
    
    except Exception as e:
        print("Error while analyzing IMAGE")
        print(e)
        return "Error analyzing image"
