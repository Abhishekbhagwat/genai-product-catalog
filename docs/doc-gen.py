import sys
import os

from pydoc_markdown.interfaces import Context
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.renderers.markdown import MarkdownRenderer

title = sys.argv[1]

context = Context(directory=os.getcwd())
loader = PythonLoader(search_path=['google/cloud/ml/applied'])
renderer = MarkdownRenderer(render_module_header=False)

loader.init(context)
renderer.init(context)

modules = loader.load()

print("""
---
title: "{0}"
weight: 4
---

""".format(title))

print(renderer.render_to_string(modules))
