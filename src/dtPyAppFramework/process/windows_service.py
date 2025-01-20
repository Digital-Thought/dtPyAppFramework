import platform
import logging

if platform.system() == "Windows":
    try:
        import win32service
        import win32serviceutil
        import win32event
        import servicemanager
    except ImportError as ex:
        logging.error("pywin32 is not installed.")
        raise ex


class WindowsService(win32serviceutil.ServiceFramework):

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        from dtPyAppFramework.process import ProcessManager
        self.args = args
        process_manager = ProcessManager()
        self.running_function = process_manager.__main__
        self.stop_function = process_manager.handle_shutdown
        self._svc_name_ = process_manager.short_name
        self._svc_display_name_ = process_manager.full_name
        self._svc_description_ = process_manager.description

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop_function(self.args)

    def SvcDoRun(self):
        logging.info(f"Service {self.name} is starting...")
        servicemanager.LogInfoMsg(f"Service {self.name} is starting...")
        self.running_function(self.args)
        logging.info("Service is stopping...")