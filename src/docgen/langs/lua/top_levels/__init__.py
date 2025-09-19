import importlib
import pkgutil
from docgen.DocMatcher import DocTag

_TOP_LEVELS = []

for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    if is_pkg:
        continue  # skip subfolders
    module = importlib.import_module(f"{__name__}.{name}")
    for obj in module.__dict__.values():
        if isinstance(obj, type) and issubclass(obj, DocTag) and obj is not DocTag:
            _TOP_LEVELS.append(obj)

_TOP_LEVELS = list(dict.fromkeys(_TOP_LEVELS))

# expose all tag classes at package level
globals().update({cls.__name__: cls for cls in _TOP_LEVELS})
__all__ = [cls.__name__ for cls in _TOP_LEVELS]