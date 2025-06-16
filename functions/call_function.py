from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(function_call_part, verbose=False):
    func_name = function_call_part.name
    func_args = function_call_part.args
    func_args['working_directory'] = './calculator'
    func_dict = {
        "get_files_info": get_files_info, 
        "get_file_content": get_file_content, 
        "write_file": write_file, 
        "run_python_file": run_python_file
    }
    
    if verbose:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")
    
    result = func_dict[func_name](**func_args)

    if not str(func_name) in func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": result},
            )
        ],
    )
    

    