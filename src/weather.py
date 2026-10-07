import os
import pandas as pd
from src.config import RAIN_FILE


class Weather:

    def __init__(self):
        if not os.path.exists(RAIN_FILE):
            raise FileNotFoundError(
                f"Rainfall file not found: {RAIN_FILE}\nPut district_rainfall.csv inside the 'datasets' folder.")
        self.df = pd.read_csv(RAIN_FILE)
        self.df.columns = self.df.columns.str.strip()
        self.df["STATE/UT"] = self.df["STATE/UT"].astype(str).str.upper().str.strip()
        self.df["DISTRICT"] = self.df["DISTRICT"].astype(str).str.upper().str.strip()

    def get_rainfall(self, state, district):
        state, district = state.upper().strip(), district.upper().strip()
        result = self.df[(self.df["STATE/UT"] == state) & (self.df["DISTRICT"] == district)]
        if len(result) == 0:
            return None
        return float(result.iloc[0]["ANNUAL"])
