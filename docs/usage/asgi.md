# Testing ASGI apps

You can use HTTPX WS to test WebSockets defined in an ASGI app, [just like you do with HTTPX for HTTP endpoints](https://www.python-httpx.org/async/#calling-into-python-web-apps).

For this, we've implemented a custom transport for HTTPX, `ASGIWebSocketTransport`. You need to instantiate a class of this transport and set it as parameter on your HTTPX client.

Let's say you have this Starlette app:

```py
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, WebSocketRoute


async def http_hello(request):
    return HTMLResponse("Hello World!")

async def ws_hello(websocket):
    await websocket.accept()
    await websocket.send_text("Hello World!")
    await websocket.close()


app = Starlette(
    routes=[
        Route("/http", http_hello),
        WebSocketRoute("/ws", ws_hello),
    ],
)
```

You can call it directly like this:

```py
import httpx
from httpx_ws import aconnect_ws
from httpx_ws.transport import ASGIWebSocketTransport

async with httpx.AsyncClient(transport=ASGIWebSocketTransport(app)) as client:
    http_response = await client.get("http://server/http")
    assert http_response.status_code == 200

    async with aconnect_ws("http://server/ws", client) as ws:
        message = await ws.receive_text()
        assert message == "Hello World!"
```

Notice that, in this case, you *must* pass the `client` instance to `aconnect_ws`. HTTP requests are handled normally.
