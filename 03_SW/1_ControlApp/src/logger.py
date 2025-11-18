import logging

_logger: logging.Logger|None = None

def get_logger() -> logging.Logger:
    global _logger
    if not _logger:
        _logger = logging.getLogger("RobotGUI")
        _logger.setLevel(logging.DEBUG)
        _logger.addHandler(get_logger_console_handler())
        _logger.addHandler(get_logger_file_handler())
    return _logger


def get_logger_console_handler() -> logging.StreamHandler:
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter("%(asctime)s | %(levelname)s: %(name)s: %(message)s")
    c_handler.setFormatter(c_format)
    return c_handler


def get_logger_file_handler() -> logging.FileHandler:
    f_handler = logging.FileHandler("log.log")
    f_handler.setLevel(logging.ERROR)
    f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    f_handler.setFormatter(f_format)
    return f_handler
