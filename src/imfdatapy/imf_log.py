import logging.config
from datetime import datetime
import os

class LogFile:
    def __init__(self, logdir=None, is_log_to_file=True):

        self.is_log_to_file = is_log_to_file

        cwd = os.getcwd()
        time_stamp = str(datetime.now())[:19].replace(" ", "-").replace(":", "-")

        if not is_log_to_file:
            print("WARN: Just creating a logger with output to screen.")
        else:
            if logdir is None:
                if (cwd[-3:] == "src") or (cwd[-4:] == "demo") or (cwd[-5:] == "tests"):
                    self.logdir = "../log"
                elif cwd[-9:] == "imfdatapy":
                    self.logdir = "../../log"
            else:
                logdir = f"{logdir}{os.sep}" if logdir[-1] != os.sep else logdir
                self.logdir = logdir

            if not os.path.exists(self.logdir):
                print(f"WARN: Creating log directory {self.logdir}")
                os.mkdir(self.logdir)
            self.log_file = f"{self.logdir}/imfdatapy_{time_stamp}.log"


        self.log_format = "%(asctime)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s"

    def start_log(self):
        rootLogger = logging.getLogger()

        if self.is_log_to_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(logging.Formatter(self.log_format))

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logging.Formatter(self.log_format))
        rootLogger.addHandler(consoleHandler)

        logger = logging.getLogger("imfdatapy_log")
        logger.setLevel(logging.INFO)

        if self.is_log_to_file:
            logger.addHandler(file_handler)
            logger.info(f"Current directory {os.getcwd()}")
            logger.info(f"Started log {self.log_file}")

        return logger