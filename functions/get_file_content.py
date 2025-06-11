import os

def get_file_content(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_path, file_path))

    print(working_path)
    print(file_path)

    if file_path.startswith(working_path + os.sep) is False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(file_path) is False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        MAX_CHARS = 10000
        file_size = os.path.getsize(file_path)

        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if file_size <= MAX_CHARS:
            return file_content_string
        else:
            return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {str(e)}"