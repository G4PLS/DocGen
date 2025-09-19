import pytest

from docgen.language import Language
from docgen.fileParser import FileParser

class DummyLanguage(Language):
    NAME: str = "dummy"
    FILE_EXTENSION: str = ".dummy"
    COMMENT_STYLE_REGEX: str = r"-{2,}"  # matches -- or more
    SINGLE_COMMENT_CHAR: str = '-'
    BLOCK_START_REGEX: str = r"-{3,}"  # -{3,} # matches --- (block start)
    BLOCK_END_REGEX: str = r"-{3,}"
    PARAM_REGEX: str = r"-{2,}\@"


@pytest.fixture
def fileparser():
    fp = FileParser()
    fp.current_language = DummyLanguage
    return fp

def test_pre_parse_line_param(fileparser):
    test_line = "--@param test"
    assert fileparser.pre_parse_line(test_line) == ("param", "test")

    test_line = "--@param"
    assert fileparser.pre_parse_line(test_line) == ("param", "")

def test_pre_parse_line_block(fileparser):
    test_line = "---@block test"
    assert fileparser.pre_parse_line(test_line) == ("block", "test")

    test_line = "---@block"
    assert fileparser.pre_parse_line(test_line) == ("block", "")

def test_pre_parse_line_invalid_line(fileparser):
    test_line = "-@param test"
    assert fileparser.pre_parse_line(test_line) is None

    test_line = "--# test"
    assert fileparser.pre_parse_line(test_line) is None