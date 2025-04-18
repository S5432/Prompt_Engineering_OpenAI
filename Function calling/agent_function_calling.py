from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from pydantic import BaseModel, Field, HttpUrl  # 
from typing import Dict, List, Optional

from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

from typing import Dict, List, Optional
from datetime import datetime
import json
import requests

from dotenv import load_dotenv
import os       

# Load environment variables from .env file
load_dotenv()

# Setup the Langchain ChatOpenAI model
llm   = ChatOpenAI(model="gpt-4o",
            temperature=0.4)

################# tool calling agent #################  

from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor


# Get the prompt
oaif_prompt = hub.pull("hwchase17/openai-functions-agent")
######### defining tools #########
@tool
def get_exchange_rate(base_currency: str, target_currency: str, date: str = "latest") -> float:
    """Get the latest exchange rate between two currency. Date defaults latest if not provided."""
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base_currency.lower()}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get(base_currency.lower(), {}).get(target_currency.lower(), None)
    else:
        raise Exception(f"Failed to fetch exchange rate: {response.status_code}")


################ Using built in LangChain tool integrations ################

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults

wrapper = DuckDuckGoSearchAPIWrapper(max_results=10)
web_search = DuckDuckGoSearchResults(api_wrapper=wrapper)

print(get_exchange_rate.invoke({"base_currency": "usd", "target_currency": "jpy"}))


llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
tools = [web_search, get_exchange_rate]


# Create the agent
oaif_agent = create_tool_calling_agent(llm, tools, oaif_prompt)

# Create the Agent Executor
# This is the runtime for an agent. This is what actually calls the agent, executes the actions it chooses, passes the action outputs back to the agent, and repeats. I
oaif_agent_executor = AgentExecutor(agent=oaif_agent, tools=tools, verbose=True)

######## invoking the agent ########    

query = "When was langgraph cloud released? and how much is a dollar worth in japan rn"

response = oaif_agent_executor.invoke({"input": query})

print("\n", response['output'])