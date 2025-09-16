from abc import ABC, abstractmethod

class DocElement(ABC):
    NAME: str

    def __init__(self):
        super().__init__()

    @abstractmethod
    def json(self):
        pass

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