import os
import argparse
import sys
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Couldn't load api key")
    
    client = genai.Client(api_key=api_key)


    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt,
                temperature=0),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata == None:
            raise RuntimeError("No Meta Data")
        elif args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_results = []
    
        if response.function_calls:
            for function_call in response.function_calls:
                
                function_call_result = call_function(function_call, args.verbose)

                if function_call_result.parts == None:
                    raise Exception("No data")
                
                if function_call_result.parts[0].function_response == None:
                    raise Exception("No data")
                
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("No data")
                
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

                #print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(response.text)
            return

        messages.append(types.Content(role="user", parts=function_results))
    
    print("No result has been reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
