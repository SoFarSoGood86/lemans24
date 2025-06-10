import logging
import asyncio
from datetime import timedelta
import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.const import CONF_API_KEY

from .const import DOMAIN, API_URL

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    api_key = config.get(CONF_API_KEY)
    if not api_key:
        _LOGGER.error("API key is required")
        return

    coordinator = LeMansDataUpdateCoordinator(hass, api_key)
    await coordinator.async_config_entry_first_refresh()

    sensors = []

    sensors.append(LeMansRaceStatusSensor(coordinator))
    sensors.append(LeMansRemainingTimeSensor(coordinator))
    sensors.append(LeMansTotalCarsSensor(coordinator))
    sensors.append(LeMansCarsInPitSensor(coordinator))
    sensors.append(LeMansLeaderSensor(coordinator))
    sensors.append(LeMansWeatherSensor(coordinator))

    for car in coordinator.data.get("cars", []):
        sensors.append(LeMansCarSensor(coordinator, car))

    async_add_entities(sensors, True)

class LeMansDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_key):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.api_key = api_key
        self.data = {}

    async def _async_update_data(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(API_URL, headers=headers) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error fetching data: {response.status}")
                        data = await response.json()
                        return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

class LeMansRaceStatusSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "LeMans 24h Race Status"
        self._attr_unique_id = "lemans24_race_status"

    @property
    def native_value(self):
        return self.coordinator.data.get("race_status")

class LeMansRemainingTimeSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "LeMans 24h Remaining Time"
        self._attr_unique_id = "lemans24_remaining_time"

    @property
    def native_value(self):
        return self.coordinator.data.get("remaining_time")

class LeMansTotalCarsSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "LeMans 24h Total Cars"
        self._attr_unique_id = "lemans24_total_cars"

    @property
    def native_value(self):
        return self.coordinator.data.get("total_cars")

class LeMansCarsInPitSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "LeMans 24h Cars in Pit"
        self._attr_unique_id = "lemans24_cars_in_pit"

    @property
    def native_value(self):
        return self.coordinator.data.get("cars_in_pit")

class LeMansLeaderSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "LeMans 24h Leader"
        self._attr_unique_id = "lemans24_leader"

    @property
    def native_value(self):
        return self.coordinator.data.get("leader")

class LeMansWeatherSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "LeMans 24h Weather"
        self._attr_unique_id = "lemans24_weather"

    @property
    def native_value(self):
        weather = self.coordinator.data.get("weather")
        if weather:
            return f"{weather.get('temp')}°C, {weather.get('humidity')}%, {weather.get('condition')}"
        return None

class LeMansCarSensor(SensorEntity):
    def __init__(self, coordinator, car_data):
        self.coordinator = coordinator
        self.car = car_data
        self._attr_name = f"LeMans 24h Car #{car_data['number']}"
        self._attr_unique_id = f"lemans24_car_{car_data['number']}"

    @property
    def native_value(self):
        return self.car.get("position")

    @property
    def extra_state_attributes(self):
        return {
            "team": self.car.get("team"),
            "laps": self.car.get("laps"),
            "last_lap_time": self.car.get("last_lap_time"),
            "best_lap_time": self.car.get("best_lap_time"),
            "status": self.car.get("status"),
        }
