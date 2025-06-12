import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
model_name = "gemini-2.0-flash-001"
client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
2
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a file's content limited to the first 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get contents of, relative to the working directory",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file contatining a function, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute relative to the working path. Returns STDOUT, STDERR and any returncode that is not equal to 0. Will return a message if no output is produced",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file and if needed create the file and any directory structure, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to be written to, if it does not exist creates the file and any needed directories in the working path",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content of the file to be writeen in the destination file_path.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


if len(sys.argv) < 2:
    print("A prompt must be provided")
    sys.exit(1)

user_prompt = sys.argv[1]  

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

response = client.models.generate_content(model=model_name, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
function_calls = response.function_calls

function_results = []

if function_calls:
    for function in function_calls:
        if sys.argv[2] == "--verbose":
            function_response = call_function(function, verbose=True)
        else:
            function_response = call_function(function)
        
        if not function_response.parts[0].function_response.response:
            raise Exception("Error: The function returned no ouput")
        elif sys.argv[2] == "--verbose":
            print(f"-> {function_response.parts[0].function_response.response["result"]}")
        else:
            function_results.append(function_response)
else:    
    print(response.text)
prompt_usage = response.usage_metadata.prompt_token_count
response_usage = response.usage_metadata.candidates_token_count
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_usage}")
    print(f"Response tokens: {response_usage}")





