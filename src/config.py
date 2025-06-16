from pathlib import Path

# Define base directory as the src/ folder
BASE_DIR = Path(__file__).resolve().parent

# Point to model.pkl inside src/
MODEL_PATH = BASE_DIR / 'model.pkl'
