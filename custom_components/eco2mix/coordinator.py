"""DataUpdateCoordinator for eco2mix."""

from datetime import datetime, timedelta
import logging
from typing import Any

import pytz
import requests

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    ALL_PRODUCTION_SOURCES,
    DOMAIN,
    LOW_CARBON_SOURCES,
    RENEWABLE_SOURCES,
    STORAGE_KEY,
    STORAGE_VERSION,
)

_LOGGER = logging.getLogger(__name__)


class Eco2mixDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching eco2mix data."""

    def __init__(self, hass: HomeAssistant, scan_interval: int) -> None:
        """Initialize."""
        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=timedelta(minutes=scan_interval)
        )
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._last_timestamp = None
        self._cached_data = None
        self._failed_updates = 0
        self._last_successful_update = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""
        try:
            data = await self.hass.async_add_executor_job(self._get_data)

            if data is None:
                _LOGGER.error("No data received from API")
                return await self._handle_api_failure()

            if self._last_timestamp == data.get("timestamp"):
                _LOGGER.debug("Data hasn't changed since last update")
                return self.data if self.data else data

            # Reset failure counter on successful update
            self._failed_updates = 0
            self._last_successful_update = dt_util.utcnow()
            self._last_timestamp = data.get("timestamp")

            # Store successful data
            await self._store.async_save(data)
            self._cached_data = data

            return data

        except requests.exceptions.RequestException as err:
            self._failed_updates += 1
            _LOGGER.error(
                "API request failed: %s (Attempt %d)", err, self._failed_updates
            )
            return await self._handle_api_failure()

        except Exception as err:
            self._failed_updates += 1
            _LOGGER.exception("Unexpected error: %s", err)
            return await self._handle_api_failure()

    async def _handle_api_failure(self) -> dict[str, Any]:
        """Handle API failures by using cached data."""
        if self._failed_updates == 1:
            _LOGGER.warning("First API failure, loading cached data")
        elif self._failed_updates % 5 == 0:
            _LOGGER.error(
                "API has been unavailable for %d attempts (%s since last success)",
                self._failed_updates,
                dt_util.utcnow() - self._last_successful_update
                if self._last_successful_update
                else "never",
            )

        if not self._cached_data:
            self._cached_data = await self._store.async_load()

        if self._cached_data:
            _LOGGER.debug(
                "Using cached data from %s", self._cached_data.get("timestamp")
            )
            return self._cached_data

        raise UpdateFailed("No cached data available")

    def _get_data(self) -> dict[str, Any]:
        """Get the latest data from eco2mix."""
        paris_tz = pytz.timezone("Europe/Paris")
        current_time = datetime.now(paris_tz)
        date_str = current_time.strftime("%Y/%m/%d")

        url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records"
        params = {
            "limit": 100,
            "refine": f"date_heure:{date_str}",
            "order_by": "date_heure desc",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data["results"]:
                _LOGGER.error("No data available in API response")
                return None

            current_data = None
            for entry in data["results"]:
                if entry["consommation"] is not None:
                    current_data = entry
                    break

            if not current_data:
                _LOGGER.error("No valid data found in API response")
                return None

            return self._process_data(current_data)

        except requests.exceptions.Timeout:
            _LOGGER.error("API request timed out")
            raise
        except requests.exceptions.RequestException as err:
            _LOGGER.error("API request failed: %s", err)
            raise

    def _process_data(self, current_data: dict[str, Any]) -> dict[str, Any]:
        """Process the raw API data."""
        processed_data = {
            "consumption": current_data["consommation"],
            "nuclear": current_data["nucleaire"],
            "wind": current_data["eolien"],
            "solar": current_data["solaire"],
            "hydraulic": current_data["hydraulique"],
            "bioenergy": current_data["bioenergies"],
            "gas": current_data["gaz"],
            "coal": current_data["charbon"],
            "fuel": current_data["fioul"],
            "timestamp": datetime.fromisoformat(current_data["date_heure"]),
            "pumping": abs(current_data["pompage"]) if current_data["pompage"] else 0,
        }

        total_production = sum(
            processed_data[source]
            for source in ALL_PRODUCTION_SOURCES
            if processed_data.get(source) is not None
        )
        processed_data["total_production"] = total_production

        exchanges = current_data.get("ech_physiques", 0)
        processed_data["import"] = max(0, exchanges)
        processed_data["export"] = abs(min(0, exchanges))

        processed_data["renewable"] = sum(
            processed_data[source]
            for source in RENEWABLE_SOURCES
            if processed_data.get(source) is not None
        )
        processed_data["low_carbon"] = sum(
            processed_data[source]
            for source in LOW_CARBON_SOURCES
            if processed_data.get(source) is not None
        )

        total_production_mw = total_production
        if total_production_mw > 0:
            for source in ALL_PRODUCTION_SOURCES:
                source_value_mw = (
                    processed_data[source]
                    if processed_data.get(source) is not None
                    else 0
                )
                processed_data[f"{source}_percentage"] = (
                    source_value_mw / total_production_mw * 100
                )
            processed_data["renewable_percentage"] = (
                (processed_data["renewable"]) / total_production_mw * 100
            )
            processed_data["low_carbon_percentage"] = (
                (processed_data["low_carbon"]) / total_production_mw * 100
            )

        return processed_data

    @staticmethod
    def _to_kw(value: float | None) -> float | None:
        """Convert MW to kW."""
        return value
