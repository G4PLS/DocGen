from abc import abstractmethod
from .docMatcher import DocElement

class DocTag(DocElement):
    TYPE: str = "TAG"
    ELEMENT_TYPE: str = "undefined"
    NAME: str = "undefined"

    def __init__(self, file_path: str, data: str):
        super().__init__()
        self.file_path = file_path
        self.__data = {}
        self.parse_data(data)

    def json(self):
        data = super().json()

        data["data"] = self.__data
        return data

    def parse_data(self, data: str):
        self.__data = data

#############
# Base Tags #
#############

class TextDocTag(DocTag):
    ELEMENT_TYPE: str = "TEXT"
    NAME: str

    def __init__(self, file_path, data):
        self.text: str = ""

        super().__init__(file_path, data)

    def json(self):
        data = super().json()

        data["text"] = self.text

        return data

    def parse_data(self, data):
        super().parse_data(data)
        self.text = data
    
class MarkerDocTag(DocTag):
    ELEMENT_TYPE: str = "MARKER"
    NAME: str

    def __init__(self, file_path, data):
        super().__init__(file_path, data)

    def json(self):
        return super().json()

    def parse_data(self, data):
        super().parse_data(data)
        return super().parse_data(data)
    
class ParameterDocTag(DocTag):
    ELEMENT_TYPE: str = "PARAMETER"
    NAME: str
    SPLIT: int

    def __init__(self, file_path, data):
        super().__init__(file_path, data)

    @abstractmethod
    def json(self):
        return super().json()

    @abstractmethod
    def parse_data(self, data):
        super().parse_data(data)

    def split_data(self, data: str):
        parts = data.split(maxsplit=self.SPLIT)

        if len(parts) < self.SPLIT:
            raise ValueError(f"Invalid param line: {data}")

        return parts
    
class StateDocTag(DocTag):
    ELEMENT_TYPE: str = "STATE"
    NAME: str
    STATES: list[str]

    def __init__(self, file_path, data):
        self.state: str|None = None

        super().__init__(file_path, data)

    def json(self):
        data = super().json()

        data["state"] = self.state

        return data

    def parse_data(self, data):
        super().parse_data(data)
        if data in self.STATES:
            self.state = data

class ValueDocTag(ParameterDocTag):
    ELEMENT_TYPE: str = "VALUE"
    NAME: str
    SPLIT: int = 2

    def __init__(self, file_path, data):
        self.type: str = "unknown"
        self.value: str|None = None

        super().__init__(file_path, data)

    def json(self):
        data = super().json()

        data["value-type"] = self.type
        data["value"] = self.value

        return data

    def parse_data(self, data: str):
        super().parse_data(data)
        parts = self.split_data(data)

        self.type = parts[0]
        self.value = parts[1]

class ListDocTag(DocTag):
    ELEMENT_TYPE: str = "LIST"
    NAME: str
    
    def __init__(self, file_path, data):
        self.list: list[str] = []

        super().__init__(file_path, data)

    def json(self):
        data = super().json()

        data["list"] = self.list

        return data

    def parse_data(self, data: str):
        super().parse_data(data)
        self.list = data.split()

class NameDocTag(DocTag):
    ELEMENT_TYPE: str = "NAME"
    NAME: str

    def __init__(self, file_path, data):
        self.name: str = None

        super().__init__(file_path, data)

    def json(self):
        data = super().json()

        data["name"] = self.name

        return data

    def parse_data(self, data):
        super().parse_data(data)
        parts = data.split(maxsplit=1)

        self.name = parts[0]