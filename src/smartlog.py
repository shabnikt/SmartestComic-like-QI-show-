import logging
import os


class Formatter(logging.Formatter):
    grey = "\x1b[29;20m"
    yellow = "\x1b[33;2m"
    red = "\x1b[31;2m"
    bold_red = "\x1b[31;21m"
    reset = "\x1b[0m"
    format_info = "%(asctime)s: %(levelname)s: %(module)s: %(message)s"
    format_rest = "%(levelname)s: %(module)s: %(funcName)s: %(lineno)d: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_rest + reset,
        logging.INFO: grey + format_info,
        logging.WARNING: yellow + format_rest + reset,
        logging.ERROR: red + format_rest + reset,
        logging.CRITICAL: bold_red + format_rest + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log_level = logging.getLevelName(os.getenv("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)
log.setLevel(log_level)

# defines the stream handler
_ch = logging.StreamHandler()  # creates the handler
# _ch.setLevel(logging.INFO)  # creates the handler
_ch.setFormatter(Formatter())  # sets the handler formatting
log.addHandler(_ch)
