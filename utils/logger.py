import logging

import colorlog


formatter = colorlog.ColoredFormatter(
    fmt="%(black)s%(asctime)s  %(log_color)s%(levelname)s%(reset)s  %(message_log_color)s%(message)s",
    datefmt="%b %d %Y, %H:%M %Z",
    style='%',
    secondary_log_colors={
        'message': {
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red'
        }
    }
)


def configure_logger(name=None):
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


logger = configure_logger()
