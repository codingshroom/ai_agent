import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
result = load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def access_sys_argv(index):
    if len(sys.argv) > index:
        return sys.argv[index]


def main():
    prompt = str(access_sys_argv(1))
    if prompt == "None":
        print("no prompt provided")
        exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages,)

    if access_sys_argv(2) == "--verbose":
        print("User prompt:", response.text)
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", response_tokens)


if __name__ == "__main__":
    main()
