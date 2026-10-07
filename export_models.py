"""Converts crop_model.pkl / yield_model.pkl into compact browser files.
Run:  python export_models.py   (from the project root; needs models/*.pkl)
If datasets/district_rainfall.csv exists, rainfall data is exported too."""
import os, json, struct, joblib, numpy as np, pandas as pd
M = os.environ.get("MODEL_DIR") or ("models" if os.path.exists("models/crop_model.pkl") else ".")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "data")

def pack(trees, leaf_fn, nclass):
    thr, right, feat, leaves, roots = [], [], [], [], []
    def walk(t, n):
        i = len(thr)
        if t.children_left[n] == -1:
            if leaf_fn is None: thr.append(float(t.value[n].ravel()[0])); right.append(0)
            else: thr.append(0.0); right.append(len(leaves) // nclass); leaves.extend(leaf_fn(t.value[n].ravel()))
            feat.append(-1); return
        thr.append(float(t.threshold[n])); right.append(0); feat.append(int(t.feature[n]))
        walk(t, t.children_left[n]); right[i] = len(thr); walk(t, t.children_right[n])
    for e in trees:
        roots.append(len(thr)); walk(e.tree_, 0)
    return thr, right, feat, leaves, roots

def write(path, thr, right, feat, leaves, roots, extra):
    feat = np.array(feat, np.int16); pad = (-len(feat)) % 2
    parts = [np.array(thr, np.float32), np.array(right, np.int32), np.array(leaves, np.float32),
             np.array(roots, np.int32), np.concatenate([feat, np.zeros(pad, np.int16)])]
    hdr = json.dumps({"n": len(thr), "l": len(leaves), "t": len(roots), **extra}).encode()
    hdr += b" " * ((-len(hdr)) % 4)
    with open(path, "wb") as f:
        f.write(struct.pack("<I", len(hdr))); f.write(hdr)
        for p in parts: f.write(p.tobytes())

crop = joblib.load(f"{M}/crop_model.pkl"); C = len(crop.classes_)
norm = lambda v: v / v.sum()
write(f"{OUT}/crop.bin", *pack(crop.estimators_, norm, C), {"c": C})

yl = joblib.load(f"{M}/yield_model.pkl")
oh = yl.named_steps["preprocessor"].named_transformers_["cat"]
write(f"{OUT}/yield.bin", *pack(yl.named_steps["model"].estimators_, None, 1), {})
cats = [list(c) for c in oh.categories_]
meta = {"crops_ml": list(crop.classes_), "states": cats[0], "districts": cats[1],
        "ycrops": cats[2], "seasons": cats[3], "rain": None}
csv = "datasets/district_rainfall.csv"
if os.path.exists(csv):
    r = pd.read_csv(csv)
    r.columns = r.columns.str.strip()

    # Support different state-column names
    if "STATE" in r.columns:
        state_col = "STATE"
    elif "STATE/UT" in r.columns:
        state_col = "STATE/UT"
    else:
        raise ValueError("State column not found in district_rainfall.csv")

    r["S"] = r[state_col].astype(str).str.upper().str.strip()
    r["D"] = r["DISTRICT"].astype(str).str.upper().str.strip()

    meta["rain"] = {
        s: {
            d: round(float(v), 1)
            for d, v in zip(g.D, g.ANNUAL)
        }
        for s, g in r.groupby("S")
    }
json.dump(meta, open(f"{OUT}/meta.json", "w"))
print("done", {k: os.path.getsize(f"{OUT}/{k}") for k in os.listdir(OUT)})
