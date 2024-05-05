import typing
from utils import (
    file_io,
    logger as utils_logger,
)


def generate_http_header() -> typing.Dict:
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.0.0 Safari/537.36"
    )
    origin = "https://dexscreener.com"
    return {
        "User-Agent": user_agent,
        "Origin": origin,
    }


logger = utils_logger.logger
max_retries = 5
http_header = generate_http_header()
settings = file_io.open_json_file("chain/settings.json")
