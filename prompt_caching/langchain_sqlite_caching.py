import os
import time
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.globals import set_llm_cache  # Import set_llm_cache
from langchain_core.caches import InMemoryCache 
from langchain_openai import ChatOpenAI
from langchain_community.cache import SQLiteCache
# Initialize OpenAI API and load environment variables
load_dotenv()

# Set up the cache using the new method
set_llm_cache(SQLiteCache(database_path=".langchain.db"))

# To make the caching really obvious, let's use a slower model.
llm = ChatOpenAI(model="gpt-3.5-turbo-16k")  # Corrected model name

# The first time, it is not yet in cache, so it should take longer
prompt = "What is the Capital of France?"

# First call, not cached
with get_openai_callback() as cb:
    print("------------------------------------------")
    start_time = time.time()
    response = llm.invoke(prompt)  # Use invoke for LLM calls
    end_time = time.time()

    print(f"LLM Response: {response}")
    print(f"Time taken: {end_time - start_time:0.2f} sec")
    print(f"{cb}")

    print("------------------------------------------")

# Second call, should be cached
with get_openai_callback() as cb_cache:
    print("------------------------------------------")
    start_time = time.time()
    response = llm.invoke(prompt)  # Use invoke for LLM calls
    end_time = time.time()

    print(f"LLM Response: {response}")
    print(f"Time taken: {end_time - start_time:0.2f} sec")
    print(f"{cb_cache}")

    print("------------------------------------------")