import typing

import pandas as pd

from chain import (
    configs,
    downloader,
    extractor,
)


def get_pairs(chain: str, uri: str) -> pd.DataFrame:
    pairs = downloader.retrieve_pairs(uri, configs.max_retries)
    count = len(pairs)
    configs.logger.info(f"Downloaded {count} pairs from {uri}")
    extracted_pairs = extractor.extract_pairs(chain, pairs)
    df = pd.DataFrame(extracted_pairs)
    configs.logger.info(f"Extracted {len(df)} pairs from {count} pairs")
    return df


def get_chain_pairs(
    chain: str, pair_types: typing.List[str]
) -> typing.Generator[typing.Tuple[str, pd.DataFrame], None, None]:
    base_url = configs.settings["base_url"]
    chain_settings = configs.settings[chain]
    for pair_type in pair_types:
        setting = chain_settings[pair_type]
        uri = (
            f"{base_url}/{setting['since']}/1?&{setting['filter']}&{setting['rank_by']}"
        )
        yield pair_type, get_pairs(chain, uri)
