import os
import subprocess


def run_python_file(working_directory, directory):
    work_dir = os.path.abspath(working_directory)
    dirr = os.path.abspath(os.path.join(work_dir, directory))

    if not dirr.startswith(work_dir):
        return f'Error: Cannot execute "{directory}" as it is outside the permitted working directory'

    if not os.path.exists(dirr):
        return f'Error: File "{directory}" not found.'
    
    if not dirr.endswith(".py"):
        return f'Error: "{directory}" is not a Python file.'

    try:
        result = subprocess.run(["python3", dirr], timeout=30, capture_output=True, text=True, cwd=work_dir, )
        if not result.stderr and not result.stdout:
            return "No output produced"
        exit_code = ""
        if result.returncode != 0:
            exit_code = f" Process exited with code {result.returncode}"
        return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}' + (exit_code)

    except Exception as e:
        return f"Error: executing Python file: {e}"

