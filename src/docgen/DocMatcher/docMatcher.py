from abc import ABC, abstractmethod

class DocElement(ABC):
    TYPE: str = "ELEMENT"
    ELEMENT_TYPE: str = "undefined"
    NAME: str = "undefined"

    def __init__(self):
        super().__init__()

    def json(self):
        return {
            "type": self.TYPE,
            "element-type": self.ELEMENT_TYPE,
            "element-name": self.NAME,
        }

class DocMatcher[T: DocElement]:
    def __init__(self, allowed: list[type[T]]):
        self._registry: dict[str, type[T]] = {entry.NAME: entry for entry in allowed}
    
    def get(self, registry_key: str, fallback: type[T], *args, **kwargs) -> T:
        cls: type[T] = self._registry.get(registry_key)

        if cls is not None:
            return cls(*args, **kwargs)

        if fallback is not None:
            return fallback(*args, **kwargs)

        raise KeyError(f"No DocElement registered under key {registry_key}")