import os

"""
This script automates the process of formatting and linting Python code using popular tools.

It provides two tasks:
1. Formatting: Uses `black` to automatically format the code according to the PEP 8 style guide.
2. Linting: Uses `flake8` to check the code for style violations and errors.

Usage:
    python script_name.py format   # Formats the code using black and isort
    python script_name.py lint     # Lints the code using flake8

Functions:
    - format_code(): Runs the `black` and `isort` commands to format and sort imports in the code.
    - lint_code(): Runs the `flake8` command to lint the code and report style violations or errors.

Command-Line Arguments:
    task (str): Specifies the task to run. It can be either 'format' to format the code or 'lint' to lint the code.
    
"""


def format_code():
    os.system("black .")
    os.system("isort .")


def lint_code():
    os.system("flake8 .")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("task", choices=["format", "lint"], help="Task to run")
    args = parser.parse_args()

    if args.task == "format":
        format_code()
    elif args.task == "lint":
        lint_code()
