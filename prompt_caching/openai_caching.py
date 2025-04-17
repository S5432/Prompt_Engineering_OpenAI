
from openai import OpenAI
import cachetools
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


######################################################################################

# Create a cache with a maximum size of 1000 items
cache = cachetools.LRUCache(maxsize=1000)


def get_prediction(text):
    # Check if the prediction is in the cache
    if text in cache:
        print("Cache hit!")
        return cache[text]
    
    # If not in cache, get prediction from GPT-3
    print("Cache miss! Fetching from GPT-4...")
    client = OpenAI()
    response = client.chat.completions.create(
        model  = "gpt-4.1",
        messages=[{"role": "user", "content": text}],
        temperature=0.4,
        top_p=1,    
        frequency_penalty=0,
        presence_penalty=0,
        
    )
    cache[text] = response.choices[0].message.content
    return cache[text]



if __name__=="__main__":

    print(get_prediction(text="What is the Capital of India? "))
    print(get_prediction(text="What is the Capital of France? "))
    print(get_prediction(text="What is the Capital of India? "))