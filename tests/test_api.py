import asyncio
import contextlib
import queue
import time
import typing
from unittest.mock import MagicMock, call, patch

import httpcore
import httpx
import pytest
import wsproto
from httpcore.backends.base import AsyncNetworkStream, NetworkStream
from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect as StarletteWebSocketDisconnect

from httpx_ws import (
    AsyncWebSocketSession,
    JSONMode,
    WebSocketDisconnect,
    WebSocketInvalidTypeReceived,
    WebSocketNetworkError,
    WebSocketSession,
    WebSocketUpgradeError,
    aconnect_ws,
    connect_ws,
)
from tests.conftest import ServerFactoryFixture


@pytest.mark.asyncio
async def test_upgrade_error():
    def handler(request):
        return httpx.Response(400)

    with httpx.Client(
        base_url="http://localhost:8000", transport=httpx.MockTransport(handler)
    ) as client:
        with pytest.raises(WebSocketUpgradeError):
            with connect_ws("http://socket/ws", client):
                pass

    async with httpx.AsyncClient(
        base_url="http://localhost:8000", transport=httpx.MockTransport(handler)
    ) as client:
        with pytest.raises(WebSocketUpgradeError):
            async with aconnect_ws("http://socket/ws", client):
                pass


@pytest.mark.asyncio
class TestSend:
    async def test_send_error(self):
        class MockNetworkStream(NetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )
                self._should_close = False

            def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                while not self._should_close:
                    time.sleep(0.1)
                raise httpcore.ReadError()

            def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                raise httpcore.WriteError()

            def close(self) -> None:
                self._should_close = True

        stream = MockNetworkStream()
        websocket_session = WebSocketSession(stream)
        with pytest.raises(WebSocketNetworkError):
            websocket_session.send(wsproto.events.Ping())
        websocket_session.close()

    async def test_async_send_error(self):
        class AsyncMockNetworkStream(AsyncNetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )
                self._should_close = False

            async def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                while not self._should_close:
                    await asyncio.sleep(0.1)
                raise httpcore.ReadError()

            async def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                raise httpcore.WriteError()

            async def aclose(self) -> None:
                self._should_close = True

        stream = AsyncMockNetworkStream()
        websocket_session = AsyncWebSocketSession(stream)
        with pytest.raises(WebSocketNetworkError):
            await websocket_session.send(wsproto.events.Ping())
        await websocket_session.close()

    async def test_send(
        self,
        server_factory: ServerFactoryFixture,
        on_receive_message: MagicMock,
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            message = await websocket.receive_text()
            on_receive_message(message)

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        ws.send(wsproto.events.TextMessage(data="CLIENT_MESSAGE"))
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        await aws.send(
                            wsproto.events.TextMessage(data="CLIENT_MESSAGE")
                        )
                except WebSocketDisconnect:
                    pass

        on_receive_message.assert_has_calls(
            [call("CLIENT_MESSAGE"), call("CLIENT_MESSAGE")]
        )

    async def test_send_text(
        self,
        server_factory: ServerFactoryFixture,
        on_receive_message: MagicMock,
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            message = await websocket.receive_text()
            on_receive_message(message)

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        ws.send_text("CLIENT_MESSAGE")
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        await aws.send_text("CLIENT_MESSAGE")
                except WebSocketDisconnect:
                    pass

        on_receive_message.assert_has_calls(
            [call("CLIENT_MESSAGE"), call("CLIENT_MESSAGE")]
        )

    async def test_send_bytes(
        self,
        server_factory: ServerFactoryFixture,
        on_receive_message: MagicMock,
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            message = await websocket.receive_bytes()
            on_receive_message(message)

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        ws.send_bytes(b"CLIENT_MESSAGE")
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        await aws.send_bytes(b"CLIENT_MESSAGE")
                except WebSocketDisconnect:
                    pass

        on_receive_message.assert_has_calls(
            [call(b"CLIENT_MESSAGE"), call(b"CLIENT_MESSAGE")]
        )

    @pytest.mark.parametrize("mode", ["text", "binary"])
    async def test_send_json(
        self,
        mode: JSONMode,
        server_factory: ServerFactoryFixture,
        on_receive_message: MagicMock,
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()

            message = await websocket.receive_json(mode=mode)
            on_receive_message(message)

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        ws.send_json({"message": "CLIENT_MESSAGE"}, mode=mode)
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        await aws.send_json({"message": "CLIENT_MESSAGE"}, mode=mode)
                except WebSocketDisconnect:
                    pass

        on_receive_message.assert_has_calls(
            [call({"message": "CLIENT_MESSAGE"}), call({"message": "CLIENT_MESSAGE"})]
        )


@pytest.mark.asyncio
class TestReceive:
    async def test_receive_error(self):
        class MockNetworkStream(NetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )

            def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                raise httpcore.ReadError()

            def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                pass

            def close(self) -> None:
                pass

        stream = MockNetworkStream()
        websocket_session = WebSocketSession(stream)
        with pytest.raises(WebSocketNetworkError):
            websocket_session.receive()
        websocket_session.close()

    async def test_async_receive_error(self):
        class AsyncMockNetworkStream(AsyncNetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )

            async def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                raise httpcore.ReadError()

            async def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                pass

            async def aclose(self) -> None:
                pass

        stream = AsyncMockNetworkStream()
        websocket_session = AsyncWebSocketSession(stream)
        with pytest.raises(WebSocketNetworkError):
            await websocket_session.receive()
        await websocket_session.close()

    async def test_receive(self, server_factory: ServerFactoryFixture):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await asyncio.sleep(0.1)  # FIXME: see #7

            await websocket.send_text("SERVER_MESSAGE")

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        event = ws.receive()
                        assert isinstance(event, wsproto.events.TextMessage)
                        assert event.data == "SERVER_MESSAGE"
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        event = await aws.receive()
                        assert isinstance(event, wsproto.events.TextMessage)
                        assert event.data == "SERVER_MESSAGE"
                except WebSocketDisconnect:
                    pass

    async def test_receive_text(self, server_factory: ServerFactoryFixture):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await asyncio.sleep(0.1)  # FIXME: see #7

            await websocket.send_text("SERVER_MESSAGE")

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        data = ws.receive_text()
                        assert data == "SERVER_MESSAGE"
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        data = await aws.receive_text()
                        assert data == "SERVER_MESSAGE"
                except WebSocketDisconnect:
                    pass

    async def test_receive_text_invalid_type(
        self, server_factory: ServerFactoryFixture
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await asyncio.sleep(0.1)  # FIXME: see #7

            await websocket.send_bytes(b"SERVER_MESSAGE")

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        with pytest.raises(WebSocketInvalidTypeReceived):
                            ws.receive_text()
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        with pytest.raises(WebSocketInvalidTypeReceived):
                            await aws.receive_text()
                except WebSocketDisconnect:
                    pass

    async def test_receive_bytes(self, server_factory: ServerFactoryFixture):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await asyncio.sleep(0.1)  # FIXME: see #7

            await websocket.send_bytes(b"SERVER_MESSAGE")

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        data = ws.receive_bytes()
                        assert data == b"SERVER_MESSAGE"
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        data = await aws.receive_bytes()
                        assert data == b"SERVER_MESSAGE"
                except WebSocketDisconnect:
                    pass

    async def test_receive_bytes_invalid_type(
        self, server_factory: ServerFactoryFixture
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await asyncio.sleep(0.1)  # FIXME: see #7

            await websocket.send_text("SERVER_MESSAGE")

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                with connect_ws("http://socket/ws", client) as ws:
                    with pytest.raises(WebSocketInvalidTypeReceived):
                        ws.receive_bytes()

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                async with aconnect_ws("http://socket/ws", aclient) as aws:
                    with pytest.raises(WebSocketInvalidTypeReceived):
                        await aws.receive_bytes()

    @pytest.mark.parametrize("mode", ["text", "binary"])
    async def test_receive_json(
        self, mode: JSONMode, server_factory: ServerFactoryFixture
    ):
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await asyncio.sleep(0.1)  # FIXME: see #7

            await websocket.send_json({"message": "SERVER_MESSAGE"}, mode=mode)

            await websocket.close()

        with server_factory(websocket_endpoint) as socket:
            with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
                try:
                    with connect_ws("http://socket/ws", client) as ws:
                        data = ws.receive_json(mode=mode)
                        assert data == {"message": "SERVER_MESSAGE"}
                except WebSocketDisconnect:
                    pass

            async with httpx.AsyncClient(
                transport=httpx.AsyncHTTPTransport(uds=socket)
            ) as aclient:
                try:
                    async with aconnect_ws("http://socket/ws", aclient) as aws:
                        data = await aws.receive_json(mode=mode)
                        assert data == {"message": "SERVER_MESSAGE"}
                except WebSocketDisconnect:
                    pass


@pytest.mark.asyncio
class TestReceivePing:
    async def test_receive_ping(self):
        class MockNetworkStream(NetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )
                self.events_to_send = [
                    wsproto.events.Ping(b"SERVER_PING"),
                    wsproto.events.CloseConnection(1000),
                ]

            def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                try:
                    event = self.events_to_send.pop(0)
                    return self.connection.send(event)
                except IndexError:
                    raise httpcore.ReadError()

            def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                self.connection.receive_data(buffer)

            def close(self) -> None:
                pass

        stream = MockNetworkStream()
        websocket_session = WebSocketSession(stream)
        await asyncio.sleep(0.1)
        websocket_session.close()

        received_events = list(stream.connection.events())
        assert received_events == [
            wsproto.events.Pong(b"SERVER_PING"),
            wsproto.events.CloseConnection(1000, ""),
        ]

    async def test_async_receive_ping(self):
        class MockAsyncNetworkStream(AsyncNetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )
                self.events_to_send = [
                    wsproto.events.Ping(b"SERVER_PING"),
                    wsproto.events.CloseConnection(1000),
                ]

            async def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                try:
                    event = self.events_to_send.pop(0)
                    return self.connection.send(event)
                except IndexError:
                    raise httpcore.ReadError()

            async def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                self.connection.receive_data(buffer)

            async def aclose(self) -> None:
                pass

        stream = MockAsyncNetworkStream()
        websocket_session = AsyncWebSocketSession(stream)
        await asyncio.sleep(0.1)
        await websocket_session.close()

        received_events = list(stream.connection.events())
        assert received_events == [
            wsproto.events.Pong(b"SERVER_PING"),
            wsproto.events.CloseConnection(1000, ""),
        ]


@pytest.mark.asyncio
class TestKeepalivePing:
    async def test_keepalive_ping(self):
        class MockNetworkStream(NetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )
                self._should_close = False
                self.ping_received = 0
                self.ping_answered = 0
                self.events_to_send: queue.Queue[wsproto.events.Event] = queue.Queue()

            def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                while not self._should_close:
                    try:
                        event = self.events_to_send.get_nowait()
                        self.ping_answered += 1
                        return self.connection.send(event)
                    except queue.Empty:
                        pass
                raise httpcore.ReadError()

            def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                self.connection.receive_data(buffer)
                for event in self.connection.events():
                    if isinstance(event, wsproto.events.Ping):
                        self.ping_received += 1
                        self.events_to_send.put(event.response())

            def close(self) -> None:
                self._should_close = True

        stream = MockNetworkStream()
        websocket_session = WebSocketSession(
            stream,
            keepalive_ping_interval_seconds=0.1,
            keepalive_ping_timeout_seconds=0.1,
        )
        await asyncio.sleep(0.2)
        websocket_session.close()

        assert stream.ping_received >= 1
        assert stream.ping_answered >= 1

    async def test_keepalive_ping_timeout(self):
        class MockNetworkStream(NetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )
                self._should_close = False

            def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                while not self._should_close:
                    time.sleep(0.1)
                raise httpcore.ReadError()

            def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                pass

            def close(self) -> None:
                self._should_close = True

        stream = MockNetworkStream()
        with pytest.raises(WebSocketNetworkError):
            websocket_session = WebSocketSession(
                stream,
                keepalive_ping_interval_seconds=0.1,
                keepalive_ping_timeout_seconds=0.1,
            )
            websocket_session.receive()

    async def test_async_keepalive_ping(self):
        class MockAsyncNetworkStream(AsyncNetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )
                self._should_close = False
                self.ping_received = 0
                self.ping_answered = 0
                self.events_to_send: asyncio.Queue[
                    wsproto.events.Event
                ] = asyncio.Queue()

            async def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                while not self._should_close:
                    try:
                        event = self.events_to_send.get_nowait()
                        self.ping_answered += 1
                        return self.connection.send(event)
                    except asyncio.QueueEmpty:
                        await asyncio.sleep(0.1)
                raise httpcore.ReadError()

            async def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                self.connection.receive_data(buffer)
                for event in self.connection.events():
                    if isinstance(event, wsproto.events.Ping):
                        self.ping_received += 1
                        await self.events_to_send.put(event.response())

            async def aclose(self) -> None:
                self._should_close = True

        stream = MockAsyncNetworkStream()
        websocket_session = AsyncWebSocketSession(
            stream,
            keepalive_ping_interval_seconds=0.1,
            keepalive_ping_timeout_seconds=0.1,
        )
        await asyncio.sleep(0.3)
        await websocket_session.close()

        assert stream.ping_received >= 1
        assert stream.ping_answered >= 1

    async def test_async_keepalive_ping_timeout(self):
        class MockAsyncNetworkStream(AsyncNetworkStream):
            def __init__(self) -> None:
                self.connection = wsproto.connection.Connection(
                    wsproto.connection.ConnectionType.SERVER
                )
                self._should_close = False

            async def read(
                self, max_bytes: int, timeout: typing.Optional[float] = None
            ) -> bytes:
                while not self._should_close:
                    await asyncio.sleep(0.1)
                raise httpcore.ReadError()

            async def write(
                self, buffer: bytes, timeout: typing.Optional[float] = None
            ) -> None:
                pass

            async def aclose(self) -> None:
                self._should_close = True

        stream = MockAsyncNetworkStream()
        with pytest.raises(WebSocketNetworkError):
            websocket_session = AsyncWebSocketSession(
                stream,
                keepalive_ping_interval_seconds=0.1,
                keepalive_ping_timeout_seconds=0.1,
            )
            await websocket_session.receive()


@pytest.mark.asyncio
async def test_ping_pong(server_factory: ServerFactoryFixture):
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            await websocket.receive_text()
        except StarletteWebSocketDisconnect:
            pass

    with server_factory(websocket_endpoint) as socket:
        with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
            with connect_ws("http://socket/ws", client) as ws:
                ping_callback = ws.ping()
                result = ping_callback.wait()
                assert result is True

        async with httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(uds=socket)
        ) as aclient:
            async with aconnect_ws("http://socket/ws", aclient) as aws:
                aping_callback = await aws.ping()
                aresult = await aping_callback.wait()
                assert aresult is True


@pytest.mark.asyncio
async def test_send_close(server_factory: ServerFactoryFixture):
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            await websocket.receive_text()
        except StarletteWebSocketDisconnect:
            pass

    with server_factory(websocket_endpoint) as socket:
        with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
            with connect_ws("http://socket/ws", client):
                pass

        async with httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(uds=socket)
        ) as aclient:
            async with aconnect_ws("http://socket/ws", aclient):
                pass


@pytest.mark.asyncio
async def test_receive_close(server_factory: ServerFactoryFixture):
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        await asyncio.sleep(0.1)  # FIXME: see #7
        await websocket.close()

    with server_factory(websocket_endpoint) as socket:
        with httpx.Client(transport=httpx.HTTPTransport(uds=socket)) as client:
            with connect_ws("http://socket/ws", client) as ws:
                with pytest.raises(WebSocketDisconnect):
                    ws.receive()

        async with httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(uds=socket)
        ) as aclient:
            async with aconnect_ws("http://socket/ws", aclient) as aws:
                with pytest.raises(WebSocketDisconnect):
                    await aws.receive()


@pytest.mark.asyncio
async def test_default_httpx_client():
    mock_context = contextlib.ExitStack()
    with patch(
        "httpx_ws._api._connect_ws", return_value=mock_context
    ) as mock_connect_ws:
        with connect_ws("http://socket/ws"):
            pass
    mock_connect_ws.assert_called_once()
    httpx_client = mock_connect_ws.call_args[1]["client"]
    assert isinstance(httpx_client, httpx.Client)
    assert httpx_client.is_closed

    mock_async_context = contextlib.AsyncExitStack()
    with patch(
        "httpx_ws._api._aconnect_ws", return_value=mock_async_context
    ) as mock_aconnect_ws:
        async with aconnect_ws("http://socket/ws"):
            pass
    mock_aconnect_ws.assert_called_once()
    httpx_client = mock_aconnect_ws.call_args[1]["client"]
    assert isinstance(httpx_client, httpx.AsyncClient)
    assert httpx_client.is_closed


@pytest.mark.asyncio
async def test_subprotocol():
    def handler(request):
        assert (
            request.headers["sec-websocket-protocol"]
            == "custom_protocol, unsupported_protocol"
        )

        return httpx.Response(
            101,
            headers={"sec-websocket-protocol": "custom_protocol"},
            extensions={"network_stream": MagicMock()},
        )

    def async_handler(request):
        assert (
            request.headers["sec-websocket-protocol"]
            == "custom_protocol, unsupported_protocol"
        )

        network_stream = MagicMock()
        async_method_return_value = asyncio.Future()
        async_method_return_value.set_result(MagicMock())
        network_stream.write.return_value = async_method_return_value
        network_stream.aclose.return_value = async_method_return_value

        return httpx.Response(
            101,
            headers={"sec-websocket-protocol": "custom_protocol"},
            extensions={"network_stream": network_stream},
        )

    with httpx.Client(
        base_url="http://localhost:8000", transport=httpx.MockTransport(handler)
    ) as client:
        with connect_ws(
            "http://socket/ws",
            client,
            subprotocols=["custom_protocol", "unsupported_protocol"],
        ) as ws:
            assert ws.subprotocol == "custom_protocol"

    async with httpx.AsyncClient(
        base_url="http://localhost:8000", transport=httpx.MockTransport(async_handler)
    ) as client:
        async with aconnect_ws(
            "http://socket/ws",
            client,
            subprotocols=["custom_protocol", "unsupported_protocol"],
        ) as aws:
            assert aws.subprotocol == "custom_protocol"
