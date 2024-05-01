from collections import namedtuple

import pandas as pd
import pytest

from chain import pairs, configs


fields_to_extract = configs.settings["fields_to_extract"]
PairRecord = namedtuple("PairRecord", fields_to_extract.keys())
mock_token_address = "0x123"
mock_pair = [
    {
        "chainId": "solana",
        "baseToken": {"address": mock_token_address},
        "profile": {"website": "https://example.com"}
    },
    {
        "chainId": "solana",
        "baseToken": {"address": mock_token_address},
        "profile": {"website": "https://example.com", "twitter": "example"}
    },
]


def get_exepected_pair_record():
    mock_pair_record = {
        "chain": "solana",
        "base_token_address": mock_token_address,
        "base_token_api": f"https://api.dexscreener.com/latest/dex/tokens/{mock_token_address}"
    }
    expected = {k: mock_pair_record.get(k, None) for k, _ in fields_to_extract.items()}
    return PairRecord(**expected)


@pytest.mark.parametrize(
    "chain, chain_pairs, expected",
    [
        ("ethereum", mock_pair, pd.DataFrame([])),
        ("solana", mock_pair, pd.DataFrame([get_exepected_pair_record()])),
    ]
)
def test_create_data_frame(chain, chain_pairs, expected):
    pd.testing.assert_frame_equal(pairs.create_data_frame(chain, chain_pairs), expected)


@pytest.mark.parametrize(
    "chain, expected",
    [
        ("ethereum", pd.DataFrame([])),
        ("solana", pd.DataFrame([get_exepected_pair_record()])),
    ]
)
def test_get_pairs(mocker, chain, expected):
    mocker.patch("chain.pairs.downloader.retrieve_pairs", return_value=mock_pair)
    pd.testing.assert_frame_equal(pairs.get_pairs(chain, "uri"), expected)


@pytest.mark.parametrize(
    "chain, pair_type, expected",
    [
        ("solana", "all", [("all", pd.DataFrame([get_exepected_pair_record()]))]),
    ]
)
def test_get_chain_pairs(mocker, chain, pair_type, expected):
    mocker.patch("chain.pairs.downloader.retrieve_pairs", return_value=mock_pair)
    print(f"xxxxxxxxxxxxxxxx: {list(pairs.get_chain_pairs(chain, pair_type))}")
