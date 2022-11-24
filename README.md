# httpx-ws
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

WebSockets support for HTTPX

[![build](https://github.com/frankie567/httpx-ws/workflows/Build/badge.svg)](https://github.com/frankie567/httpx-ws/actions)
[![codecov](https://codecov.io/gh/frankie567/httpx-ws/branch/main/graph/badge.svg?token=fL49kIvrj6)](https://codecov.io/gh/frankie567/httpx-ws)
[![PyPI version](https://badge.fury.io/py/httpx-ws.svg)](https://badge.fury.io/py/httpx-ws)
[![Downloads](https://pepy.tech/badge/httpx-ws)](https://pepy.tech/project/httpx-ws)

<p align="center">
<a href="https://github.com/sponsors/frankie567"><img src="https://md-btn.deta.dev/button.svg?text=Buy%20me%20a%20coffee%20%E2%98%95%EF%B8%8F&bg=ef4444&w=200&h=50"></a>
</p>


## Installation

> ⚠️ This is a very young project. Expect bugs 🐛

```bash
pip install httpx-ws
```

## Quickstart

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

with httpx.AsyncClient() as client:
    async with aconnect_ws("http://localhost:8000/ws", client) as ws:
        message = await ws.receive_text()
        print(message)
        await ws.send_text("Hello!")
```

## Testing ASGI apps

You can use `httpx_ws` to test WebSockets defined in an ASGI app, [just like you do with HTTPX for HTTP endpoints](https://www.python-httpx.org/async/#calling-into-python-web-apps).

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

## Development

### Setup environment

We use [Hatch](https://hatch.pypa.io/latest/install/) to manage the development environment and production build. Ensure it's installed on your system.

### Run unit tests

You can run all the tests with:

```bash
hatch run test
```

### Format the code

Execute the following command to apply `isort` and `black` formatting:

```bash
hatch run lint
```

## License

This project is licensed under the terms of the MIT license.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="http://francoisvoron.com"><img src="https://avatars.githubusercontent.com/u/1144727?v=4?s=100" width="100px;" alt="François Voron"/><br /><sub><b>François Voron</b></sub></a><br /><a href="#maintenance-frankie567" title="Maintenance">🚧</a> <a href="https://github.com/frankie567/httpx-ws/commits?author=frankie567" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!