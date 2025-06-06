from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Test request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello!"}]
)

# Print response
print(response.choices[0].message.content)