import os
import joblib
from src.weather import Weather
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from src.config import SOIL_FILE, MODEL_DIR


class CropModel:

    def __init__(self):

        self.df = None
        self.model = None
        self.weather = Weather()

    def load_data(self):

        print("\nLoading Soil Dataset...")

        self.df = pd.read_excel(SOIL_FILE)

        print(f"Dataset Loaded ({len(self.df)} rows)")

    def prepare_data(self):

        X = self.df[
            [
                "N",
                "P",
                "K",
                "temperature",
                "humidity",
                "ph",
                "rainfall"
            ]
        ]

        y = self.df["label"]

        return train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

    def train(self):

        X_train, X_test, y_train, y_test = self.prepare_data()

        print("\nTraining Random Forest...\n")

        self.model = RandomForestClassifier(
            n_estimators=300,
            random_state=42
        )

        self.model.fit(X_train, y_train)

        prediction = self.model.predict(X_test)

        accuracy = accuracy_score(y_test, prediction)

        print(f"Accuracy : {accuracy*100:.2f}%")

        print()

        print(classification_report(y_test, prediction))

    def save(self):

        os.makedirs(MODEL_DIR, exist_ok=True)

        model_path = os.path.join(
            MODEL_DIR,
            "crop_model.pkl"
        )

        joblib.dump(self.model, model_path)

        print("\nModel Saved Successfully")
        print(model_path)

    def run(self):

        self.load_data()

        self.train()

        self.save()