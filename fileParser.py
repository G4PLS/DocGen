import re

from Language import *
from DocMatcher import *

class FileParser:
    @staticmethod
    def parse_file(path: str):
        language: Language = LanguageMatcher.get_language_for_file(path)

        if not language:
            return
        
        print("PARSING", path)
        
        lines: list[str] = []
        with open(path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file]

        FileParser.parse_lines(lines, language, path)

    @staticmethod
    def parse_lines(lines: list[str], language: Language, path: str):
        block_matcher = DocMatcher(language.ALLOWED_BLOCKS)
        tag_matcher = DocMatcher(language.ALLOWED_TAGS)

        in_block = False
        block: DocBlock | None = None

        for i in range(len(lines)):
            line = lines[i]

            # Detect end of a doc block
            if in_block and re.match(language.BLOCK_END_REGEX, line):
                if block:
                    print(block.json())
                in_block = False
                block = None
                continue

            # Parses the line for the Doc Content (Tags)
            parsed = FileParser.pre_parse_line(line, language)
            if parsed is None:
                continue

            name, content = parsed

            # Detect start of a doc block
            if not in_block and re.match(language.BLOCK_START_REGEX, line):
                in_block = True

                block = block_matcher.get(name, content)
                continue

            # Detect if in doc block and if we should add content
            if in_block and block:
                tag: DocTag = tag_matcher.get(name, path, i, content)

                if not tag or not block:
                    continue

                block.add_element(tag)

    @staticmethod
    def pre_parse_line(line: str, language: Language) -> tuple[str, str] | None:
        match = re.match(language.PARAM_REGEX, line)

        if not match:
            return None
        
        content = line[match.end():].strip()
        parts = content.split(maxsplit=1)

        name = parts[0]
        data = parts[1] if len(parts) > 1 else ""

        return name, data