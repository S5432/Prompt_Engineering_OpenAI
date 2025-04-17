from openai import OpenAI
from dotenv import load_dotenv
import os       

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
    model = "gpt-4.1",
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    )

print(completion.choices[0].message.content)