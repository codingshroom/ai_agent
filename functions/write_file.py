import os


def write_file(working_directory, directory, content):
    try:
        work_dir = os.path.abspath(working_directory)
        dirr = os.path.abspath(os.path.join(work_dir, directory))
    except:
        return "Error: os.path.abspath or os.path.join did not work"

    if not dirr.startswith(work_dir):
        return f'Error: Cannot write to "{dirr}" as it is outside the permitted working directory'

    if not os.path.exists(dirr):
        try:
            joined_path = os.path.join(dirr, "..")
            new_path = os.path.abspath(joined_path)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
        except:
            return "Error: os.path.join(), os.path.abspath(), os.path.exists() or (most likely) os.makedirs() failed"
        
        try:
            with open(dirr, "x") as f:
                f.write(content) if content is not None else f.write(str(content))
                return f'Successfully created "{dirr}", successfully wrote to "{dirr}" ({len(str(content))} characters written)'
        except:
            return "Error: open() or .write() failed"

    else:
        try:
            with open(dirr, "w") as f:
                f.write(content) if content is not None else f.write(str(content))
                return f'Successfully wrote to "{dirr}" ({len(str(content))} characters written)'
        except:
            return "Error: open() or .write() failed"
