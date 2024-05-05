import typing

import pandas as pd

from chain import (
    configs,
    downloader,
    extractor,
)


def create_data_frame(chain: str, pairs: typing.List[typing.Dict]) -> pd.DataFrame:
    extracted_pairs = extractor.extract_pairs(chain, pairs)
    configs.logger.info(
        f"Extracted {len(extracted_pairs)} pairs out of {len(pairs)} downloaded pairs."
    )
    return pd.DataFrame(extracted_pairs)


def get_pairs(chain: str, uri: str) -> pd.DataFrame:
    pairs = downloader.retrieve_pairs(uri, configs.max_retries)
    configs.logger.info(f"Downloaded {len(pairs)} pairs from {uri}")
    pairs_df = create_data_frame(chain, pairs)
    return pairs_df


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
