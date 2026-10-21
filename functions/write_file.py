import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    f = open(target_file, "w")

    f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes text to a specified file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write to",
                },
                "content": {
                    "type": "string",
                    "description": "The content that shall be written to the FIle"
                }
            },
            "required": ["file_path", "content"],
        },
    },
}