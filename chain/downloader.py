from contextlib import contextmanager
import json
import ssl
import typing

import websocket

from chain import configs


@contextmanager
def websocket_connection(
    uri: str, header: dict, suppress_origin: bool = True
) -> typing.Generator[websocket.WebSocket, None, None]:
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    try:
        ws.connect(uri, header=header, suppress_origin=suppress_origin)
        yield ws
    except websocket.WebSocketException as e:
        configs.logger.error(f"Failed websocket connection: {e}")
    finally:
        ws.close()


def receive_pairs_from_websocket(
    ws: websocket.WebSocket,
) -> typing.Dict[str, typing.Any]:
    try:
        return json.loads(ws.recv())
    except json.JSONDecodeError as e:
        configs.logger.error(f"Failed to decode JSON: {e}")
        return {}


def retrieve_pairs(uri: str, max_tries: int) -> typing.List[dict]:
    http_header = configs.settings["http_header"]
    for tries in range(max_tries):
        with websocket_connection(uri, http_header) as ws:
            pairs = receive_pairs_from_websocket(ws).get("pairs")
            if pairs:
                return pairs
        configs.logger.info(
            f"Attempt {tries + 1} of {max_tries} failed to retrieve pairs."
        )
    return []
