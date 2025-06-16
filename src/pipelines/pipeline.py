from components.data_processing import load_data, clean_data
from components.feature_engineering import encode_features
from pipelines.model_training import train_model, save_model
from pipelines.model_evaluation import evaluate_model
from config import MODEL_PATH
from logger import setup_logging

DATA_PATH = 'data/telco_churn.csv'
# MODEL_PATH = 'model.pkl'


def run_pipeline():
    print("Loading data...")
    df = load_data(DATA_PATH)

    print("Cleaning data...")
    df = clean_data(df)

    print("Encoding features...")
    df = encode_features(df)

    print("Training model...")
    model, X_test, y_test = train_model(df)

    print("Evaluating model...")
    evaluate_model(model, X_test, y_test)

    print(f"Saving model to {MODEL_PATH} ...")
    save_model(model, MODEL_PATH)

    print("Pipeline finished successfully.")

if __name__ == "__main__":
    run_pipeline()
    setup_logging(prefix="pipeline")
