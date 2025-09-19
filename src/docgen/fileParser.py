import re

from .language import Language
from .DocMatcher import *
from dataclasses import dataclass, field

from docgen.DocMatcher.topLevel import init, get, DocTopLevel, print_all

@dataclass
class Block:
    START_INDEX: int
    END_INDEX: int

    HEADER: tuple[str,str] = None
    CONTENT: list[tuple[str, str]] = field(default_factory=list)

class FileParser:
    def __init__(self):
        self.blocks: list[DocBlock] = []

        self.current_file_path: str = ""
        self.current_lines: list[str] = []
        self.current_language: Language

    def parse_file(self, path: str, language: type[Language]):
        self.current_file_path = path
        self.current_language = language
        
        self.current_lines: list[str] = []
        with open(path, "r", encoding="utf-8") as file:
            self.current_lines = [line.strip() for line in file]

        blocks = self.extract_blocks(self.current_lines)
        self.parse_blocks(blocks)

    def extract_blocks(self, lines: list[str]) -> list[Block]:
        blocks: list[Block] = []
        current_block: Block = None

        for i, line in enumerate(lines):
            line_content = self.pre_parse_line(line)

            if current_block and re.match(self.current_language.BLOCK_END_REGEX, line):
                current_block.END_INDEX = i
                blocks.append(current_block)
                current_block = None
            elif not current_block and re.match(self.current_language.BLOCK_START_REGEX, line):
                current_block = Block(i, i)
                current_block.HEADER = line_content
            elif current_block and line_content:
                current_block.CONTENT.append(line_content)

        return blocks

    def parse_blocks(self, blocks: list[Block]) -> None:
        block_matcher = DocMatcher[DocBlock](self.current_language.BLOCKS)
        tag_matcher = DocMatcher[DocTag](self.current_language.TAGS)
        init(self.current_language.TOP_LEVELS)

        doc_blocks: list[DocBlock] = []
        top_level: DocTopLevel = None

        # Todo: If block is toplevel add elements to toplevel
        for block in blocks:
            if block.START_INDEX == 0:
                top_level = get(block.HEADER)
                continue
            elif top_level is None:
                top_level = get(("", ""))

            current_block = block_matcher.get(block.HEADER[0], DocBlock, block.HEADER[1])

            for name, content in block.CONTENT:
                tag = tag_matcher.get(name, DocTag, self.current_file_path, content)
                current_block.add_element(tag)

            if top_level:
                top_level.add_block(current_block)
            doc_blocks.append(current_block)

    def pre_parse_line(self, line: str):
        match = re.match(self.current_language.PARAM_REGEX, line)

        if not match:
            return None
        
        content = line[match.end():].strip()
        parts = content.split(maxsplit=1)

        name = parts[0]
        data = parts[1] if len(parts) > 1 else ""

        return name, data