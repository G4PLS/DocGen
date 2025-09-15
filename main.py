import os
from pathlib import Path
from fileParser import FileParser

def main():
    fp = FileParser()

    for path in Path("./Test").rglob("*"):  # recursive glob
        if path.is_file():
            fp.parse_file(path)
        elif path.is_dir():
            print("Dir:", path)


if __name__ == "__main__":
    main()
