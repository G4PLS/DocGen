import importlib
import pkgutil

IGNORE = {"tags", "blocks", "top_levels"}  # subpackages to skip

# Loop through all submodules/subpackages of langs
for loader, name, is_pkg in pkgutil.iter_modules(__path__):
    if name in IGNORE:
        continue  # skip folders like tags/ and blocks/
    
    # Import the module/package
    importlib.import_module(f"{__name__}.{name}")