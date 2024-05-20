from collections import namedtuple

import pytest

from chain import (
    extractor,
    configs,
)


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


@pytest.mark.parametrize(
    "pair, key, expected",
    [
        ({"key": "value"}, "''", None),
        ({"key": {"key2": "value"}}, "key.key2", "value"),
    ],
)
def test_get_nested_value(pair, key, expected):
    assert extractor.get_nested_value(pair, key) == expected


def get_expected_pair_record():
    base_record = {
        "chain": "solana",
        "base_token_address": mock_token_address,
        "base_token_api": f"https://api.dexscreener.com/latest/dex/tokens/{mock_token_address}",
        "website": "https://example.com",
    }
    mock_pair_records = [base_record, {**base_record, "twitter": "example"}]
    return [PairRecord(**{k: record.get(k, None) for k in fields_to_extract}) for record in mock_pair_records]


def test_map_pair_to_dataclass():
    assert extractor.get_pair_record(mock_pair[0]) == get_expected_pair_record()[0]


@pytest.mark.parametrize(
    "chain, pairs, expected",
    [
        ("ethereum", mock_pair, []),
        ("solana", mock_pair, get_expected_pair_record()),
    ],
)
def test_extract_pairs(chain, pairs, expected):
    assert extractor.extract_pairs(chain, pairs) == expected
