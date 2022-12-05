import uvicorn
from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.routing import WebSocketRoute


async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("FOO")
    await websocket.close()


routes = [
    WebSocketRoute("/ws", endpoint=websocket_endpoint),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app)