# AgriSense – Crop Recommendation & Yield Prediction

## Folder guide
| Path | What it is |
|---|---|
| `main.py`, `gui.py` | Desktop app (Tkinter). Run `python main.py` |
| `src/` | ML code: training, data loading, prediction logic |
| `models/` | Trained models (`crop_model.pkl`, `yield_model.pkl`) |
| `datasets/` | Put your 3 dataset files here (see PUT_YOUR_DATASETS_HERE.txt) |
| `docs/` | Website (live demo) for GitHub Pages |
| `train_models.py` | Retrain both models |
| `export_models.py` | Convert models for the website |

## Run desktop app
    pip install -r requirements.txt
    python main.py

## Live demo on GitHub Pages
Repo -> Settings -> Pages -> Branch `main`, folder **/docs** -> Save.
`models/yield_model.pkl` is 102 MB (GitHub limit is 100 MB), so it is in `.gitignore`; the website uses `docs/data/*.bin` instead.
After retraining: `python train_models.py` then `python export_models.py`.
