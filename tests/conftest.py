import contextlib
import pathlib
import tempfile
from collections.abc import Callable
from typing import Literal, Protocol
from unittest.mock import MagicMock

import anyio
import pytest
import uvicorn
from anyio.from_thread import start_blocking_portal
from starlette.applications import Starlette
from starlette.routing import WebSocketRoute


@pytest.fixture
def on_receive_message():
    return MagicMock()


@pytest.fixture(params=("wsproto", "websockets"))
def websocket_implementation(request) -> Literal["wsproto", "websockets"]:
    return request.param


class ServerFactoryFixture(Protocol):
    def __call__(
        self, endpoint: Callable
    ) -> contextlib.AbstractContextManager[str]: ...


@pytest.fixture
def server_factory(
    websocket_implementation: Literal["wsproto", "websockets"],
) -> ServerFactoryFixture:
    @contextlib.contextmanager
    def _server_factory(endpoint: Callable):
        with (
            start_blocking_portal(backend="asyncio") as portal,
            tempfile.TemporaryDirectory() as socket_directory,
        ):
            socket = str(pathlib.Path(socket_directory) / "socket.sock")
            app = Starlette(routes=[WebSocketRoute("/ws", endpoint=endpoint)])
            server = uvicorn.Server(
                uvicorn.Config(app, uds=socket, ws=websocket_implementation)
            )
            task = portal.start_task_soon(server.serve)

            async def wait_until_started():
                with anyio.fail_after(5):
                    while not server.started:
                        if task.done():
                            task.result()
                            raise RuntimeError(
                                "Uvicorn stopped before opening its socket"
                            )
                        await anyio.sleep(0.01)

            try:
                portal.call(wait_until_started)
                yield socket
            finally:
                server.should_exit = True
                task.result()

    return _server_factory
