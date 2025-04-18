from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from pydantic import BaseModel, Field, HttpUrl  # 
from typing import Dict, List, Optional

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


############## Using Pydantic schemas (non-invokable tool) ##############
from langchain_core.pydantic_v1 import BaseModel, Field

class SendEmailCampaignLC(BaseModel):
    "Send a marketing email campaign out to your mailing list"
    
    recipients: List[str] = Field(
        ..., 
        description="List of strings, each an email address. Example: ['example1@mail.com', 'example2@mail.com']"
    )
    subject: str = Field(
        ..., 
        description="String specifying the email's subject line. Example: 'Exciting News!'"
    )
    body_text: str = Field(
        ..., 
        description="Plain text content of the email body. Example: 'We have some exciting updates to share with you.'"
    )

################ Using built in LangChain tool integrations ################

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults

wrapper = DuckDuckGoSearchAPIWrapper(max_results=10)
web_search = DuckDuckGoSearchResults(api_wrapper=wrapper)

print(get_exchange_rate.invoke({"base_currency": "usd", "target_currency": "jpy"}))

print()

print(web_search.invoke("Fun things to do in SF"))


############# atteching the tool to the LLM #############

tools = [web_search, SendEmailCampaignLC, get_exchange_rate]
llm_tools = llm.bind_tools(tools)

# prompt = "How much is a dollar worth in Japan right now"
# prompt = "Can you send an email to adamlucek@youtube.com, samaltman@openai.com, and elonmusk@twitter.com about the cool youtube channel https://www.youtube.com/@AdamLucek"
# prompt = "When was langgraph cloud released?"
prompt = "When was langchain founded? and how much is a dollar worth in japan rn"

output = llm_tools.invoke(prompt)
print("\n---Response---")
print(output)
print("\n---Tool Calls---")
print(output.tool_calls)


###### handling tool calls ######
from langchain_core.messages import HumanMessage, ToolMessage

query = "When was langchain founded? and how much is a dollar worth in japan rn"

messages = [HumanMessage(query)]
ai_msg = llm_tools.invoke(messages)
messages.append(ai_msg)

# Only using web search and exchange rate, and the Pydantic schema is not a full function, just a container for arguments
for tool_call in ai_msg.tool_calls:
    selected_tool = {"duckduckgo_results_json": web_search, "get_exchange_rate": get_exchange_rate}[tool_call["name"].lower()]
    tool_output = selected_tool.invoke(tool_call["args"])
    messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

for i in range(0, len(messages)):
    print("-------")
    print(f"{messages[i].type}: ", messages[i])


final_response = llm_tools.invoke(messages)
print(final_response.content)