import os
import joblib
import pandas as pd

from src.config import MODEL_DIR
from src.weather import Weather

# The crop model was trained on MONTHLY-scale rainfall (about 20-300 mm).
# District data is ANNUAL, so we divide by 12. Set to 1 if your training data used annual values.
RAIN_DIVISOR = 12


class Recommendation:

    def __init__(self):
        self.weather = Weather()
        self.crop_model = joblib.load(os.path.join(MODEL_DIR, "crop_model.pkl"))
        self.yield_model = joblib.load(os.path.join(MODEL_DIR, "yield_model.pkl"))

        # Exact labels the yield model was trained on (e.g. 'Kharif     ' has trailing spaces)
        enc = self.yield_model.named_steps["preprocessor"].named_transformers_["cat"]
        self.labels = [{str(v).strip().upper(): v for v in cats} for cats in enc.categories_]

    def _label(self, i, value):
        return self.labels[i].get(str(value).strip().upper(), value)

    def recommend_crop(self, N, P, K, temperature, humidity, ph, state, district):
        rainfall = self.weather.get_rainfall(state, district)
        if rainfall is None:
            raise ValueError("Rainfall not found for this State/District.")
        sample = pd.DataFrame([{
            "N": N, "P": P, "K": K, "temperature": temperature,
            "humidity": humidity, "ph": ph, "rainfall": rainfall / RAIN_DIVISOR,
        }])
        return self.crop_model.predict(sample)[0], rainfall

    def predict_yield(self, state, district, crop, season, area):
        rainfall = self.weather.get_rainfall(state, district)
        sample = pd.DataFrame([{
            "State": self._label(0, state),
            "District": self._label(1, district),
            "Crop": self._label(2, crop),
            "Season": self._label(3, season),
            "Area": area,
        }])
        return self.yield_model.predict(sample)[0], rainfall
