import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'dtPyAppFramework'
author = 'Digital-Thought'
copyright = '2024, Digital-Thought'
release = '2.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
