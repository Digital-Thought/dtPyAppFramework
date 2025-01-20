import sys
import os
import time

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.process import ProcessManager

import logging


class SimpleApp(AbstractApp):

    def define_args(self, arg_parser):
        return

    def main(self, args):
        logging.info("Running your code")
        logging.info(f'Secrets Store Index : {Settings().secret_manager.get_local_stores_index()}')
        Settings()['test1'] = 'hellow world'
        logging.info(Settings().get_raw_settings())
        logging.info(f'All Key/Value Pairs in the Secret for cloud store "test1" : {Settings().get("test1")}')
        logging.info(f'All Key/Value Pairs in the Secret for cloud store "test_setting.bob" : {Settings().get("test_setting.bob")}')
        logging.debug(f'All Key/Value Pairs in the Secret for cloud store "test_setting.bob" : {Settings().get("test_setting.bob")}')
        logging.info(f'All Key/Value Pairs in the Secret for cloud store "test_setting.app_core" : {Settings().get("test_setting.app_core")}')
        Settings().secret_manager.set_secret('bob', 'hello world')
        # logging.info(f'Just the value for "key1" in the Secret for cloud store "test1" : {settings.Settings()['test1.key1']}')
        #ProcessManager().handle_shutdown()


    def exiting(self):
        logging.info('Put your custom exiting process here!')


#def new_multiprocessing_job(self, job_name, worker_count, target, args=(), kwargs={}):
os.environ['DEV_MODE'] = "True"
SimpleApp(description="Simple App", version="1.0", short_name="simple_app",
             full_name="Simple Application", console_app=True).run()
