import asyncio
from typing import Optional
from aiohttp import ClientSession

from api.constants import GEOCODING_API_URL
from api.entities.point import DecimalDegreePoint
from api.logger import logger


async def handle_geocoding(session: ClientSession, address: str):
    params = {
        "q": address,
        "autocomplete": 0,
        "index": "address",
        "limit": 1,
        "returntruegeometry": "false",
    }

    async with session.get(GEOCODING_API_URL, params=params) as geocoding_response:
        geocoding_response.raise_for_status()
        json_response = await geocoding_response.json()

        if len(json_response["features"]) == 0:
            logger.debug(f"No data from geocoding api for '{address}'")
            logger.debug(f"Full data: {json_response}")
            raise Exception("No data from geocoding api for address: " + address)

        long, lat = json_response["features"][0]["geometry"]["coordinates"]

        logger.debug(
            f"Geocoding successful, got lat: {lat}, long: {long} for '{address}'"
        )
        return DecimalDegreePoint(lat=lat, long=long)


async def handle_geocoding_with_throttle(
    session: ClientSession, address: str, semaphore: Optional[asyncio.Semaphore]
) -> DecimalDegreePoint:
    if semaphore:
        async with semaphore:
            return await handle_geocoding(session, address)
    else:
        return await handle_geocoding(session, address)


async def handle_geocoding_batch(
    addresses: dict[str, str], semaphore: Optional[asyncio.Semaphore]
) -> dict[str, DecimalDegreePoint]:
    logger.debug(
        f"Geocoding request incoming with {len(addresses)} addresses")

    async with ClientSession() as session:
        tasks = [
            handle_geocoding_with_throttle(session, address, semaphore)
            for address in addresses.values()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {
            address_id: result
            for address_id, result in zip(addresses.keys(), results)
            if not isinstance(result, BaseException)
        }
