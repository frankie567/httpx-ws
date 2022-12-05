import httpx
from httpx_ws import connect_ws


def my_client():
    with httpx.Client() as client:
        with connect_ws("http://localhost:8000/ws", client) as ws:
            text = ws.receive_text()
            return text


if __name__ == "__main__":
    print(my_client())