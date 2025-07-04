from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# file upload
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

# repsonse from GPT       
def get_response(question, file_id):
         
    try:
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    
                        {   "role": "system",
                            "content": "Act as a science teacher and explain to a 7 year old about the book uploaded. Make sure answers \
                                        should be only about the subject realted to science, maths, astronomy, astrophysics, planetary science,\
                                        cosmology.If asked anything else, say its unrealted."
                        },
                    
                        {  "role": "user",
                            "content": [
                                {"type": "file", "file" : {"file_id": file_id}},
                                {"type": "text", "text": question}
                            ]
                        }                    
                ]
            )

        print("@@@@ I am in FILE and QUESTION @@@")
        
        content = response.choices[0].message.content
        print(content)
        return content
        
    except Exception as e:
        print(" ##### Failed to get response:", e)
        return None
    
def handle_message_only(question):
    """Answer only if the question is about science/space"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a science expert. Answer only if the question is related to "
                               "science, astronomy, astrophysics, planetary science, or cosmology. "
                               "If not related, say: 'This is unrelated to space or science.'"
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        print("@@@@ I am ONLYYYY QUESTION @@@")
        
        content = response.choices[0].message.content
        print(content)
        return content
    
    except Exception as e:
        print("Error handling message:", e)
        return "I can't help with that right now."