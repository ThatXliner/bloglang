from typing import Optional
from bloglang import ast
from bloglang.plugin import __stub, __default, stdlib
import pluggy

manager = pluggy.PluginManager("bloglang.plugin")
manager.add_hookspecs(__stub)
manager.load_setuptools_entrypoints("bloglang.plugin")
manager.register(stdlib)
manager.register(__default)
