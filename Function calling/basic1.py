from openai import OpenAI
from dotenv import load_dotenv
import os       

# Load environment variables from .env file
load_dotenv()

########################### Define a function that GPT can call ###########################

def add_numbers(a:int,b:int):
    return a + b


############################# Define a function information fot GPT ###########################

functions =[
    {
        "name": "add_numbers",
        "description": "Add two numbers together",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "The first number to add"
                },
                "b": {
                    "type": "integer",
                    "description": "The second number to add"
                }
            },
            "required": ["a", "b"]
        }
    }
]

# user message
user_message = "What is the sum of 5 and 10?"

## ##############################  ASk GPT to decide if it wants to call a function ###########################  
 

client = OpenAI()

# Ask GPT to decide if it wants to call a function
response = client.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": user_message}
    ],
    functions=functions,
    function_call="auto"  # GPT can decide if it wants to call a function
)

# Check if GPT wants to call our function
if response.choices[0].message.get("function_call"):
    function_name = response.choices[0].message["function_call"]["name"]
    arguments = eval(response.choices[0].message["function_call"]["arguments"])

    # Call the actual function
    result = add_numbers(**arguments)

    # Send the result back to GPT to make a nice reply
    second_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": user_message},
            response.choices[0].message,
            {"role": "function", "name": function_name, "content": str(result)}
        ]
    )

    # Final answer from GPT
    print("GPT:", second_response.choices[0].message["content"])
else:
    # No function needed
    print("GPT:", response.choices[0].message["content"])
# completion = client.chat.completions.create(
#     model = "gpt-4.1",
#     messages = [
#         {"role": "user", "content": "Hello, how are you?"}
#     ],
#     )

# print(completion.choices[0].message.content)