import pytest

@pytest.mark.asyncio
async def test_upyog_anoop():
    import upyog as upy

    assert await upy.anoop() == None
    assert await upy.anoop(foo = "bar") == None