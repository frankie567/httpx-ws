# Quickstart

`httpx-ws` provides `connect_ws` and `aconnect_ws` to help connecting and communication with WebSockets. The resulting `WebSocketSession`/`AsyncWebSocketSession` object provides helpers to send and receive messages in the WebSocket.

**Sync**

```py
from httpx_ws import connect_ws

with connect_ws("http://localhost:8000/ws") as ws:
    message = ws.receive_text()
    print(message)
    ws.send_text("Hello!")
```

**Async**

```py
from httpx_ws import aconnect_ws

async with aconnect_ws("http://localhost:8000/ws") as ws:
    message = await ws.receive_text()
    print(message)
    await ws.send_text("Hello!")
```

You can also pass an `httpx.Client`/`httpx.AsyncClient` if you want to customize parameters or benefit from connection pooling:

**Sync**

```py
import httpx
from httpx_ws import connect_ws

with httpx.Client() as client:
    with connect_ws("http://localhost:8000/ws", client) as ws:
        message = ws.receive_text()
        print(message)
        ws.send_text("Hello!")
```

**Async**

```py
import httpx
from httpx_ws import aconnect_ws

async with httpx.AsyncClient() as client:
    async with aconnect_ws("http://localhost:8000/ws", client) as ws:
        message = await ws.receive_text()
        print(message)
        await ws.send_text("Hello!")
```
