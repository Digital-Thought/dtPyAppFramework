import sys
import os
import logging
import pytest

sys.path.append(os.path.abspath('../src'))

from dtPyAppFramework.paths import ApplicationPaths
from dtPyAppFramework.secrets_store import SecretsManager
from dtPyAppFramework import app_logging


class CoreTests:

    def test_1(self):
        assert 1 == 1
