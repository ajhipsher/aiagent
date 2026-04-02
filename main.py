import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
model_name = "gemini-2.5-flash"


def main():
    if api_key == None:
        raise RuntimeError("Your API key isn't working.")
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata == None:
        raise RuntimeError("Usage metadata was not returned.")

    if response.function_calls is not None:
        function_result_list = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if function_call_result.parts is None:
                raise Exception("Parts are None")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Function response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Function response value is None")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_result_list.append(function_call_result.parts[0])

    else:
        print(response.text)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
