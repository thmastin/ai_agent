import os
import subprocess

def run_python_file(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    full_file_path = os.path.abspath(os.path.join(working_path, file_path))

    if full_file_path.startswith(working_path + os.sep) is False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_file_path):
        return f'Error: File "{file_path}" not found.'
    if not full_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python", file_path], timeout=30, capture_output=True, cwd=working_path)
        output = []
        output.append(f"STDOUT: {result.stdout.decode()}")
        output.append(f"STDERR: {result.stderr.decode()}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout.decode().strip() and not result.stderr.decode().strip() and result.returncode == 0:
            return "No output produced."
        else:
            return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"