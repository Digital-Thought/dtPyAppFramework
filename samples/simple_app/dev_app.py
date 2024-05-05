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
        logging.info(f'All Key/Value Pairs in the Secret for cloud store "test1" : {settings.Settings()['test1']}')
        logging.info(f'Just the value for "key1" in the Secret for cloud store "test1" : {settings.Settings()['test1.key1']}')


 #def new_multiprocessing_job(self, job_name, worker_count, target, args=(), kwargs={}):
os.environ['DEV_MODE'] = "True"
SimpleApp(description="Simple App", version="1.0", short_name="simple_app",
             full_name="Simple Application", console_app=True).run()
