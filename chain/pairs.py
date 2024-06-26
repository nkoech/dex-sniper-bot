import typing

import pandas as pd

from chain import (
    configs,
    downloader,
    extractor,
)


def download_pairs(uri: str) -> typing.List[dict]:
    pairs = downloader.retrieve_pairs(uri, configs.max_retries)
    configs.logger.info(f"Downloaded {len(pairs)} pairs from {uri}")
    return pairs


def extract_pairs(chain: str, pairs: typing.List[dict]) -> pd.DataFrame:
    extracted_pairs = extractor.extract_pairs(chain, pairs)
    df = pd.DataFrame(extracted_pairs)
    configs.logger.info(f"Extracted {len(df)} pairs from {len(pairs)} pairs")
    return df


def get_chain_pairs(
    chain: str, pair_types: typing.List[str]
) -> typing.Generator[typing.Tuple[str, pd.DataFrame], None, None]:
    base_url = configs.settings["url"]["pairs_dex"]
    chain_settings = configs.settings[chain]
    for pair_type in pair_types:
        setting = chain_settings[pair_type]
        api_query = f"{setting['since']}/1?&{setting['filter']}&{setting['rank_by']}"
        pairs = download_pairs(f"{base_url}/{api_query}")
        yield pair_type, extract_pairs(chain, pairs)
