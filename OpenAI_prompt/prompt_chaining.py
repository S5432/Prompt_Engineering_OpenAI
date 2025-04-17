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


######################################################################################
# Example Article

article = '''
           NASA has announced a new mission to explore the moons of Jupiter, particularly focusing on Europa.
           Scientists believe Europa has a subsurface ocean that may harbor life. 
           The spacecraft is scheduled to launch in 2027 and will carry a suite of instruments to analyze ice, water, and chemical signs of life.
'''


######################################################################################
# Step 1 Extract the main topic of the article

step1_prompt = f'Read the article below and briefly state its main topic:\n\n {article} '


messages = [
    {
        "role": "user",
        "content": step1_prompt
    }
]

main_topic  = chat_completion(params, messages)
print("🧠 Main Topic:",main_topic)

########################################################################################
# step 2 generate a short summary using the topic

step2_prompt = f"'Generate a short summary of the article based on the main topic:\n\n {main_topic}"

messages = [
    {
        "role": "user",
        "content": step2_prompt
    }
]

summary  = chat_completion(params, messages)
print("\n📄 Summary:",summary)


########################################################################################
# Generate 3 question for a discussion based on the summary

step3_prompt = f"'Generate 3 questions for a discussion based on the summary:\n\n {summary}"

messages = [
    {
        "role": "user",
        "content": step2_prompt
    }
]

questions  = chat_completion(params, messages)
print("\n❓ Discussion Questions:\n",questions)