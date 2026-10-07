import os
import joblib
import time
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.config import APY_FILE, MODEL_DIR

start = time.time()

print("Training Started...")
class YieldModel:

    def __init__(self):

        self.df = None
        self.pipeline = None

    def load_data(self):

     print("\nLoading APY Dataset...")

     self.df = pd.read_excel(APY_FILE)

    # Clean column names
     self.df.columns = self.df.columns.str.strip()

     print(self.df.columns.tolist())

     print(f"Rows Loaded : {len(self.df)}")

    def preprocess(self):
        print("Step 1 : Dropping Missing Values")
        self.df = self.df.dropna()
        self.df = self.df.sample(
            n=50000,
            random_state=42
        )
        print("Step 2 : Creating Features")
        X = self.df[
            [
                "State",
                "District",
                "Crop",
                "Season",
                "Area"
            ]
        ]

        y = self.df["Yield"]

        categorical = [
            "State",
            "District",
            "Crop",
            "Season"
        ]

        numerical = [
            "Area"
        ]

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "cat",
                    OneHotEncoder(handle_unknown="ignore"),
                    categorical
                ),
                (
                    "num",
                    "passthrough",
                    numerical
                )
            ]
        )
        print("Step 3 : Splitting Data")
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )
        print("Step 4 : Building Pipeline")
        self.pipeline = Pipeline(
            [
                ("preprocessor", preprocessor),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=30,
                        random_state=42,
                        n_jobs=-1,
                        verbose=1
                    )
                )
            ]
        )
        print("Step 5 : Training Model...")
        self.pipeline.fit(X_train, y_train)

        end = time.time()

        print(f"\nTraining Completed in {end-start:.2f} seconds")

        prediction = self.pipeline.predict(X_test)

        print("\nR2 Score :", r2_score(y_test, prediction))

        print(
            "Mean Absolute Error :",
            mean_absolute_error(y_test, prediction)
        )
        print("Training Finished!")

    def save(self):

        os.makedirs(MODEL_DIR, exist_ok=True)

        joblib.dump(
            self.pipeline,
            os.path.join(
                MODEL_DIR,
                "yield_model.pkl"
            )
        )

        print("\nYield Model Saved Successfully.")

    def run(self):

        self.load_data()

        self.preprocess()

        self.save()