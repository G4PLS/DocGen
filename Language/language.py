from DocMatcher import DocBlock, DocTag

class Language:
    NAME: str
    FILE_EXTENSION: str
    COMMENT_STYLE_REGEX: str
    SINGLE_COMMENT_CHAR: chr
    BLOCK_START_REGEX: str
    BLOCK_END_REGEX: str
    PARAM_REGEX: str
    ALLOWED_BLOCKS: list[type["DocBlock"]]
    ALLOWED_TAGS: list[type["DocTag"]]