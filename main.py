import os
from pathlib import Path
from src.fileParser import FileParser

def main():
    print("H EYHEY")
    for path in Path("./Test").rglob("*"):  # recursive glob
        if path.is_file():
            FileParser.parse_file(path)
        elif path.is_dir():
            print("Dir:", path)


if __name__ == "__main__":
    main()
