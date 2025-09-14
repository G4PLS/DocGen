from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T", bound="DocElement")

class DocMatcher(Generic[T]):
    def __init__(self, allowed: list[type[T]]):
        self._registry: dict[str, type[T]] = {entry.NAME: entry for entry in allowed}
    
    def get(self, registry_key: str, *args, **kwargs):
        cls = self._registry.get(registry_key)

        if not cls:
            return None
        
        return cls(*args, **kwargs)
    
class DocElement(ABC):
    NAME: str

    def __init__(self):
        super().__init__()

    @abstractmethod
    def json(self):
        pass

class DocBlock(DocElement, Generic[T]):
    NAME: str

    def __init__(self, name: str):
        super().__init__()

        print("CREATED", name)

        self.block_name: str = name
        self._elements: list[T] = []

    def add_element(self, element: T):
        self._elements.append(element)

    def json(self):
        return {
            "type": self.NAME,
            "name": self.block_name,
            "elements": [element.json() for element in self._elements]
        }

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