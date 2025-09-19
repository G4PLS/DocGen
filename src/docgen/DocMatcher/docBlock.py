from .docMatcher import DocElement
from .docTag import DocTag

class DocBlock(DocElement):
    TYPE: str = "BLOCK"
    ELEMENT_TYPE: str = "BLOCK"
    NAME: str = "undefined"
    ALLOWED_TAGS: list[type[DocTag]] = None

    def __init__(self, name: str):
        super().__init__()

        self.block_name: str = name
        self._elements: list[DocTag] = []

    def add_element(self, element: DocTag):
        if self.ALLOWED_TAGS is not None and not any(isinstance(element, tag) for tag in self.ALLOWED_TAGS):
            return

        self._elements.append(element)

    def json(self):
        data = super().json()

        data["name"] = self.block_name
        data["elements"] = [element.json() for element in self._elements]

        return data