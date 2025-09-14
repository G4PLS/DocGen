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