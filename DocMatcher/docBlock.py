from .docMatcher import DocElement
from .docTag import DocTag

class DocBlock(DocElement):
    NAME: str
    ALLOWED_TAGS: list[type[DocTag]] = None

    def __init__(self, name: str):
        super().__init__()

        print("CREATED", name)

        self.block_name: str = name
        self._elements: list[DocTag] = []

    def add_element(self, element: DocTag):
        if self.ALLOWED_TAGS is not None and not any(isinstance(element, tag) for tag in self.ALLOWED_TAGS):
            return

        self._elements.append(element)

    def json(self):
        return {
            "type": self.NAME,
            "name": self.block_name,
            "elements": [element.json() for element in self._elements]
        }