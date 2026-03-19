import os

from functions.write_file import write_file

if __name__ == "__main__":
    tests = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
    ]

    for working_directory, file_path, content in tests:
        print(f"Result for '{file_path}':")
        result = write_file(working_directory, file_path, content)
        for line in result.splitlines():
            print(f"  {line}")
        print()
