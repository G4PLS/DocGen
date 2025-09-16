import importlib
import pkgutil
from DocMatcher import DocTag

_TAGS = []

for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    if is_pkg:
        continue  # skip subfolders
    module = importlib.import_module(f"{__name__}.{name}")
    for obj in module.__dict__.values():
        if isinstance(obj, type) and issubclass(obj, DocTag) and obj is not DocTag:
            _TAGS.append(obj)

_TAGS = list(dict.fromkeys(_TAGS))

# expose all tag classes at package level
globals().update({cls.__name__: cls for cls in _TAGS})
__all__ = [cls.__name__ for cls in _TAGS]