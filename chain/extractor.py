import typing
from collections import namedtuple

from chain import configs


base_token_api_url = configs.settings["tokens_api_url"]
fields_to_extract = configs.settings["fields_to_extract"]
PairRecord = namedtuple("PairRecord", fields_to_extract.keys())


def has_socials(profile: dict) -> bool:
    return bool(profile.get("website")) and bool(profile.get("twitter", False))


def get_nested_value(pair: dict, key: str) -> typing.Optional[typing.Union[str, float]]:
    key_parts = key.split(".")
    value = pair
    for part in key_parts:
        value = value.get(part)
        if value is None:
            return None
    return value


def get_pair_record(
    pair: typing.Dict[str, typing.Optional[typing.Union[str, float]]]
) -> PairRecord:
    pair_record = {
        field: get_nested_value(pair, key) for field, key in fields_to_extract.items()
    }
    pair_record["base_token_api"] = (
        f"{base_token_api_url}/{pair_record['base_token_address']}"
    )
    return PairRecord(**pair_record)


def extract_pairs(chain: str, pairs: typing.List[dict]) -> typing.List[PairRecord]:
    chain_pairs = []
    for pair in pairs:
        if pair["chainId"] != chain or not has_socials(pair.get("profile", {})):
            continue
        chain_pairs.append(get_pair_record(pair))
    return chain_pairs
