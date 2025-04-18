import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.constants import MAX_CONCURRENT_REQUESTS
from api.load_dataset import load_dataset_file
from api.services.coverage_checker import CoverageChecker
from api.routes.network_coverage import router as network_coverage_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    dataset = load_dataset_file()
    coverage_checker = CoverageChecker(dataset=dataset)
    app.state.coverage_checker = coverage_checker
    app.state.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(network_coverage_router)
