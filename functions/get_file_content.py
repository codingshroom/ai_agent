import os

MAX_CHARS = 10000


def get_file_content(working_directory, directory): 
    try:
        work_dir = os.path.abspath(working_directory)
        dirr = os.path.join(work_dir, directory)
        dirr = os.path.abspath(dirr)  # dirr without that line could look like this: Users/projects/ai_agent/..
    except:
        return "Error: os.path.abspath() failed"
    
    if not dirr.startswith(work_dir):
        return f'Error: Cannot read "{directory}" as it is outside the permitted working directory'
    if not os.path.isfile(dirr):
        return f'Error: File not found or is not a regular file: "{directory}"'

    with open(dirr, "r") as f:
        try:
            file_content_string = f.read(MAX_CHARS)
            # Check if there's more content by trying to read one more character
            if f.read(1):  # If there's at least one more character
                file_content_string += f'[...File "{directory}" truncated at 10000 characters]'
        except:
            return "Error: either open(directory) or .read() failed"

    return file_content_string
