import asyncio
from typing import Optional

from api.services.coverage_checker import CoverageChecker
from api.services.geocoder import handle_geocoding_batch
from api.entities.network_coverage import NetworkCoverage


async def get_addresses_coverage(
    addresses: dict[str, str],
    coverage_checker: CoverageChecker,
    semaphore: Optional[asyncio.Semaphore],
) -> dict[str, list[NetworkCoverage]]:
    points = await handle_geocoding_batch(addresses, semaphore)
    result = {
        point_index: coverage_checker.get_point_coverage(point_data)
        for point_index, point_data in points.items()
    }

    return result
