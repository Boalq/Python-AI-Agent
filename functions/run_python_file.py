import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]

    if args is not None:
        command.extend(args)    

    done_obj = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

    output = ""
    
    if done_obj.returncode != 0:
        output += f"Process exited with code {done_obj.returncode}"
    
    if done_obj.stdout == "" and done_obj.stderr == "":
        output += "No output produced"
    
    if done_obj.stdout != "":
        output += f"STDOUT:{done_obj.stdout}\n"
    
    if done_obj.stderr != "":
        output += f"STDERR:{done_obj.stderr}"

    return output

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes or Runs a Python file and returns its output. Use this when the user wants to run or execute a script, not just view its contents",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the File that shall be executed",
                },
                "args": {
                    "type": "array",
                    "description": "The args for the execution",
                    "items": {
                        "type": "string",
                    },
                },
            },
            "required": ["file_path"],
        },
    },
}