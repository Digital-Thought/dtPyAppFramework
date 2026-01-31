"""
Shared pytest configuration and fixtures for dtPyAppFramework tests.
"""

import os
import sys

# Ensure src/ is on the import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
