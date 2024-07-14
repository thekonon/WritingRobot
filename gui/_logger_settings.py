import logging

def get_logger_console_handler() -> logging.StreamHandler:
    """
        Return s handler for console logging
    """
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
    c_handler.setFormatter(c_format)
    return c_handler
    
    
def get_logger_file_handler() -> logging.FileHandler:
    f_handler = logging.FileHandler('log.log')
    f_handler.setLevel(logging.ERROR)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    return f_handler