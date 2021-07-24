from typing import Optional

import pluggy

from bloglang import ast
from bloglang.plugin import __default, __stub, stdlib

manager = pluggy.PluginManager("bloglang.plugin")
manager.add_hookspecs(__stub)
manager.load_setuptools_entrypoints("bloglang.plugin")
manager.register(stdlib)
manager.register(__default)
