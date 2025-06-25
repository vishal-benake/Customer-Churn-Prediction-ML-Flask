from flask import Flask, request, render_template, session
from src.pipelines.predict_pipeline import CustomData, PredictPipeline
import secrets

application = Flask(__name__)
app = application

# Required for session data to persist
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                gender=request.form.get('gender'),
                SeniorCitizen=int(request.form.get('SeniorCitizen')),
                Partner=request.form.get('Partner'),
                Dependents=request.form.get('Dependents'),
                tenure=float(request.form.get('tenure')),
                PhoneService=request.form.get('PhoneService'),
                MultipleLines=request.form.get('MultipleLines'),
                InternetService=request.form.get('InternetService'),
                OnlineSecurity=request.form.get('OnlineSecurity'),
                OnlineBackup=request.form.get('OnlineBackup'),
                DeviceProtection=request.form.get('DeviceProtection'),
                TechSupport=request.form.get('TechSupport'),
                StreamingTV=request.form.get('StreamingTV'),
                StreamingMovies=request.form.get('StreamingMovies'),
                Contract=request.form.get('Contract'),
                PaperlessBilling=request.form.get('PaperlessBilling'),
                PaymentMethod=request.form.get('PaymentMethod'),
                MonthlyCharges=float(request.form.get('MonthlyCharges')),
                TotalCharges=float(request.form.get('TotalCharges'))
            )

            pred_df = data.get_data_as_data_frame()

            predict_pipeline = PredictPipeline()
            pred, proba = predict_pipeline.predict(pred_df)

            prediction_text = "Customer will churn" if pred[0] == 1 else "Customer will not churn"

            session['user_input'] = pred_df.to_dict(orient='records')[0]
            session['prediction_text'] = prediction_text
            session['churn_prob'] = float(proba[0][1])
            session['not_churn_prob'] = float(proba[0][0])

            return render_template('home.html', prediction_text=prediction_text)

        except Exception as e:
            print("Prediction Error:", e)
            return f"Internal Server Error: {str(e)}", 500

@app.route('/report')
def report():
    user_input = session.get('user_input')
    prediction_text = session.get('prediction_text')
    churn_prob = session.get('churn_prob')
    not_churn_prob = session.get('not_churn_prob')

    if not user_input or not prediction_text:
        return "Missing session data. Please go back and submit the form again.", 400

    return render_template(
        'report.html',
        prediction_text=prediction_text,
        user_input=user_input,
        churn_prob=churn_prob,
        not_churn_prob=not_churn_prob
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0")
