from functions.get_file_content import get_file_content

if __name__ == "__main__":
    tests = [
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py"),
    ]
    for working_directory, file_path in tests:
        print(f"Result for '{file_path}':")
        result = get_file_content(working_directory, file_path)
        for line in result.splitlines():
            print(f"  {line}")
        print()
