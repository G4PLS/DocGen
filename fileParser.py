import re

from language import Language
from DocMatcher import *

class FileParser:
    def __init__(self):
        self.blocks: list[DocBlock] = []

        self.current_language: Language|None = None
        self.current_file_path: str = ""
        self.current_lines: list[str] = []

    def parse_file(self, path: str, language: type[Language]):
        self.current_file_path = path
        self.current_language = language
        
        self.current_lines: list[str] = []
        with open(path, "r", encoding="utf-8") as file:
            self.current_lines = [line.strip() for line in file]

        self.parse_lines()

    def parse_lines(self):
        i = 0
        while i < len(self.current_lines):
            line = self.current_lines[i]

            if re.match(self.current_language.BLOCK_START_REGEX, line):
                i, data = self.parse_block(i)
                if data:
                    print(data.json())
            else:
                i += 1

    def parse_block(self, start_index: int):
        block_matcher = DocMatcher[DocBlock](self.current_language.ALLOWED_BLOCKS)
        tag_matcher = DocMatcher[DocTag](self.current_language.ALLOWED_TAGS)

        block = None

        for i in range(start_index, len(self.current_lines)):
            raw_line = self.current_lines[i]

            # Start of Block
            if block is None and re.match(self.current_language.BLOCK_START_REGEX, raw_line):
                name, content = self.pre_parse_line(raw_line)
                block = block_matcher.get(name, DocBlock, content)
                continue

            # End of Block
            if block and re.match(self.current_language.BLOCK_END_REGEX, raw_line):
                return i+1, block

            # Inside block
            parsed = self.pre_parse_line(raw_line)
            if parsed and block:
                name, content = parsed
                tag = tag_matcher.get(name, DocTag, self.current_file_path, i, content)
                if tag:
                    block.add_element(tag)

        return start_index+1, None

    def pre_parse_line(self, line: str):
        match = re.match(self.current_language.PARAM_REGEX, line)

        if not match:
            return None
        
        content = line[match.end():].strip()
        parts = content.split(maxsplit=1)

        name = parts[0]
        data = parts[1] if len(parts) > 1 else ""

        return name, data