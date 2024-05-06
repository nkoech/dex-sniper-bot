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
        "profile": {"website": "https://example.com"},
    },
    {
        "chainId": "solana",
        "baseToken": {"address": mock_token_address},
        "profile": {"website": "https://example.com", "twitter": "example"},
    },
]


def get_exepected_pair_record():
    mock_pair_record = {
        "chain": "solana",
        "base_token_address": mock_token_address,
        "base_token_api": f"https://api.dexscreener.com/latest/dex/tokens/{mock_token_address}",
    }
    expected = {k: mock_pair_record.get(k, None) for k, _ in fields_to_extract.items()}
    return PairRecord(**expected)


@pytest.mark.parametrize(
    "chain, input_pairs, expected",
    [
        ("ethereum", [], pd.DataFrame([])),
        ("solana", mock_pair, pd.DataFrame([get_exepected_pair_record()])),
    ],
)
def test_extract_pairs(chain, input_pairs, expected):
    pd.testing.assert_frame_equal(pairs.extract_pairs(chain, input_pairs), expected)


@pytest.mark.parametrize(
    "chain, pair_type, expected",
    [
        (
            "solana",
            ["new_pairs", "trending_pairs"],
            [
                ("new_pairs", pd.DataFrame([get_exepected_pair_record()])),
                ("trending_pairs", pd.DataFrame([get_exepected_pair_record()])),
            ],
        ),
    ],
)
def test_get_chain_pairs(mocker, chain, pair_type, expected):
    mocker.patch("chain.pairs.downloader.retrieve_pairs", return_value=mock_pair)
    for i, (result_pair_type, result_pairs_df) in enumerate(
        pairs.get_chain_pairs(chain, pair_type)
    ):
        assert result_pair_type == expected[i][0]
        pd.testing.assert_frame_equal(result_pairs_df, expected[i][1])
