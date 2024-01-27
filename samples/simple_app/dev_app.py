import sys
import os
import time

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework import settings

import logging


class SimpleApp(AbstractApp):

    def define_args(self, arg_parser):
        return

    def main(self, args):
        logging.info("Running your code")


 #def new_multiprocessing_job(self, job_name, worker_count, target, args=(), kwargs={}):
os.environ['DEV_MODE'] = "True"
SimpleApp(description="Simple App", version="1.0", short_name="simple_app",
             full_name="Simple Application", console_app=True).run()
