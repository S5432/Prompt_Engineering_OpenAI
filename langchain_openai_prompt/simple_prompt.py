from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Setup the Langchain ChatOpenAI model
llm   = ChatOpenAI(model="gpt-4o",
            temperature=0.4)

# Send a message to the model
response = llm([HumanMessage(content="Hello!")])

# Print the model's response
print(response.content)
