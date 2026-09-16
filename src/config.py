# src/config.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA = PROJECT_ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"