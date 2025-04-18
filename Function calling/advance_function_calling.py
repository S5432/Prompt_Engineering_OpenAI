from openai import OpenAI
from pydantic import BaseModel, Field, HttpUrl 
from typing import Dict, List, Optional
from datetime import datetime
import json

from dotenv import load_dotenv
import os       

# Load environment variables from .env file
load_dotenv()

############## Defining the tools properties with pydentic ##############

from enum import Enum

class PriorityLevel(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"

class SendEMailCampaign(BaseModel):

    recipients : List[str] = Field(
        ...,
        description="List of strings, each an email address. Example: ['example1@mail.com', 'example2@mail.com']"

    )

    subject : str = Field(
        ...,
        description="String specifying the email's subject line. Example: 'Exciting News!"
    )

    body_text : str = Field(
        ...,
        description="Plain text content of the email body. Example: 'We have some exciting updates to share with you."
    )
    attachments : List[HttpUrl] = Field(
        default=[],
        description="List of URLs to attachment files. Example: ['http://example.com/attachment1.pdf', 'http://example.com/attachment2.png']"
    )
    personalization : Dict[str, str] = Field(
        default={},
        description="Dictionary for personalizing email content. Key is recipient email, value is a dictionary of variables. Example: {'example1@mail.com': {'first_name': 'John'}, 'example2@mail.com': {'first_name': 'Jane'}}"
    )
    send_time : Optional[datetime] = Field(
        default=None,
        description="The time when the email campaign is to be sent. Example: '2024-07-13T14:30:00'"
    )
    priority : Optional[PriorityLevel]= Field(
        default=None,
        description="Email priority level, Options: 'low', 'normal', 'high', Example: 'high'"
        
   
    )
    tracking: Optional[Dict[str, bool]] = Field(
        default={"open": True, "click": True}, 
        description="Tracking options for the email. Keys can be 'open' and 'click', values are booleans. Example: {'open': True, 'click': True}"
    )
    campaign_id: Optional[str] = Field(
        None, 
        description="Unique identifier for the email campaign for tracking purposes. Example: 'campaign_12345'"
    )


# Function for printing out responses neatly
def pprint_response(response):
    print("--- Full Response ---\n")
    print(response, "\n")
    
    print("--- Chat Completion Message ---\n")
    print(response.choices[0].message, "\n")
    
    if response.choices[0].message.tool_calls:
        for i in range(0, len(response.choices[0].message.tool_calls)):
            print(f"--- Tool Call {i+1} ---\n")
            print(f"Function: {response.choices[0].message.tool_calls[i].function.name}\n")
            print(f"Arguments: {response.choices[0].message.tool_calls[i].function.arguments}\n")

######### ### creating tools  with pydentic schema ##############

email_campaign_tool = [
    {
        "type": "function",
        "function": {
            "name": "send_email_campaign",
            "description": "Send an email campaign to a list of recipients with the specified parameters.",
            "parameters": SendEMailCampaign.model_json_schema(),
        },
    }
        

]


print(email_campaign_tool)


# ###############  Define OpenAI LLM  ###########################
client = OpenAI()
prompt = """
"Can you send an email to adamlucek@youtube.com, samaltman@openai.com, and elonmusk@twitter.com about the cool youtube channel https://www.youtube.com/@AdamLucek 
for July 20th at 8 am pst, this is high priority and include just click tracking and name personalization, 
the campaign is campaign_13, 
also add my linkedin as an attachment https://www.linkedin.com/in/adamrlucek/,
Sign off your response with Adam Ł in the body.
"""

messages = [{"role": "user", 
             "content": prompt}]


response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=email_campaign_tool,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )


# Example function of sending off an Email Campaign
def send_email_campaign(data: dict):
    try:
        # Validate and parse the data using the SendEmailCampaign model
        campaign = SendEMailCampaign(**data)
        
        # Simulate sending the email campaign
        print(f"\nSending email campaign '{campaign.campaign_id or 'N/A'}' with priority '{campaign.priority}':")
        for recipient in campaign.recipients:
            personalized_subject = campaign.subject
            if recipient in campaign.personalization:
                if 'first_name' in campaign.personalization[recipient]:
                    personalized_subject = f"{campaign.personalization[recipient]['first_name']}, {campaign.subject}"
            
            print("-----")
            print(f"\nTo: {recipient}")
            print(f"Subject: {personalized_subject}")
            print(f"Body: {campaign.body_text}")
            if campaign.attachments:
                attachment_urls = [str(url) for url in campaign.attachments]
                print(f"\tAttachments: {', '.join(attachment_urls)}")

        print("-----")
        print(f"\nScheduled Send Time: {campaign.send_time or 'Immediate'}")
        print(f"Campaign ID: {campaign.campaign_id or 'N/A'}")
        print(f"Tracking: {campaign.tracking}")
    except Exception as e:
        print(f"Failed to send email campaign: {e}")

args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
send_email_campaign(args)
