from language import Language
from DocMatcher import DocTag, DocBlock
from .tags import *
from .blocks import *

_tag_classes = [cls for cls in globals().values() if isinstance(cls, type) and issubclass(cls, DocTag) and cls is not DocTag]
_block_classes = [cls for cls in globals().values() if isinstance(cls, type) and issubclass(cls, DocBlock) and cls is not DocBlock]

class Lua(Language):
    NAME: str = "Lua"
    FILE_EXTENSION: str = ".lua"
    COMMENT_STYLE_REGEX: str = r"-{2,}" # matches -- or more
    SINGLE_COMMENT_CHAR: str = '-'
    BLOCK_START_REGEX: str = r"-{3,}" #-{3,} # matches --- (block start)
    BLOCK_END_REGEX: str = r"-{3,}"
    PARAM_REGEX: str = r"-{2,}\@"
    ALLOWED_BLOCKS: list[type["DocBlock"]] = []
    ALLOWED_TAGS: list[type["DocTag"]] = []

Lua.ALLOWED_BLOCKS = _block_classes
Lua.ALLOWED_TAGS = _tag_classes