import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

INPUT_FOLDER = Path(os.getenv("INPUT_FOLDER", "./input"))
OUTPUT_FOLDER = Path(os.getenv("OUTPUT_FOLDER", "./output"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
