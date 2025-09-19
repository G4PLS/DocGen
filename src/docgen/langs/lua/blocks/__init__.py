import importlib
import pkgutil
from docgen.DocMatcher.docBlock import DocBlock

_BLOCKS = []

for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    if is_pkg:
        continue  # skip subfolders
    module = importlib.import_module(f"{__name__}.{name}")
    for obj in module.__dict__.values():
        if isinstance(obj, type) and issubclass(obj, DocBlock) and obj is not DocBlock:
            _BLOCKS.append(obj)

_BLOCKS = list(dict.fromkeys(_BLOCKS))

# expose all tag classes at package level
globals().update({cls.__name__: cls for cls in _BLOCKS})
__all__ = [cls.__name__ for cls in _BLOCKS]