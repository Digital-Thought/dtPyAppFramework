Usage
=====

Here's an example of how to use dtPyAppFramework:

.. code-block:: python

   from dtPyAppFramework.application import AbstractApp
   from dtPyAppFramework import settings

   import logging

   class MyApplication(AbstractApp):

       def define_args(self, arg_parser):
           # Define your command-line arguments here
           return

       def main(self, args):
           logging.info("Running your code")
           ## Place you own code here that you wish to run

   # Initialise and run the application
   MyApplication(description="Simple App", version="1.0", short_name="simple_app",
             full_name="Simple Application", console_app=True).run()

The above example will output the following to the console:


.. image:: _static/simple_app_output.jpg
   :alt: Output
