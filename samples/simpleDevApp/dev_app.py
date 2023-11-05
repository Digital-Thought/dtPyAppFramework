import sys
import os
import time

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.app import AbstractApp
from dtPyAppFramework import settings

import logging

class SimpleApp(AbstractApp):

    def define_args(self, arg_parser):
        return

    def main(self, args):
        logging.info("Running your code")
        ## Place you own code here that you wish to run

SimpleApp(description="Simple App", version="1.0", short_name="simple_app",
             full_name="Simple Application", console_app=True).run()
