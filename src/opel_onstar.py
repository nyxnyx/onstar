"""
Support of Opel OnStar online service. Might work also for other cars that 
are using OnStar.

"""

import asyncio
import logging


import voluptuous as vol

from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.const import (
            ATTR_BATTERY_LEVEL, CONF_PASSWORD, CONF_SCAN_INTERVAL, CONF_USERNAME, CONF_RESOURCES)

DOMAIN = 'opel_onstar'
DATA_KEY = DOMAIN

_LOGGER = logging.getLogger(__name__)
MIN_UPDATE_INTERVAL = timedelta(minutes=1)
DEFAULT_UPDATE_INTERVAL = timedelta(minutes=1)

CONF_UPDATE_INTERVAL = 'update_interval'
SIGNAL_VEHICLE_SEEN = '{}.vehicle_seen'.format(DOMAIN)

RESOURCES = {'position': ('device_tracker',),
             'lock': ('lock', 'Lock'),
             'odometer': ('sensor', 'Odometer', 'mdi:speedometer', 'km'),
             'fuel_amount': ('sensor', 'Fuel amount', 'mdi:gas-station', 'L'),
             'fuel_amount_level': (
                 'sensor', 'Fuel level', 'mdi:water-percent', '%'),
             'average_fuel_consumption': (
                 'sensor', 'Fuel consumption', 'mdi:gas-station', 'L/100 km'),
             'distance_to_empty': ('sensor', 'Range', 'mdi:ruler', 'km'),
             'washer_fluid_level': ('binary_sensor', 'Washer fluid'),
             'brake_fluid': ('binary_sensor', 'Brake Fluid'),
             'service_warning_status': ('binary_sensor', 'Service'),
             'bulb_failures': ('binary_sensor', 'Bulbs'),
             'doors': ('binary_sensor', 'Doors'),
             'windows': ('binary_sensor', 'Windows')}

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_PIN): cv.string,
        vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): (
            vol.All(cv.time_period, vol.Clamp(min=MIN_UPDATE_INTERVAL))),
        vol.Optional(CONF_NAME, default={}): vol.Schema(
            {cv.slug: cv.string}),
        vol.Optional(CONF_RESOURCES): vol.All(
            cv.ensure_list, [vol.In(RESOURCES)]),
        vol.Optional(CONF_REGION): cv.string,
        vol.Optional(CONF_SERVICE_URL): cv.string,
        vol.Optional(CONF_SCANDINAVIAN_MILES, default=False): cv.boolean,
    }),
}, extra=vol.ALLOW_EXTRA)

