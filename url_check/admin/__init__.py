from importlib import import_module
from pathlib import Path
from typing import Any, cast

from django.contrib import admin
from django.contrib.admin.exceptions import AlreadyRegistered
from django.db.models.base import ModelBase, Model

from .. import models


def register_modules() -> None:
    admin_modules = list(Path(__file__).parent.glob("*admin.py"))

    for item in admin_modules:
        name: str = item.name.replace(".py", "")
        module_prefix: str = ".".join(item.parts[2:-1])
        module: str = f"{module_prefix}.{name}"
        import_module(module)


def register_models() -> None:
    for item in dir(models):
        model: type[Model] = getattr(models, item)
        if not isinstance(model, ModelBase): continue
        if model._meta.abstract: continue

        try: admin.site.register(model)
        except AlreadyRegistered: pass


register_modules()
register_models()
