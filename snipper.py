import pathlib
import typing

from chain import (
    configs,
    pairs,
)
from utils import file_io


def snip(chain: str, pair_types: typing.List[str]):
    reports_dir = pathlib.Path(configs.settings["reports_dir"]) / chain
    for pair_type, pairs_df in pairs.get_chain_pairs(chain, pair_types):
        report_file = reports_dir / f"{pair_type}.csv"
        file_io.save_report_as_csv(pairs_df, report_file)
        print(pairs_df[:10])


if __name__ == "__main__":
    snip("solana", ["new_pairs", "gaining_pairs", "trending_pairs"])
