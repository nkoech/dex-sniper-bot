import typing

import requests

import configs


def request_pairs(uri: str) -> typing.Dict[str, typing.Any]:
    try:
        response = requests.get(uri)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        configs.logger.error(f"Failed to request pairs from {uri}: {e}")
        return {}


def retrieve_pairs(uri: str, max_tries: int) -> typing.List[str]:
    for tries in range(max_tries):
        pairs = request_pairs(uri).get("pairs")
        if pairs:
            return pairs
        configs.logger.info(f"Attempt {tries + 1} of {max_tries} failed to retrieve pairs.")
    return []
