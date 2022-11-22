from typing import Callable
from unittest.mock import MagicMock

import httpx
import pytest
import wsproto
from starlette.types import ASGIApp
from starlette.websockets import WebSocket

from httpx_ws import WebSocketDisconnect, WebSocketUpgradeError, aconnect_ws
from httpx_ws.transport import ASGIWebSocketTransport


@pytest.mark.asyncio
async def test_upgrade_error():
    def handler(request):
        return httpx.Response(400)

    async with httpx.AsyncClient(
        base_url="http://localhost:8000", transport=httpx.MockTransport(handler)
    ) as client:
        with pytest.raises(WebSocketUpgradeError):
            async with aconnect_ws(client, "/ws"):
                pass


@pytest.fixture
def send_app(
    websocket_app_factory: Callable[[Callable], ASGIApp], on_receive_message: MagicMock
) -> ASGIApp:
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()

        message = await websocket.receive_text()
        on_receive_message(message)

        await websocket.close()

    return websocket_app_factory(websocket_endpoint)


@pytest.mark.asyncio
class TestSend:
    async def test_send(
        self,
        websocket_app_factory: Callable[[Callable], ASGIApp],
        on_receive_message: MagicMock,
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            message = await websocket.receive_text()
            on_receive_message(message)

            await websocket.close()

        app = websocket_app_factory(websocket_endpoint)

        async with httpx.AsyncClient(
            base_url="http://localhost:8000", transport=ASGIWebSocketTransport(app)
        ) as client:
            async with aconnect_ws(client, "/ws") as ws:
                await ws.send(wsproto.events.TextMessage(data="CLIENT_MESSAGE"))

        on_receive_message.assert_called_once_with("CLIENT_MESSAGE")

    async def test_send_text(
        self,
        websocket_app_factory: Callable[[Callable], ASGIApp],
        on_receive_message: MagicMock,
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            message = await websocket.receive_text()
            on_receive_message(message)

            await websocket.close()

        app = websocket_app_factory(websocket_endpoint)

        async with httpx.AsyncClient(
            base_url="http://localhost:8000", transport=ASGIWebSocketTransport(app)
        ) as client:
            async with aconnect_ws(client, "/ws") as ws:
                await ws.send_text("CLIENT_MESSAGE")

        on_receive_message.assert_called_once_with("CLIENT_MESSAGE")

    async def test_send_bytes(
        self,
        websocket_app_factory: Callable[[Callable], ASGIApp],
        on_receive_message: MagicMock,
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            message = await websocket.receive_bytes()
            on_receive_message(message)

            await websocket.close()

        app = websocket_app_factory(websocket_endpoint)

        async with httpx.AsyncClient(
            base_url="http://localhost:8000", transport=ASGIWebSocketTransport(app)
        ) as client:
            async with aconnect_ws(client, "/ws") as ws:
                await ws.send_bytes(b"CLIENT_MESSAGE")

        on_receive_message.assert_called_once_with(b"CLIENT_MESSAGE")

    @pytest.mark.parametrize("mode", ["text", "binary"])
    async def test_send_json(
        self,
        mode: str,
        websocket_app_factory: Callable[[Callable], ASGIApp],
        on_receive_message: MagicMock,
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            message = await websocket.receive_json(mode=mode)
            on_receive_message(message)

            await websocket.close()

        app = websocket_app_factory(websocket_endpoint)

        async with httpx.AsyncClient(
            base_url="http://localhost:8000", transport=ASGIWebSocketTransport(app)
        ) as client:
            async with aconnect_ws(client, "/ws") as ws:
                await ws.send_json({"message": "CLIENT_MESSAGE"}, mode=mode)

        on_receive_message.assert_called_once_with({"message": "CLIENT_MESSAGE"})


@pytest.mark.asyncio
async def test_receive_message(websocket_app_factory: Callable[[Callable], ASGIApp]):
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()

        await websocket.send_text("SERVER_MESSAGE")

        await websocket.close()

    app = websocket_app_factory(websocket_endpoint)

    async with httpx.AsyncClient(
        base_url="http://localhost:8000", transport=ASGIWebSocketTransport(app)
    ) as client:
        async with aconnect_ws(client, "/ws") as ws:
            event = await ws.receive()
            assert isinstance(event, wsproto.events.TextMessage)
            assert event.data == "SERVER_MESSAGE"


@pytest.mark.asyncio
async def test_send_close(websocket_app_factory: Callable[[Callable], ASGIApp]):
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.receive_text()

    app = websocket_app_factory(websocket_endpoint)

    async with httpx.AsyncClient(
        base_url="http://localhost:8000", transport=ASGIWebSocketTransport(app)
    ) as client:
        async with aconnect_ws(client, "/ws"):
            pass


@pytest.mark.asyncio
async def test_receive_close(websocket_app_factory: Callable[[Callable], ASGIApp]):
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await websocket.close()

    app = websocket_app_factory(websocket_endpoint)

    async with httpx.AsyncClient(
        base_url="http://localhost:8000", transport=ASGIWebSocketTransport(app)
    ) as client:
        with pytest.raises(WebSocketDisconnect):
            async with aconnect_ws(client, "/ws") as ws:
                await ws.receive()