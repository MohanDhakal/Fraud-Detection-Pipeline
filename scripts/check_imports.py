import importlib
import pathlib
import sys

SRC = pathlib.Path("src")

sys.path.insert(0, str(SRC.resolve()))

failed = False

for file in SRC.rglob("*.py"):
    if file.name == "__init__.py":
        continue

    relative = file.relative_to(SRC).with_suffix("")
    module = ".".join(relative.parts)

    try:
        importlib.import_module(module)
        print(f"OK   {module}")
    except Exception as e:
        failed = True
        print(f"FAIL {module}: {type(e).__name__}: {e}")

if failed:
    sys.exit(1)
