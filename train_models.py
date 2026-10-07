"""Retrain both models (needs the files inside /datasets). Run: python train_models.py"""
from src.train_crop_model import CropRecommendationModel
from src.yield_model import YieldModel

m = CropRecommendationModel(); m.load_dataset(); m.train(); m.save_model()
y = YieldModel(); y.run()
print("Models saved in /models. Now run: python export_models.py to refresh the website models.")
