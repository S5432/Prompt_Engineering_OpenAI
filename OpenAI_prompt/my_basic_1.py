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
# basic prompt example (Zero SHot Prompting)
######################################################################################

# 1. sentence completion prompt
# prompt = "The sky is"

# 1.1 Text Summarization prompt
prompt = "'Summarize the following text: " \
"'An antibiotic is a type of antimicrobial substance active against bacteria. " \
"It is the most important type of antibacterial agent for fighting bacterial infections, and antibiotic medications are widely" \
" used in the treatment and prevention of such infections.[1][2] They may either kill or inhibit the growth of bacteria. A limited" \
" number of antibiotics also possess antiprotozoal activity.[3][4] Antibiotics are not effective against viruses such as the ones which" \
" cause the common cold or influenza.[5] Drugs which inhibit growth of viruses are termed antiviral drugs or antivirals. Antibiotics are also" \
" not effective against fungi. Drugs which inhibit growth of fungi are called antifungal drugs.'"

# 1.2 Question Answering prompt
prompt2 ='''Answer the question based on the context below. Keep the answer short and concise. 
            Respond "Unsure about answer" if not sure about the answer.

            Context: Teplizumab traces its roots to a New Jersey drug company called Ortho Pharmaceutical. 
            There, scientists generated an early version of the antibody, dubbed OKT3. Originally sourced from mice,
            the molecule was able to bind to the surface of T cells and limit their cell-killing potential. In 1986, 
            it was approved to help prevent organ rejection after kidney transplants, making it the first therapeutic 
            antibody allowed for human use.

            Question: What is Ortho Pharmaceutical?

            Answer:

'''

# 1.3 Text Classification prompt

prompt3 = '''Classify the following text into one of the following categories:
            1. neutral
            2. negative 
            3. positive

            Text: The new smartphone model has been released with advanced features and improved battery life.

            Sentiment:
'''

# 1.4 Role Playing prompt
#example 1
prompt4 = '''You are a helpful assistant. 
            Your task is to provide information about the weather.

            User: What is the weather like today?
            Assistant: The weather today is sunny with a high of 75°F and a low of 55°F.

            User: Will it rain tomorrow?
            Assistant:
'''
# example 2

prompt5 = ''' You are a helpful assistant.
        The following is a conversation with an AI research assistant. The assistant tone is technical and scientific.

        Human: Hello, who are you?
        AI: Greeting! I am an AI research assistant. How can I help you today?
        Human: Can you tell me about the creation of blackholes?
        AI:


'''

# 1.5 Code Generation prompt
prompt6 = ''' Write a Python function to calculate the factorial of a number.

'''

# 1.6 Reasoning prompt

prompt7 = '''
         The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. 
         What is the sum of the odd numbers in this group?
         Solve by breaking the problem into steps. First, identify the odd numbers, add them, and indicate 
         whether the result is odd or even."""


'''

################################################## Few Shot Prompting ##################################################
# 2.1 Few Shot Prompting (Question Answering prompt)

prompt8 = '''Answer the question based on the context below. Keep the answer short and concise.
            Respond "Unsure about answer" if not sure about the answer.

            Context: The capital of France is Paris. Paris is a beautiful city.
            Question: What is the capital of France? 
            Answer: Paris

            Context: The Eiffel Tower is located in Paris.
            Question: Where is the Eiffel Tower located? 
            Answer:
''' 

################################################## chain of thought Prompting ##################################################
# 3.1 Chain of thought Prompting (Arithmetic Reasoning prompt)
prompt9 = '''Answer the question based on the context below. Keep the answer short and concise.
            Respond "Unsure about answer" if not sure about the answer.

            Question: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?
            Answer: Roger started with 5 balls. 2 cans of 3 tennis balls is 2 * 3 = 6 tennis balls. So he has 5 + 6 = 11 tennis balls.

            
            Question: The cafeteria had 23 apples. If they used 10 to make lunch and bought 20 more, how many apples do they have? 
            Answer:
'''

# 3.2 Chain of thought Prompting (Commonsense Reasoning prompt)
prompt10 = '''Answer the question based on the context below. Keep the answer short and concise.
            Respond "Unsure about answer" if not sure about the answer.

            Question: The trophy doesn't fit in the brown suitcase because it's too big. What is the problem?
            Answer: The trophy is too big.

            
            Question: The sun is shining brightly and it is 80 degrees outside. What is the problem?
            Answer:
'''

# 3.3 Chain of thought Prompting (Multi-Step Question Answering prompt)
prompt11 = '''Answer the question based on the context below. Keep the answer short and concise.
            Respond "Unsure about answer" if not sure about the answer.

            Question: The cafeteria had 23 apples. If they used 10 to make lunch and bought 20 more, how many apples do they have?
            Answer: The cafeteria started with 23 apples. They used 10, so 23 - 10 = 13.  They bought 20 more, so 13 + 20 = 33. The answer is 33.

            
            Question: The school had 12 pencils and then 2 more students came and each student was given 3 pencils. How many pencils were left?
            Answer:
'''



# Define the messages for the chat completion
# The messages should be a list of dictionaries with "role" and "content" keys

messages = [
    {
        "role": "user",
        "content": prompt11
    }
]

response  = chat_completion(params, messages)
print(response)