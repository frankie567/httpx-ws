# Client

In addition to the function-based APIs `connect_ws` and `aconnect_ws`, `httpx-ws` also provides class-based APIs with `WebSocketClient` and `AsyncWebSocketClient`.

**Sync**

```py
import httpx
from httpx_ws import WebSocketClient

with httpx.Client() as client:
    ws_client = WebSocketClient(client)
    with ws_client.connect("http://localhost:8000/ws") as ws:
        message = ws.receive_text()
        print(message)
        ws.send_text("Hello!")
```

**Async**

```py
import httpx
from httpx_ws import AsyncWebSocketClient

async with httpx.AsyncClient() as client:
    ws_client = AsyncWebSocketClient(client)
    async with ws_client.connect("http://localhost:8000/ws") as ws:
        message = await ws.receive_text()
        print(message)
        await ws.send_text("Hello!")
```

**Usage Example**

The WebSocketClient class APIs are particularly useful for libraries and applications using dependency injection patterns:

```py
import httpx
from httpx_ws import AsyncWebSocketClient

# Your service SDK
class MyServiceSDK:
    def __init__(self, websocket_client: AsyncWebSocketClient) -> None:
        self._websocket_client = websocket_client

    async def hello(self) -> str:
        async with self._websocket_client.connect("ws://localhost:8000/ws") as ws:
            await ws.send_text("Hello!")
            response = await ws.receive_text()
            return response

# Usage example
async def main() -> None:
    async with httpx.AsyncClient() as client:
        ws_client = AsyncWebSocketClient(client)

        service = MyServiceSDK(ws_client)
        response = await service.hello()
        print(f"Received: {response}")
```
