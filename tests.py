import sys
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def access_sys_argv(index):
    if len(sys.argv) > index:
        return sys.argv[index]

def test():
    if access_sys_argv(1) == "--get_files":
        return get_files_info("calculator", access_sys_argv(2))
    if access_sys_argv(1) == "--get_content":
        return get_file_content("calculator", access_sys_argv(2))
    if access_sys_argv(1) == "--write_file":
        return write_file("calculator", access_sys_argv(2), access_sys_argv(3))
    if access_sys_argv(1) == "--run_file":
        return run_python_file("calculator", access_sys_argv(2))
    if access_sys_argv(1) == "--help" or access_sys_argv(1) == "-h":
        return "python3 tests.py --action 'working_directory' 'directory'\naction can be:\n--get_files: to list files in directory\n--get_content: to show content of file\n--write_file: overwrite the file with given content: 'content' | str\n--run_file: to run python file"
    else:
        return "use python3 tests.py -h or\npython3 tests.py --help for help"


print(test())
