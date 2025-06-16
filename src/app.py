from flask import Flask, render_template, request
import joblib
from pipeline.utils import preprocess_input  # your utility to preprocess single input
from logger import setup_logging
from config import MODEL_PATH
from pathlib import Path


app = Flask(__name__)
model = joblib.load(MODEL_PATH)  # your trained pipeline model
df_columns = model.named_steps['scaler'].feature_names_in_ if hasattr(model.named_steps['scaler'], 'feature_names_in_') else None
# Or save your df_columns at model training time and load here for input alignment


# Set the correct templates folder path (relative to this file)
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        user_input = {
            'gender': request.form['gender'],
            'SeniorCitizen': request.form['SeniorCitizen'],
            'Partner': request.form['Partner'],
            'Dependents': request.form['Dependents'],
            'PhoneService': request.form['PhoneService'],
            'MultipleLines': request.form['MultipleLines'],
            'InternetService': request.form['InternetService'],
            'OnlineSecurity': request.form['OnlineSecurity'],
            'OnlineBackup': request.form['OnlineBackup'],
            'DeviceProtection': request.form['DeviceProtection'],
            'TechSupport': request.form['TechSupport'],
            'StreamingTV': request.form['StreamingTV'],
            'StreamingMovies': request.form['StreamingMovies'],
            'Contract': request.form['Contract'],
            'PaperlessBilling': request.form['PaperlessBilling'],
            'PaymentMethod': request.form['PaymentMethod'],
            'tenure': float(request.form['tenure']),
            'MonthlyCharges': float(request.form['MonthlyCharges']),
            'TotalCharges': float(request.form['TotalCharges'])
        }

        # Preprocess user input to match model input format
        input_df = preprocess_input(user_input, df_columns)

       # Predict churn class
        pred = model.predict(input_df)[0]
        prediction_text = "Customer will churn" if pred == 1 else "Customer will not churn"

        # Get churn probability (confidence score for class = 1)
        prob = model.predict_proba(input_df)[0][1]
        user_input['confidence'] = f"{prob:.2%}"

        # Render result on index.html
        return render_template('index.html', prediction_text=prediction_text, user_input=user_input)

@app.route('/report', methods=['POST'])
def report():
    user_input = request.form.to_dict()
    prediction_text = user_input.pop('prediction', 'No prediction')

    return render_template('report.html', prediction_text=prediction_text, user_input=user_input)


if __name__ == '__main__':
    app.run(debug=True)
    setup_logging(prefix="app")
