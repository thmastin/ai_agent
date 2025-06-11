import os

def write_file(working_directory, file_path, content):
    working_path = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_path, file_path))

    if file_path.startswith(working_path + os.sep) is False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        directory = os.path.dirname(file_path)
        if directory:  # Only if there's actually a directory to create
            os.makedirs(directory, exist_ok=True)
        
        with open(file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"