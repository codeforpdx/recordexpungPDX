import logging


class DetailedFormatter(logging.Formatter):

    formatstr = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    def format(self, record):
        formatter = logging.Formatter(self.formatstr)
        return formatter.format(record)


class ColoredFormatter(DetailedFormatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + DetailedFormatter.formatstr + reset,
        logging.INFO: yellow + DetailedFormatter.formatstr + reset,
        logging.WARNING: yellow + DetailedFormatter.formatstr + reset,
        logging.ERROR: red + DetailedFormatter.formatstr + reset,
        logging.CRITICAL: bold_red + DetailedFormatter.formatstr + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def attach_logger(app):
    app.logger = logging.getLogger("recordexpunge")
    app.logger.setLevel(logging.DEBUG)
    if app.config["TIER"] == "development":
        colored_stdout_handler(app.logger)
        # file_handler(app.logger)
    else:
        stdout_handler(app.logger)


def colored_stdout_handler(logger):
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(ColoredFormatter())
    logger.addHandler(stdout_handler)


def file_handler(logger):
    log_file_handler = logging.FileHandler("logs/expungeservice_log.txt")
    log_file_handler.setLevel(logging.DEBUG)
    log_file_handler.setFormatter(DetailedFormatter())
    logger.addHandler(log_file_handler)


def stdout_handler(logger):
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(DetailedFormatter())
    logger.addHandler(stdout_handler)
