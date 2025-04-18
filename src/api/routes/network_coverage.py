from fastapi import APIRouter, Body, Depends
import asyncio

from api.logger import logger
from api.services.coverage_checker import CoverageChecker
from api.services.address_coverage import get_addresses_coverage
from api.routes.dependencies import get_coverage_checker, get_semaphore

router = APIRouter()


@router.post(
    "/network_coverage",
    responses={
        200: {
            "description": "Get Coverage data for given addresses",
            "content": {
                "application/json": {
                    "example": {
                        "id": {
                            "Orange": {"2G": True, "3G": True, "4G": True},
                            "Free": {"2G": False, "3G": True, "4G": True},
                        }
                    }
                }
            },
        }
    },
)
async def get_network_coverage(
    addresses: dict[str, str] = Body(
        example={"id": "157 boulevard Mac Donald 75019 Paris"}
    ),
    coverage_checker: CoverageChecker = Depends(get_coverage_checker),
    semaphore: asyncio.Semaphore = Depends(get_semaphore),
):
    coverages = await get_addresses_coverage(addresses, coverage_checker, semaphore)
    result = {}
    for address_id, coverage_list in coverages.items():
        all_operator_coverage = {}
        for operator_coverage in coverage_list:
            all_operator_coverage.update(operator_coverage.to_dict())
        result[address_id] = all_operator_coverage

    logger.info(f"Found result for request: {[idx for idx in result]}")
    return result
