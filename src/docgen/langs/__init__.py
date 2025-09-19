import importlib
import pkgutil

from docgen.language import Language

IGNORE = {"tags", "blocks", "top_levels"}  # subpackages to skip

for _, name, is_pkg in pkgutil.iter_modules(__path__):
    if name in IGNORE:
        continue  # skip internal folders

    # Import the language package/module
    module = importlib.import_module(f"{__name__}.{name}")

    # Find all Language subclasses in this module and call discover_components
    for subclass in Language.__subclasses__():
        if subclass.__module__.startswith(f"{__name__}.{name}"):
            subclass.discover_components()
