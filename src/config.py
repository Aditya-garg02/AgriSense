import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_DIR = os.path.join(BASE_DIR, "datasets")
MODEL_DIR = os.path.join(BASE_DIR, "models")
CLEAN_DIR = os.path.join(BASE_DIR, "cleaned_data")

APY_FILE = os.path.join(DATASET_DIR, "APY.xlsx")
SOIL_FILE = os.path.join(DATASET_DIR, "soil_data.xlsx")
CROP_FILE = os.path.join(DATASET_DIR, "crop_requirements.xlsx")
RAIN_FILE = os.path.join(DATASET_DIR, "district_rainfall.csv")