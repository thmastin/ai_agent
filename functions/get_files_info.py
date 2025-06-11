import os

def get_files_info(working_directory, directory=None):
    working_path = os.path.abspath(working_directory)
    if directory is None:
        directory_path = working_path
    elif os.path.isabs(directory):
        directory_path = directory
    else:
        directory_path = os.path.abspath(os.path.join(working_path, directory))

    if directory_path != working_path and not directory_path.startswith(working_path + os.sep):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(directory_path) is False:
        return f'Error: "{directory}" is not a directory'
    try:
        files = os.listdir(directory_path)
        output = []
        for file in files:
            file_path = os.path.join(directory_path, file)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            output.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
    except Exception as e: 
            return f"Error: {str(e)}"
    
    return "\n".join(output)