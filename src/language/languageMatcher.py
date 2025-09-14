import os

from src.language.language import Language
from src.langs import *

class LanguageMatcher:
    _LANGUAGES: dict[str, type[Language]] = {}

    @staticmethod
    def get_languages() -> dict[str, type[Language]]:
        if not LanguageMatcher._LANGUAGES:
            # Build dictionary lazily
            LanguageMatcher._LANGUAGES = {
                lang.FILE_EXTENSION: lang
                for lang in Language.__subclasses__()
            }
        return LanguageMatcher._LANGUAGES

    @staticmethod
    def get_language_for_file(path: str) -> type[Language] | None:
        _, ext = os.path.splitext(path)
        return LanguageMatcher.get_languages().get(ext)