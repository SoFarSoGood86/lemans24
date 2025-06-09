import logging
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_API_KEY, CONF_SCAN_INTERVAL
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "LeMans 24h"
DEFAULT_SCAN = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN): cv.time_period
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config[CONF_NAME]
    api_key = config[CONF_API_KEY]
    interval = config[CONF_SCAN_INTERVAL]

    client = LeMans24Client(api_key)

    sensors = [
        TotalCarsSensor(client, name),
        LeaderSensor(client, name)
    ]
    add_entities(sensors, update_before_add=True)

    def update(event_time):
        for sensor in sensors:
            sensor.schedule_update_ha_state(True)

    hass.helpers.event.track_time_interval(update, interval)

class LeMans24Client:
    def __init__(self, api_key):
        self.api_key = api_key
        self._data = None

    def update(self):
        url = f"https://fiawec.alkamelsystems.com/api/live?apikey={self.api_key}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        self._data = r.json()

    @property
    def data(self):
        if self._data is None:
            self.update()
        return self._data

class TotalCarsSensor(Entity):
    def __init__(self, client, name):
        self.client = client
        self._name = f"{name} - Total Cars"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        cars = self.client.data.get("cars", {})
        return len(cars)

class LeaderSensor(Entity):
    def __init__(self, client, name):
        self.client = client
        self._name = f"{name} - Leader"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        cars = self.client.data.get("cars", {})
        if not cars:
            return None
        leader = min(cars.values(), key=lambda c: c.get("position", float('inf')))
        return f"Car #{leader.get('number')} – {leader.get('team')}"