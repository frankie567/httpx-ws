# Subprotocols

WebSocket support the concept of [Subprotocols](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers#subprotocols), which is a way to agree on a specific communication formalism between the client and the server.

HTTPX WS allows you to send a list of subprotocols you support when opening the connection with the server. Then, you'll be able to read the subprotocol the server has accepted to conform with.

**Sync**

```py
from httpx_ws import connect_ws

with connect_ws(
    "http://localhost:8000/ws",
    subprotocols=["my_protocol_1", "my_protocol_2"],
) as ws:
    print(f"Accepted subprotocol {ws.subprotocol}")
```

**Async**

```py
from httpx_ws import aconnect_ws

async with aconnect_ws(
    "http://localhost:8000/ws",
    subprotocols=["my_protocol_1", "my_protocol_2"],
) as ws:
    print(f"Accepted subprotocol {ws.subprotocol}")
```
