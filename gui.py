import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from src.recommendation import Recommendation
from src.config import RAIN_FILE
# =====================================================
# Backend
# =====================================================

system = Recommendation()

# =====================================================
# Rainfall Dataset
# =====================================================

rainfall_df = pd.read_csv(RAIN_FILE)

rainfall_df.columns = rainfall_df.columns.str.strip()

rainfall_df["STATE/UT"] = (
    rainfall_df["STATE/UT"]
    .astype(str)
    .str.upper()
    .str.strip()
)

rainfall_df["DISTRICT"] = (
    rainfall_df["DISTRICT"]
    .astype(str)
    .str.upper()
    .str.strip()
)

state_list = sorted(
    rainfall_df["STATE/UT"]
    .dropna()
    .unique()
    .tolist()
)

# =====================================================
# Soil Types
# =====================================================

soil_types = [

    "ALLUVIAL",

    "BLACK",

    "RED",

    "LATERITE",

    "DESERT",

    "MOUNTAIN"

]

# =====================================================
# Window
# =====================================================

root = tk.Tk()

root.title("Agricultural Decision Support System")

root.state("zoomed")

root.configure(bg="#eef4f7")

# =====================================================
# Title
# =====================================================

title = tk.Label(

    root,

    text="Agricultural Decision Support System",

    font=("Arial",26,"bold"),

    bg="#1f7a4d",

    fg="white",

    pady=15

)

title.pack(fill="x")

# =====================================================
# Main Container
# =====================================================

main = tk.Frame(

    root,

    bg="#eef4f7"

)

main.pack(

    fill="both",

    expand=True,

    padx=20,

    pady=20

)

main.grid_columnconfigure(0,weight=1)

main.grid_columnconfigure(1,weight=1)

main.grid_rowconfigure(0,weight=1)

# =====================================================
# LEFT PANEL
# =====================================================

crop_frame = tk.LabelFrame(

    main,

    text="Crop Recommendation",

    font=("Arial",14,"bold"),

    bg="white",

    padx=20,

    pady=20

)

crop_frame.grid(

    row=0,

    column=0,

    sticky="nsew",

    padx=(0,10)

)

crop_frame.grid_columnconfigure(1,weight=1)

# =====================================================
# Crop Labels
# =====================================================

crop_labels=[

    "State",

    "District",

    "Soil Type",

    "Temperature (°C)",

    "Humidity (%)"

]

crop_entries={}

# =====================================================
# Update District Dropdown
# =====================================================

def update_crop_districts(event=None):

    state = crop_entries["State"].get().strip().upper()

    districts = sorted(

        rainfall_df[
            rainfall_df["STATE/UT"] == state
        ]["DISTRICT"]

        .dropna()
        .unique()
        .tolist()

    )

    crop_entries["District"]["values"] = districts
    crop_entries["District"].set("")


# =====================================================
# Create Input Fields
# =====================================================

for i, label in enumerate(crop_labels):

    tk.Label(

        crop_frame,

        text=label,

        font=("Arial",11),

        bg="white"

    ).grid(

        row=i,

        column=0,

        sticky="w",

        padx=10,

        pady=12

    )

    # -------------------------
    # State Dropdown
    # -------------------------

    if label == "State":

        widget = ttk.Combobox(

            crop_frame,

            values=state_list,

            state="readonly",

            width=32

        )

        widget.bind(

            "<<ComboboxSelected>>",

            update_crop_districts

        )

    # -------------------------
    # District Dropdown
    # -------------------------

    elif label == "District":

        widget = ttk.Combobox(

            crop_frame,

            state="readonly",

            width=32

        )

    # -------------------------
    # Soil Dropdown
    # -------------------------

    elif label == "Soil Type":

        widget = ttk.Combobox(

            crop_frame,

            values=soil_types,

            state="readonly",

            width=32

        )

    # -------------------------
    # Normal Entry
    # -------------------------

    else:

        widget = tk.Entry(

            crop_frame,

            width=35,

            relief="solid",

            bd=1,

            font=("Arial",11)

        )

    widget.grid(

        row=i,

        column=1,

        sticky="ew",

        padx=10,

        pady=12,

        ipady=4

    )

    crop_entries[label] = widget


# =====================================================
# Result Label
# =====================================================

crop_result = tk.Label(

    crop_frame,

    text="",

    bg="white",

    fg="blue",

    justify="left",

    anchor="w",

    font=("Arial",12,"bold")

)

crop_result.grid(

    row=6,

    column=0,

    columnspan=2,

    sticky="ew",

    padx=10,

    pady=20

)

# =====================================================
# Crop Recommendation Function
# =====================================================

def recommend_crop():

    try:

        state = crop_entries["State"].get().strip().upper()
        district = crop_entries["District"].get().strip().upper()
        soil = crop_entries["Soil Type"].get().strip().upper()

        temperature = float(
            crop_entries["Temperature (°C)"].get()
        )

        humidity = float(
            crop_entries["Humidity (%)"].get()
        )

        if not state:
            raise ValueError("Please select State.")

        if not district:
            raise ValueError("Please select District.")

        if not soil:
            raise ValueError("Please select Soil Type.")

        # ----------------------------------------
        # Soil Database (Default Values)
        # ----------------------------------------

        soil_data = {

            "ALLUVIAL": (90,42,43,6.5),

            "BLACK": (70,38,45,7.3),

            "RED": (55,28,32,5.8),

            "LATERITE": (40,22,28,5.2),

            "DESERT": (25,15,18,8.1),

            "MOUNTAIN": (65,35,38,6.2)

        }

        N,P,K,PH = soil_data[soil]

        crop,rainfall = system.recommend_crop(

            N,
            P,
            K,
            temperature,
            humidity,
            PH,
            state,
            district

        )

        crop_result.config(

            text=

            f"Annual Rainfall : {rainfall:.1f} mm\n\n"

            f"Recommended Crop : {crop}"

        )

    except Exception as e:

        messagebox.showerror(

            "Error",

            str(e)

        )


# =====================================================
# Recommend Button
# =====================================================

recommend_btn = tk.Button(

    crop_frame,

    text="Recommend Crop",

    command=recommend_crop,

    bg="#198754",

    fg="white",

    font=("Arial",11,"bold"),

    width=22,

    pady=6

)

recommend_btn.grid(

    row=5,

    column=0,

    columnspan=2,

    pady=15

)

# =====================================================
# RIGHT PANEL
# =====================================================

yield_frame = tk.LabelFrame(
    main,
    text="Yield Prediction",
    font=("Arial",14,"bold"),
    bg="white",
    padx=20,
    pady=20
)

yield_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(10,0)
)

yield_frame.grid_columnconfigure(1,weight=1)

yield_labels=[
    "State",
    "District",
    "Crop",
    "Season",
    "Area (ha)"
]

yield_entries={}

crop_options=[
    "Rice",
    "Wheat",
    "Maize",
    "Sugarcane",
    "Cotton",
    "Barley",
    "Gram",
    "Groundnut",
    "Jowar",
    "Bajra"
]

season_options=[
    "Kharif",
    "Rabi",
    "Zaid"
]

# =====================================================
# Update District Dropdown
# =====================================================

def update_yield_districts(event=None):

    state=yield_entries["State"].get().strip().upper()

    districts=sorted(

        rainfall_df[
            rainfall_df["STATE/UT"]==state
        ]["DISTRICT"]

        .dropna()
        .unique()
        .tolist()

    )

    yield_entries["District"]["values"]=districts
    yield_entries["District"].set("")

# =====================================================
# Create Fields
# =====================================================

for i,label in enumerate(yield_labels):

    tk.Label(

        yield_frame,

        text=label,

        font=("Arial",11),

        bg="white"

    ).grid(

        row=i,

        column=0,

        sticky="w",

        padx=10,

        pady=12

    )

    if label=="State":

        widget=ttk.Combobox(

            yield_frame,

            values=state_list,

            width=32,

            state="readonly"

        )

        widget.bind(
            "<<ComboboxSelected>>",
            update_yield_districts
        )

    elif label=="District":

        widget=ttk.Combobox(

            yield_frame,

            width=32,

            state="readonly"

        )

    elif label=="Crop":

        widget=ttk.Combobox(

            yield_frame,

            values=crop_options,

            width=32,

            state="readonly"

        )

    elif label=="Season":

        widget=ttk.Combobox(

            yield_frame,

            values=season_options,

            width=32,

            state="readonly"

        )

    else:

        widget=tk.Entry(

            yield_frame,

            width=35,

            relief="solid",

            bd=1,

            font=("Arial",11)

        )

    widget.grid(

        row=i,

        column=1,

        padx=10,

        pady=12,

        sticky="ew",

        ipady=4

    )

    yield_entries[label]=widget

# =====================================================
# Result Label
# =====================================================

yield_result=tk.Label(

    yield_frame,

    text="",

    bg="white",

    fg="blue",

    justify="left",

    anchor="w",

    font=("Arial",12,"bold")

)

yield_result.grid(

    row=7,

    column=0,

    columnspan=2,

    sticky="ew",

    padx=10,

    pady=20

)

# =====================================================
# Predict Yield
# =====================================================

def predict_yield():

    try:

        state=yield_entries["State"].get().strip().upper()
        district=yield_entries["District"].get().strip().upper()
        crop=yield_entries["Crop"].get().strip()
        season=yield_entries["Season"].get().strip()
        area=float(yield_entries["Area (ha)"].get())

        prediction,rainfall=system.predict_yield(

            state,
            district,
            crop,
            season,
            area

        )

        yield_result.config(

            text=

            f"Annual Rainfall : {rainfall if rainfall is None else round(rainfall,1)} mm\n\n"

            f"Predicted Yield : {prediction:.2f} tons/hectare"

        )

    except Exception as e:

        messagebox.showerror(

            "Error",

            str(e)

        )

# =====================================================
# Button
# =====================================================

predict_btn=tk.Button(

    yield_frame,

    text="Predict Yield",

    command=predict_yield,

    bg="#0d6efd",

    fg="white",

    font=("Arial",11,"bold"),

    width=22,

    pady=6

)

predict_btn.grid(

    row=6,

    column=0,

    columnspan=2,

    pady=15

)

# =====================================================
# Run
# =====================================================

root.mainloop()