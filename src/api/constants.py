import os
from pathlib import Path


GEOCODING_API_URL = "https://data.geopf.fr/geocodage/search"
DATASET_PATH = os.getenv("DATASET_PATH", "data/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93_ver2.csv")

LOGS_DIR = Path("logs")
ENV = os.getenv("ENV", "PROD")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
MAX_CONCURRENT_REQUESTS = 10
