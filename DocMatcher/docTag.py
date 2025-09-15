from abc import abstractmethod
from .docMatcher import DocElement
from typing import TypeVar, Generic

T = TypeVar("T", bound="ValueDocTag")

class DocTag(DocElement):
    NAME: str = "undefined"

    def __init__(self, file_path: str, line_number: int, data: str):
        super().__init__()
        self.file_path = file_path
        self.line_number = line_number
        self.parse_data(data)

    @abstractmethod
    def json(self):
        pass

    @abstractmethod
    def parse_data(self, data: str):
        pass

#
#
#

class TextDocTag(DocTag):
    TYPE: str = "TEXT"
    NAME: str

    def __init__(self, file_path, line_number, data):
        self.text: str = None

        super().__init__(file_path, line_number, data)

    def json(self):
        return {
            "type": self.TYPE,
            "tag-type": self.NAME,
            "text": self.text
        }

    def parse_data(self, data):
        self.text = data
    
class MarkerDocTag(DocTag):
    TYPE: str = "MARKER"
    NAME: str

    def __init__(self, file_path, line_number, data):
        super().__init__(file_path, line_number, data)

    def json(self):
        return {
            "type": self.TYPE,
            "tag-type": self.NAME
        }

    def parse_data(self, data):
        return super().parse_data(data)
    
class ParameterDocTag(DocTag):
    TYPE: str = "PARAMETER"
    NAME: str
    SPLIT: int

    def __init__(self, file_path, line_number, data):
        super().__init__(file_path, line_number, data)

    @abstractmethod
    def json(self):
        pass

    @abstractmethod
    def parse_data(self, data):
        pass

    def split_data(self, data: str):
        parts = data.split(maxsplit=self.SPLIT)

        if len(parts) < self.SPLIT:
            raise ValueError(f"Invalid param line: {data}")

        return parts
    
class StateDocTag(DocTag):
    TYPE: str = "STATE"
    NAME: str
    STATES: list[str]

    def __init__(self, file_path, line_number, data):
        self.state: str = None

        super().__init__(file_path, line_number, data)

    def json(self):
        return {
            "type": self.TYPE,
            "tag-type": self.NAME,
            "state": self.state
        }

    def parse_data(self, data):
        if data in self.STATES:
            self.state = data

class ValueDocTag(ParameterDocTag):
    TYPE: str = "VALUE"
    NAME: str
    SPLIT: int = 2

    def __init__(self, file_path, line_number, data):
        self.type: str
        self.value: str

        super().__init__(file_path, line_number, data)

    def json(self):
        return {
            "type": self.TYPE,
            "tag-type": self.NAME,
            "value-type": self.type,
            "value": self.value
        }

    def parse_data(self, data: str):
        parts = self.split_data(data)

        self.type = parts[0]
        self.value = parts[1]

class ListDocTag(DocTag):
    TYPE: str = "LIST"
    NAME: str
    
    def __init__(self, file_path, line_number, data):
        self.list: list[str]

        super().__init__(file_path, line_number, data)

    def json(self):
        return {
            "type": self.TYPE,
            "tag-type": self.NAME,
            "list": self.list
        }

    def parse_data(self, data: str):
        self.list = data.split()

class NameDocTag(DocTag):
    TYPE: str = "NAME"
    NAME: str

    def __init__(self, file_path, line_number, data):
        self.name: str = None

        super().__init__(file_path, line_number, data)

    def json(self):
        return {
            "type": self.TYPE,
            "tag-type": self.NAME,
            "name": self.name
        }

    def parse_data(self, data):
        parts = data.split(maxsplit=1)

        self.name = parts[0]