import json
import pathlib
import typing

import pandas as pd

from utils import logger as utils_logger


def open_json_file(json_file: str) -> typing.Dict:
    with open(json_file) as f:
        return json.load(f)


def save_report_as_csv(data_frame: pd.DataFrame, report_file: pathlib.Path):
    report_dir = report_file.parent
    report_dir.mkdir(parents=True, exist_ok=True)
    data_frame.to_csv(report_file, index=False)
    utils_logger.logger.info(f"Saved {len(data_frame)} pairs to: {report_file}.")
