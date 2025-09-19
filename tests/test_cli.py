import pytest
from unittest.mock import MagicMock, mock_open, patch
from docgen.fileParser import FileParser, Block, Language

# Dummy Language class for testing
class DummyLanguage(Language):
    NAME = "dummy"
    BLOCK_START_REGEX = r'^START'
    BLOCK_END_REGEX = r'^END'
    PARAM_REGEX = r'^\*'
    BLOCKS = {}
    TAGS = {}
    TOP_LEVELS = {}

@pytest.fixture
def parser():
    return FileParser()

def test_pre_parse_line(parser):
    parser.current_language = DummyLanguage()

    line = "* name data"
    assert parser.pre_parse_line(line) == ("name", "data")

    line = "* singleword"
    assert parser.pre_parse_line(line) == ("singleword", "")

    line = "no match"
    assert parser.pre_parse_line(line) is None