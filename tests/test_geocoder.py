import re
from aiohttp import ClientSession
from aioresponses import aioresponses
import pytest
from api.constants import GEOCODING_API_URL
from api.services.geocoder import handle_geocoding
from api.entities.point import DecimalDegreePoint

@pytest.mark.asyncio
async def test_handle_geocoding_success(mock_correct_data):
    with aioresponses() as mocked:
        mocked.get(
            re.compile(f'{GEOCODING_API_URL}.*$'),
            payload=mock_correct_data,
            status=200,
        )

        async with ClientSession() as session:
            result = await handle_geocoding(session, "addr")

    assert isinstance(result, DecimalDegreePoint)
    assert result.lat == 48.898595
    assert result.long == 2.378185

@pytest.mark.asyncio
async def test_handle_geocoding_no_data(mock_no_data_response):
    with aioresponses() as mocked:
        mocked.get(
            re.compile(f'{GEOCODING_API_URL}.*$'),
            payload=mock_no_data_response,
            status=200,
        )

        async with ClientSession() as session:
            with pytest.raises(Exception, match=f"No data from geocoding api for address: addr"):
                await handle_geocoding(session, "addr")

@pytest.mark.asyncio
async def test_handle_geocoding_api_400():
    with aioresponses() as mocked:
        mocked.get(
            re.compile(f'{GEOCODING_API_URL}.*$'),
            status=404,
        )

        async with ClientSession() as session:
            with pytest.raises(Exception):
                await handle_geocoding(session, "addr")