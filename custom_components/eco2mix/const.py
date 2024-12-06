"""Constants for the éCO2mix integration."""

from datetime import timedelta

DOMAIN = "eco2mix"
DEFAULT_SCAN_INTERVAL = 5  # minutes
SCAN_INTERVAL = timedelta(minutes=DEFAULT_SCAN_INTERVAL)

POWER_MEGA_WATT = "MW"

# Sources definition for aggregates
RENEWABLE_SOURCES = ["wind", "solar", "hydraulic", "bioenergy"]
LOW_CARBON_SOURCES = [*RENEWABLE_SOURCES, "nuclear"]
ALL_PRODUCTION_SOURCES = [*LOW_CARBON_SOURCES, "gas", "coal", "fuel"]

STORAGE_VERSION = 1
STORAGE_KEY = "eco2mix_cache"
