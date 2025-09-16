from functools import lru_cache

from DocMatcher import DocBlock, DocTag
import os

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

    @classmethod
    def all_languages(cls) -> dict[str, type["Language"]]:
        return {subclass.NAME.lower(): subclass for subclass in Language.__subclasses__()}

    @classmethod
    @lru_cache(maxsize=None)
    def all_language_extensions(cls) -> dict[str, type["Language"]]:
        return {subclass.FILE_EXTENSION.lower(): subclass for subclass in Language.__subclasses__()}

    @staticmethod
    def get_language_for_file(path: str) -> type["Language"] | None:
        _, ext = os.path.splitext(path)
        ext = ext.lower()

        return Language.all_language_extensions().get(ext)