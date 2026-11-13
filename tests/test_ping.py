import pytest

from httpx_ws._ping import AsyncPingManager, PingManager


@pytest.mark.anyio
@pytest.mark.parametrize("manager_class", [PingManager, AsyncPingManager])
async def test_ack_ignores_unsolicited_and_duplicate_pongs(manager_class):
    manager = manager_class()
    ping_id, event = manager.create(b"ping")

    manager.ack(b"unsolicited")
    assert not event.is_set()

    manager.ack(bytearray(ping_id))
    assert event.is_set()
    manager.ack(ping_id)
