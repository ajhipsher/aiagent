import os

from functions.get_files_info import get_files_info

if __name__ == "__main__":
    tests = [
        (".", "Result for current directory:"),
        ("pkg", "Result for 'pkg' directory:"),
        ("/bin", "Result for '/bin' directory:"),
        ("../", "Result for '../' directory:"),
    ]

    for directory, label in tests:
        print(label)
        result = get_files_info("calculator", directory)
        for line in result.splitlines():
            print(f"  {line}")
        print()
