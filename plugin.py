import os
import sublime
import sys
import shutil

# Clear module cache to force reloading all modules of this package.

# kiss-reloader:
prefix = __package__ + "."  # don't clear the base package
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]
prefix = None

from .unittesting.color_scheme import UnitTestingColorSchemeCommand
from .unittesting.syntax import UnitTestingSyntaxCommand
from .unittesting.syntax import UnitTestingSyntaxCompatibilityCommand
from .unittesting.unit import UnitTestingCommand


__all__ = [
    "UnitTestingCommand",
    "UnitTestingSyntaxCommand",
    "UnitTestingSyntaxCompatibilityCommand",
    "UnitTestingColorSchemeCommand",
    "plugin_loaded",
    "plugin_unloaded",
]

# publish unittesting module
sys.modules["unittesting"] = sys.modules["UnitTesting"].unittesting

UT33_CODE = """
from UnitTesting import plugin as ut38


class UnitTesting33Command(ut38.UnitTestingCommand):
    \"\"\"Execute unit tests for python 3.3 plugins.\"\"\"
    pass
"""


def plugin_loaded():
    if sys.version_info >= (3, 8):
        import json

        UT33 = os.path.join(sublime.packages_path(), "UnitTesting33")
        os.makedirs(UT33, exist_ok=True)

        try:
            try:
                with open(os.path.join(UT33, "plugin.py"), "x") as f:
                    f.write(UT33_CODE)
            except FileExistsError:
                pass

            try:
                with open(os.path.join(UT33, "dependencies.json"), "x") as f:
                    f.write(json.dumps({"*": {">3000": ["coverage"]}}))
            except FileExistsError:
                pass

            try:
                # hide from Package Control quick panels
                open(os.path.join(UT33, ".hidden-sublime-package"), "x").close()
            except FileExistsError:
                pass

        except OSError as e:
            print("UnitTesting: Error while creating python 3.3 module, since", str(e))


def plugin_unloaded():
    if sys.version_info >= (3, 8):
        UT33 = os.path.join(sublime.packages_path(), "UnitTesting33")
        try:
            shutil.rmtree(UT33)
        except Exception:
            pass
