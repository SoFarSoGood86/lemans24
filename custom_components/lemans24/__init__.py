async def async_setup(hass, config):
    hass.data.setdefault("lemans24", {})
    return True