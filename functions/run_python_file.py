import os, subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file in a specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the file, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument to be passed to the python file"
                ),
                description="arguments to be passed on to the python file",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]

    if args:
        command.extend(args)

    result = subprocess.run(command, capture_output=True, text=True, timeout=30)

    result_string = ""

    if result.returncode != 0:
        result_string += f'Process exited with code {result.returncode}\n'
    
    if result.stdout == None or result.stderr == None:
        result_string += f'No output produced'
    else:
        result_string += f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}\n'

    return result_string





    