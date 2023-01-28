import logging.config
from datetime import datetime
import os

time_stamp = str(datetime.now())[:19].replace(" ", "-").replace(":", "-")
cwd = os.getcwd()
is_file_logger = True
if (cwd[-3:] == "src") or (cwd[-4:] == "demo") or (cwd[-5:] == "tests"):
    logdir = "../log"
elif cwd[-9:] == "imfdatapy":
    logdir = "../../log"
else:
    print("WARN: Just creating a logger with output to screen.")
    is_file_logger = False

if is_file_logger:
    if not os.path.exists(logdir):
        print(f"WARN: Creating log directory {logdir}")
        os.mkdir(logdir)
    log_file = f"{logdir}/imfdatapy_{time_stamp}.log"

log_format = "%(asctime)s %(filename)s:%(lineno)d - %(levelname)s - %(message)s"

rootLogger = logging.getLogger()

if is_file_logger:
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(log_format))
rootLogger.addHandler(consoleHandler)

logger = logging.getLogger("imfdatapy_log")
logger.setLevel(logging.INFO)

if is_file_logger:
    logger.addHandler(file_handler)
    logger.info(f"Current directory {os.getcwd()}")
    logger.info(f"Started log {log_file}")