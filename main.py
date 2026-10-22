import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def main():
    #print("User Prompt: ", response.messages)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    for _ in range(2):
        if args.verbose == True:
            print("User prompt: ", args.user_prompt)
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens)


        message = response.choices[0].message
        

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)

                if not result_message["content"]:
                    raise Exception("Fatal: no content in tool response")

                if args.verbose:
                    print(f"-> {result_message['content']}")
                else:
                    print(result_message['content'])

                messages.append(result_message)
        else:
            print("Response: \n", response.choices[0].message.content)
        
        messages.append(message)
    
    return

if __name__ == "__main__":
    main()
