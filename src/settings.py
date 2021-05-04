# %%
from pathlib import Path
import os
import json

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = Path(__file__).resolve().parent

with open(SRC_DIR / 'settings.json') as jsonFile:
    settings = json.load(jsonFile)
