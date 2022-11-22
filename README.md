# httpx-ws

WebSockets support for HTTPX

[![build](https://github.com/frankie567/httpx-ws/workflows/Build/badge.svg)](https://github.com/frankie567/httpx-ws/actions)
[![codecov](https://codecov.io/gh/frankie567/httpx-ws/branch/main/graph/badge.svg?token=fL49kIvrj6)](https://codecov.io/gh/frankie567/httpx-ws)
[![PyPI version](https://badge.fury.io/py/httpx-ws.svg)](https://badge.fury.io/py/httpx-ws)
[![Downloads](https://pepy.tech/badge/httpx-ws)](https://pepy.tech/project/httpx-ws)

<p align="center">
<a href="https://github.com/sponsors/frankie567"><img src="https://md-btn.deta.dev/button.svg?text=Buy%20me%20a%20coffee%20%E2%98%95%EF%B8%8F&bg=ef4444&w=200&h=50"></a>
</p>


## Installation

> Not released on PyPI yet 😅

```bash
pip install httpx-ws
```

## Quickstart

`httpx-ws` provides `connect_ws` and `aconnect_ws` to help connecting and communication with WebSockets. The resulting `WebSocketSession`/`AsyncWebSocketSession` object provides helpers to send and receive messages in the WebSocket.

**Sync**

```py
import httpx
from httpx_ws import connect_ws

with httpx.Client() as client:
    with connect_ws(client, "http://localhost:8000/ws") as ws:
        message = ws.receive_text()
        print(message)
        ws.send_text("Hello!")
```

**Async**

```py
import httpx
from httpx_ws import aconnect_ws

async with httpx.AsyncClient() as client:
    async with aconnect_ws(client, "http://localhost:8000/ws") as ws:
        message = await ws.receive_text()
        print(message)
        await ws.send_text("Hello!")
```

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
