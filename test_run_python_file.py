import os

from functions.run_python_file import run_python_file

if __name__ == "__main__":
    tests = [
        ("calculator", "main.py", None),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py", None),
        ("calculator", "../main.py", None),
        ("calculator", "nonexistent.py", None),
        ("calculator", "lorem.txt", None),
    ]

    for working_directory, file_path, args in tests:
        print(f"Result for '{file_path}':")
        result = run_python_file(working_directory, file_path, args)
        for line in result.splitlines():
            print(f"  {line}")
        print()
