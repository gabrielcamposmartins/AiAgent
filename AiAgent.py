import requests
import webbrowser
import json

PINK = '\033[95m'
NEON_GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET_COLOR = '\033[0m'
# Ollama Server URL (Assuming you're running it locally on the default port)
OLLAMA_BASE_URL = 'http://localhost:11434'

# Map intents to functions
# Define your pre-existing functions
def search_web(query):
    webbrowser.open(f'https://www.google.com/search?q={query}')
    return f'I have opened a web search for "{query}".'

def print_camel():
    print('camelo camelo camelo camelo camelo')

function_map = {
    'search_web': search_web,
    'print_camel': print_camel
}

def process_input(user_input, model="llama3"):
    """Processes user input, gets intent from Ollama, and calls the function."""
    prompt = f'Intent: {user_input}\n'  # Format the prompt for Ollama
    # Send the prompt to Ollama and get the response
    response = requests.post(
        f'{OLLAMA_BASE_URL}/api/generate',
        json={'model': model, 'prompt': prompt},
        stream=True
    )
    intent = ""
    for chunk in response.iter_lines():
        if chunk:
            decoded_chunk = json.loads(chunk.decode('utf-8'))['response']
            if json.loads(chunk.decode('utf-8'))['done'] != True:
                intent += decoded_chunk
                # print(decoded_chunk, end="")
            else:
                intent += decoded_chunk + "\n" 
                # print(decoded_chunk, end="\n")
    return intent
    # if intent in function_map:
    # for intent in function_map:
    # if intent.find():
    #     function_to_call = function_map[intent]
    #     result = function_to_call(user_input)
    #     return result
    # else:
    #     return "I don't understand that command."

# print(function_map.keys().)
# " + function_map.keys + "
setup_context = "You're my personal assistant ai and you have access to this functions: search_web, print_camel\n do as i say when i ask you to, respond this message with an ok"

print('Agent:', process_input(setup_context))

# Main interaction loop
while True:
    user_input = input('You: ')
    if user_input.lower() == 'exit':
        break
    response = process_input(user_input)
    print('Agent:', response)
