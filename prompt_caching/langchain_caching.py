import time
from dotenv import load_dotenv
import os
import cachetools
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.globals import set_llm_cache 
from langchain_openai import OpenAI
from langchain_core.caches import InMemoryCache 

# Load environment variables from .env file
load_dotenv()

# To make the caching really obvious, lets use a slower and older model.
# Caching supports newer chat models as well.
# Setup the Langchain ChatOpenAI model
llm   = ChatOpenAI(model="gpt-4o",
            temperature=0.4)

set_llm_cache(InMemoryCache())

prompt="What is the Capital of France?"
# The first time, it is not yet in cache, so it should take longer
# Send a message to the model
response = llm([HumanMessage(content=prompt)])

# Print the model's response
print(response.content)




print("------------------------------------------")
start_time = time.time()
response = response.content
print(response)
end_time = time.time()

print(f"LLM Response: {response}")
print(f"Time taken: {end_time-start_time:0.2f} sec")
# print(f"{cb}")

print("------------------------------------------")



print("------------------------------------------")
start_time = time.time()
response = response
print(response)
end_time = time.time()

print(f"LLM Response: {response}")
print(f"Time taken: {end_time-start_time:0.2f} sec")
# print(f"{cb_cache}")

print("------------------------------------------")