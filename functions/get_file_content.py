import os

from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file content in a specified path relative to the working directory with a set character limit",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to read content from, relative to the working directory",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if (
            not target_file.startswith(working_dir_abs + os.sep)
            and target_file != working_dir_abs
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: {e}"
