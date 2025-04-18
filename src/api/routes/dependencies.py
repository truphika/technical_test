import asyncio

from fastapi import Request

from api.services.coverage_checker import CoverageChecker


def get_coverage_checker(request: Request) -> CoverageChecker:
    return request.app.state.coverage_checker


def get_semaphore(request: Request) -> asyncio.Semaphore:
    return request.app.state.semaphore
