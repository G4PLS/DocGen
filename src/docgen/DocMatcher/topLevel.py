from . import DocElement, DocTag, DocBlock, DocMatcher

class DocTopLevel(DocElement):
    TYPE: str = "TOPLEVEL"
    ELEMENT_TYPE: str = "TOPLEVEL"
    NAME: str = "undefined"
    ALLOWED_TAGS: list[type[DocTag]] = None
    ALLOWED_BLOCKS: list[type[DocBlock]] = None

    def __init__(self, name: str):
        super().__init__()

        self.top_level_name: str = name
        self._elements: list[DocTag] = []
        self._blocks: list[DocBlock] = []

    def add_element(self, element: DocTag):
        if self.ALLOWED_TAGS is not None and not any(isinstance(element, tag) for tag in self.ALLOWED_TAGS):
            return

        self._elements.append(element)

    def add_block(self, element: DocBlock):
        if self.ALLOWED_BLOCKS is not None and not any(isinstance(element, block) for block in self.ALLOWED_BLOCKS):
            return

        self._blocks.append(element)

    def json(self):
        data = super().json()

        data["name"] = self.top_level_name
        data["elements"] = [element.json() for element in self._elements]
        data["blocks"] = [element.json() for element in self._blocks]

        return data

_top_levels: dict[tuple[str, str], "DocTopLevel"] = {}
_registry: dict[str, type["DocTopLevel"]] = {}
_matcher: DocMatcher[DocTopLevel] = None

def init(allowed_top_levels: list[DocTopLevel]):
    global _matcher
    _matcher = DocMatcher[DocTopLevel](allowed_top_levels)

def get(header: tuple[str, str], *args, **kwargs):
    top_level = _top_levels.get(header)

    if top_level:
        return top_level

    top_level = _matcher.get(header[0], DocTopLevel, header[1], *args, **kwargs)

    if top_level:
        _top_levels[header] = top_level
        return top_level

    top_level = DocTopLevel("undefined")
    _top_levels[header] = top_level

    return top_level

def print_all():
    all_data = [top_level.json() for top_level in _top_levels.values()]

    print(all_data)