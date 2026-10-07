import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from src.config import SOIL_FILE, MODEL_DIR


class CropRecommendationModel:

    def __init__(self):

        self.data = None
        self.model = None

    def load_dataset(self):

        print("\nLoading Crop Recommendation Dataset...")

        self.data = pd.read_excel(SOIL_FILE)

        print("Dataset Loaded Successfully")

        print(self.data.head())

    def preprocess(self):

        print("\nPreparing Dataset...")

        X = self.data[
            [
                "N",
                "P",
                "K",
                "temperature",
                "humidity",
                "ph",
                "rainfall",
            ]
        ]

        y = self.data["label"]

        return train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y,
        )

    def train(self):

        X_train, X_test, y_train, y_test = self.preprocess()

        print("\nTraining Random Forest Model...")

        self.model = RandomForestClassifier(
            n_estimators=300,
            random_state=42,
        )

        self.model.fit(X_train, y_train)

        prediction = self.model.predict(X_test)

        accuracy = accuracy_score(y_test, prediction)

        print("\nModel Accuracy : {:.2f}%".format(accuracy * 100))

        print("\nClassification Report\n")

        print(classification_report(y_test, prediction))

    def save_model(self):

        os.makedirs(MODEL_DIR, exist_ok=True)

        joblib.dump(
            self.model,
            os.path.join(MODEL_DIR, "crop_model.pkl"),
        )

        print("\nModel Saved Successfully.")


def main():

    model = CropRecommendationModel()

    model.load_dataset()

    model.train()

    model.save_model()


if __name__ == "__main__":
    main()