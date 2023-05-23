import logging.config
from datetime import datetime
import os


class LogFile:
    def __init__(self, logdir="log", is_log_to_screen=True):

        self.is_log_to_screen = is_log_to_screen

        time_stamp = str(datetime.now())[:19].replace(" ", "-").replace(":", "-")

        logdir = f"{logdir}{os.sep}" if logdir[-1] != os.sep else logdir
        self.logdir = logdir

        if not os.path.exists(self.logdir):
            os.mkdir(self.logdir)

        self.log_file = f"{self.logdir}imfdatapy_{time_stamp}.log"

        self.log_format = "%(asctime)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s"

    def start_log(self):
        rootLogger = logging.getLogger()

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter(self.log_format))

        if self.is_log_to_screen:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logging.Formatter(self.log_format))
            rootLogger.addHandler(consoleHandler)
        else:
            # Remove consoleHandler if it exists
            for handler in rootLogger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    rootLogger.removeHandler(handler)

        logger = logging.getLogger("imfdatapy_log")
        logger.setLevel(logging.INFO)

        logger.addHandler(file_handler)

        logger.info(f"Current directory {os.getcwd()}")
        logger.info(f"Started log file in .{os.sep}{self.log_file}")

        return logger