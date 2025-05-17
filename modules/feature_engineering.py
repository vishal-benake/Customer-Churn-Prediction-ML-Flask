import pandas as pd
from sklearn.preprocessing import LabelEncoder

def encode_features(df):
    df = df.copy()
    # Binary columns encoding Yes/No to 1/0
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
    for col in binary_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0})

    # Multiple categorical features with more than two categories, use pd.get_dummies
    multi_cat_cols = ['gender', 'InternetService', 'Contract', 'PaymentMethod',
                      'MultipleLines', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                      'TechSupport', 'StreamingTV', 'StreamingMovies']

    df = pd.get_dummies(df, columns=multi_cat_cols, drop_first=True)

    return df