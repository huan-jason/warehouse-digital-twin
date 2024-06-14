from importlib import import_module
from pathlib import Path


admins = list(Path(__file__).parent.glob("*admin.py"))

for item in admins:
    name: str = item.name.replace(".py", "")
    module_prefix: str = ".".join(item.parts[2:-1])
    module: str = f"{module_prefix}.{name}"
    import_module(module)
