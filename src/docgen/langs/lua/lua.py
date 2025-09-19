from docgen.language import Language

class Lua(Language):
    NAME: str = "Lua"
    FILE_EXTENSION: str = ".lua"
    COMMENT_STYLE_REGEX: str = r"-{2,}" # matches -- or more
    SINGLE_COMMENT_CHAR: str = '-'
    BLOCK_START_REGEX: str = r"-{3,}" #-{3,} # matches --- (block start)
    BLOCK_END_REGEX: str = r"-{3,}"
    PARAM_REGEX: str = r"-{2,}\@"