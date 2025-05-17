from modules.data_processing import load_data, clean_data
from modules.feature_engineering import encode_features
from modules.model_training import train_model, save_model
from modules.model_evaluation import evaluate_model

DATA_PATH = 'data/telco_churn.csv'
MODEL_PATH = 'model.pkl'

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
