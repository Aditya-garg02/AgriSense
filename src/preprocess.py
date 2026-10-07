import os

from src.config import CLEAN_DIR


class Preprocessor:

    def __init__(self, datasets):

        self.datasets = datasets

    def clean(self):

        print("\nCleaning datasets...\n")

        for key in self.datasets:

            df = self.datasets[key]

            df.columns = df.columns.str.strip()

            df.drop_duplicates(inplace=True)

            self.datasets[key] = df

        print("Cleaning completed.\n")

    def summary(self):

        print("\n========== DATA SUMMARY ==========\n")

        for name, df in self.datasets.items():

            print("=" * 60)

            print(name.upper())

            print("=" * 60)

            print("Shape :", df.shape)

            print("\nColumns")

            print(df.columns.tolist())

            print("\nMissing Values")

            print(df.isnull().sum())

            print()

    def save(self):

        os.makedirs(CLEAN_DIR, exist_ok=True)

        self.datasets["apy"].to_csv(
            os.path.join(CLEAN_DIR, "APY_clean.csv"),
            index=False
        )

        self.datasets["soil"].to_csv(
            os.path.join(CLEAN_DIR, "soil_clean.csv"),
            index=False
        )

        self.datasets["crop"].to_csv(
            os.path.join(CLEAN_DIR, "crop_clean.csv"),
            index=False
        )

        self.datasets["rain"].to_csv(
            os.path.join(CLEAN_DIR, "rain_clean.csv"),
            index=False
        )

        print("\nCleaned files saved.\n")