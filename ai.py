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
                purpose="user_file"
                )
        return file.id
    except Exception as e:
        print("Error while uploading file:", e)
        return None

# repsonse from GPT       
def get_response(question, file_id):
         
    try:
        response = client.chat,completions.create(
                model="gpt-4o-mini",
                input=[
                    
                        {   "role": "system",
                            "content": "Act as a science teacher and explain to a 7 year old about the book uploaded. Also make sure answers \
                                        should be only about the subject like science, astronomy, astrophysics, planetary science,cosmology strictly. If asked any other question \
                                            other than the topic tell them this is not realted to subject"
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
        return response.choices[0].message.content
        # return print("WALL-E:", response.output_text)
    except Exception as e:
        print("Failed to get a response:", e)
        return None