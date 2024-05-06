from utils import (
    file_io,
    logger as utils_logger,
)


settings = file_io.open_json_file("chain/settings.json")
logger = utils_logger.logger
max_retries = 5
