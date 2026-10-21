import os

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    f = open(target_file)

    content = f.read(MAX_CHARS)

    if f.read(1):
        content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    
    return content



schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists specified file's content up to certain limit of 10000 characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to get the target file path from",
                },
            },
            "required": ["file_path"],
        },
    },
}