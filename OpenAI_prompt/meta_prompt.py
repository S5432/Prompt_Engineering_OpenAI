from openai import OpenAI
from dotenv import load_dotenv
import os       

# Load environment variables from .env file
load_dotenv()

######################################################################################
# Define the parameter for the model which we can update as per our requirements
######################################################################################

def set_open_params(
        model  = "gpt-4.1",
        temperature = 0.4,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,):
    ## set openai parameters
    openai_params = {
        "model": model,
        "temperature": temperature,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
    }
    return openai_params

######################################################################################
# define function for chat completion
#######################################################################################
# 
def chat_completion(params,messages):
    client = OpenAI()
    completion = client.chat.completions.create(
        messages = messages,
        **params
    )
    return completion.choices[0].message.content


params = set_open_params()

######################################## Meta Prompt  ##############################################

# Step 1 ask chat gpt to create  good prompt for the task
meta_prompt = ''' Write a good prompt for summarizing news articles in 3 bullet points '''

messages = [
    {
        "role": "user",
        "content": meta_prompt
    }
]

generated_prompt  = chat_completion(params, messages)
print("Generated Prompt:",generated_prompt)

# step 2 : Use the generaated prompt to summarize an article
article = ''' 
Apple Inc. unveiled its latest product line at the annual developer conference, 
introducing new MacBooks with proprietary chips and updated versions of iOS and macOS. 
The company emphasized AI integration and sustainability efforts. 
Investors responded positively, with the stock price climbing after the announcement.
'''

# Insert artivcle into the generated prompt
final_prompt = f"{generated_prompt}\n\n{article}"
print("Final Prompt:",final_prompt)

# step 3 : Use the final prompt to summarize the article
messages = [
    {
        "role": "user",
        "content": final_prompt
    }
]

summary  = chat_completion(params, messages)
print("Summary:", summary)
