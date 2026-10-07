import os

def create_directories():

    folders = [

        "cleaned_data",

        "models"

    ]

    for folder in folders:

        if not os.path.exists(folder):

            os.makedirs(folder)

    print("Folders Ready.")