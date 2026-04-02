import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs Python files in a specified path relative to the working directory, with a specified timeout, providing the output of the executed file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to Python file to be executed, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the Python file",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if (
            not target_file.startswith(working_dir_abs + os.sep)
            and target_file != working_dir_abs
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs
        )
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}\n{result.stderr}"
        if not result.stdout and not result.stderr:
            return "No output produced"
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error: {e}"
