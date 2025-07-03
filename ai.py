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
                            "content": "Act as a science teacher and explain to a 7 year old about the book uploaded. Also make sure answers \
                                        should be only about the subject like science, astronomy, astrophysics, planetary science,cosmology strictly.\
                                        If asked any other question other than the topic tell them this is not realted to subject. Also if only file is\
                                        uploaded without any uestions asked give summary of uploaded file in 10-15 lines"
                        },
                    
                        {  "role": "user",
                            "content": [
                                {"type": "file", "file" : {"file_id": file_id}},
                                {"type": "text", "text": question}
                            ]
                        }                    
                ]
            )

        print("@@@@ I reached here now wait @@@")
        
        content = response.choices[0].message.content
        print(content)
        return content
        
    except Exception as e:
        print(" ##### Failed to get response:", e)
        return None