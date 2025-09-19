import importlib
import pkgutil
from functools import lru_cache

from .DocMatcher import DocBlock, DocTag, DocTopLevel
import os
import inspect

class Language:
    NAME: str
    FILE_EXTENSION: str
    COMMENT_STYLE_REGEX: str
    SINGLE_COMMENT_CHAR: chr
    BLOCK_START_REGEX: str
    BLOCK_END_REGEX: str
    PARAM_REGEX: str
    BLOCKS: list[type["DocBlock"]]
    TAGS: list[type["DocTag"]]
    TOP_LEVELS: list[type["DocTopLevel"]]

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

    @classmethod
    def discover_components(cls):
        """
        Automatically discover DocTag, DocBlock, and DocTopLevel
        classes in the language's submodules (tags, blocks, top_levels)
        and populate cls.TAGS, cls.BLOCKS, cls.TOP_LEVELS.
        """
        # Determine the package where the class lives, e.g., "langs.lua"
        package_name = cls.__module__.rsplit(".", 1)[0]
        package = importlib.import_module(package_name)

        tags, blocks, tops = [], [], []

        # Iterate over submodules in the language package
        for _, submodule_name, _ in pkgutil.iter_modules(package.__path__):
            submod = importlib.import_module(f"{package_name}.{submodule_name}")

            # Inspect all classes in the submodule
            for _, obj in inspect.getmembers(submod, inspect.isclass):
                if issubclass(obj, DocTag) and obj is not DocTag:
                    tags.append(obj)
                elif issubclass(obj, DocBlock) and obj is not DocBlock:
                    blocks.append(obj)
                elif issubclass(obj, DocTopLevel) and obj is not DocTopLevel:
                    tops.append(obj)

        cls.TAGS = tags
        cls.BLOCKS = blocks
        cls.TOP_LEVELS = tops
