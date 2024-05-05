import pytest

from chain import downloader


class FakeWebSocket:
    def __init__(self, data):
        self.data = data
        self.closed = False

    def recv(self):
        return self.data


@pytest.mark.parametrize(
    "ws_data, expected",
    [
        (
            '{"pairs": [{"pair": "BTC/USD", "price": 10000}]}',
            {"pairs": [{"pair": "BTC/USD", "price": 10000}]},
        ),
        ('{"pairs": not a valid json}', {}),
    ],
)
def test_receive_pairs_from_websocket(ws_data, expected):
    ws = FakeWebSocket(ws_data)
    pairs = downloader.receive_pairs_from_websocket(ws)
    assert pairs == expected
