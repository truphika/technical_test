import pytest

from api.entities.point import DecimalDegreePoint

@pytest.fixture
def mock_correct_data():
    return {
        "features": [
            {
                "geometry": {"coordinates": [2.378185, 48.898595]},
            }
        ]
    }

@pytest.fixture
def mock_no_data_response():
    return {
        "features": []
    }


@pytest.fixture
def site_paris():
    return {"Operateur": "Orange","x": 651953,"y": 6861887,"2G": 1,"3G": 1,"4G": 1}

@pytest.fixture
def site_marseille():
    return {"Operateur": "Orange","x": 893330,"y": 6249763,"2G": 1,"3G": 1,"4G": 1}

@pytest.fixture
def point_close():
    return DecimalDegreePoint(48.856594, 2.312849)

@pytest.fixture
def point_out_3g_range():
    return DecimalDegreePoint(48.794238, 2.265832)

@pytest.fixture
def point_out_4g_range():
    return DecimalDegreePoint(48.752682, 2.202318)

@pytest.fixture
def point_out_2g_range():
    return DecimalDegreePoint(0, 0)