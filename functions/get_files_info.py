import os


def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."
    try:
        work_dir = os.path.abspath(working_directory)
        dirr = os.path.join(work_dir, directory)
        dirr = os.path.abspath(dirr)  # without it it may look like: Users/projects/ai_agent/.. which would lead to logic errors later
        list_dirr = os.listdir(dirr)
    except:
        return "Error: os.path or os.listdir method failed"

    if not dirr.startswith(work_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(dirr):
        return f'Error: "{directory}" is not a directory'

    output = []
    for element in list_dirr:
        path_to_element = os.path.join(dirr, element)
        try:
            file_size = os.path.getsize(path_to_element)
            is_dir = os.path.isdir(path_to_element)
        except:
            return "Error: os.path method failed"
        element_info = f"- {element}: file_size={file_size} bytes, is_dir={is_dir}"
        output.append(element_info)
    
    return "\n".join(output)
