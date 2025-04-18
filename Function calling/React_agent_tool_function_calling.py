from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from pydantic import BaseModel, Field, HttpUrl  # 
from typing import Dict, List, Optional

from langchain import hub
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor

from typing import Dict, List, Optional
from datetime import datetime
import json
import requests

from dotenv import load_dotenv
import os       

# Load environment variables from .env file
load_dotenv()


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


### Custom Prompt for React Agent ###

# react_prompt = """You are a helpful assistant that can use tools to answer questions. You have access to the following tools:
# Use the following format:

# Question: the input question you must answer

# Thought: you should always think about what to do

# Action: the action to take, should be one of [{tools_names}].

# Action Input: the input to the action

# Observation: the result of the action

# ... (this Thought/Action/Action Input/Observation can repeat N times)

# Thought: I now know the final answer

# Final Answer: the final answer to the original input question

# """

######### Create the agent executor #########
react_prompt = hub.pull("hwchase17/react")
react_agent = create_react_agent(llm, tools, react_prompt)
react_agent_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)

query = "When was google cloud released? When was google cloud founded?"

response = react_agent_executor.invoke({"input": query})
