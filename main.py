import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a leadership mentor AI."},
        {"role": "user", "content": "How can I improve my confidence as a new leader?"}
    ]
)

print(response.choices[0].message.content)


