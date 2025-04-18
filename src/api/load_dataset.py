import csv

from api.constants import DATASET_PATH


def load_dataset_file():
    with open(DATASET_PATH, "r") as dataset_file:
        reader = csv.DictReader(dataset_file)
        dataset = []
        for row in reader:
            for key in row:
                if key in ["x", "y", "2G", "3G", "4G"]:
                    row[key] = float(row[key])
            dataset.append(row)

        return dataset
