import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

load_dotenv()
result = load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question !!always!! explore the current directory first! then and only then make a function call plan. You can perform the following operations:

- List files and directories (!!!do this first!!!)
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. Do !!!NOT!!! specify the working directory in your function calls as it is automatically injected.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="shows content of file in the directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The file_path to show content from, relative to the working directory. If file doesn't exist returns Error: not found",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="overwrites any content of the given file with give content, constrained to the working directory. If file doesn't exist it will create it and write the content in it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The file_path to the file in question, relative to the working directory. If not provided, returns Error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content"
            )
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the given python file, constrained to the working directory. If file doesn't exist it will return Error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The file_path to the file in question, relative to the working directory. If not provided or doesn't exist, returns Error.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content, 
        schema_write_file, 
        schema_run_python_file
    ]
)


def access_sys_argv(index):
    if len(sys.argv) > index:
        return sys.argv[index]


def main():
    prompt = str(access_sys_argv(1))
    if prompt == "None":
        print("no prompt provided")
        exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    
    i = 0
    while i < 20:
        response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages, 
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, 
            tools=[available_functions]
            )
        )

        function_call = response.function_calls
        for candidate in response.candidates:
            messages.append(candidate.content)

        if not function_call:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print("AI Response:", response.text)
            print("Prompt tokens:", prompt_tokens)
            print("Response tokens:", response_tokens)
            break
        else: 
            types_content = call_function(function_call[0])
            messages.append(types_content)
        
        if not types_content.parts[0].function_response.response:
            raise Exception("Fatal Error: of some sort")
        for arg in sys.argv:
            if arg == "--verbose":
                print(f"-> {types_content.parts[0].function_response.response["result"]}")

        i += 1

if __name__ == "__main__":
    main()
