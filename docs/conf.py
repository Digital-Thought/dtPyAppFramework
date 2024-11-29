import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

from dtPyAppFramework.misc.packaging import load_module_package, ModulePackage

module_package: ModulePackage = load_module_package(os.path.join('../src/dtPyAppFramework', '_metadata.yaml'))

project = module_package.short_name
author = 'Digital-Thought'
copyright = '2024, Digital-Thought'
release = module_package.version

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
