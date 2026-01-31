import sys
import os
import time

sys.path.append(os.path.abspath('../../src'))

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.process import ProcessManager
from dtPyAppFramework.process.multiprocessing import MultiProcessingManager, MultiProcessingJob
import time
import logging

def start_worker_instance(key):
    logging.info(f'Working with Key: {key}')
    time.sleep(1)
    val = Settings().secret_manager.get_secret(key)
    logging.info(f'Finished Value: {val}')
    val += 1
    Settings().secret_manager.set_secret('bob', val)
    event = getattr(ProcessManager(), 'spawned_running_event', None)
    while event is not None and event.is_set():
        time.sleep(0.5)

class MultiprocessingApp(AbstractApp):

    def define_args(self, arg_parser):
        return

    def main(self, args):
        val = 1
        Settings().secret_manager.set_secret('bob', val)
        job = MultiProcessingManager().new_multiprocessing_job(job_name='default_multiprocessing_job',
                                worker_count=2,
                                target=start_worker_instance,
                                args=('bob',))
        job.start()
        val += 1
        Settings().secret_manager.set_secret('bob', val)
        time.sleep(10)
        job.close()
        logging.info(f'Finished: {Settings().secret_manager.get_secret('bob')}')
        time.sleep(5)
        ProcessManager().call_shutdown()


    def exiting(self):
        logging.info('Put your custom exiting process here!')


os.environ['DEV_MODE'] = "True"
MultiprocessingApp(description="Multiprocessing App", version="1.0", short_name="multiprocessing_app",
             full_name="Multiprocessing Application", console_app=True).run()
