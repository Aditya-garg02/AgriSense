import pandas as pd
from src.config import APY_FILE, SOIL_FILE, CROP_FILE, RAIN_FILE


class DataLoader:

    def __init__(self):
        self.apy = None
        self.soil = None
        self.crop = None
        self.rain = None

    def load_all(self):

        print("\nLoading datasets...\n")

        self.apy = pd.read_excel(APY_FILE)

        self.soil = pd.read_excel(SOIL_FILE)

        self.crop = pd.read_excel(CROP_FILE)

        self.rain = pd.read_csv(RAIN_FILE)

        print("All datasets loaded successfully.\n")

        return {
            "apy": self.apy,
            "soil": self.soil,
            "crop": self.crop,
            "rain": self.rain
        }