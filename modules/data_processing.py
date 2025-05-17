import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    # Drop customerID (not useful for prediction)
    df = df.drop('customerID', axis=1)

    # Convert TotalCharges to numeric, coerce errors to NaN
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Fill missing TotalCharges with median
    df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

    # Replace 'No internet service' and 'No phone service' with 'No' in categorical cols
    replace_cols = ['MultipleLines', 'OnlineSecurity', 'OnlineBackup',
                    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    for col in replace_cols:
        df[col] = df[col].replace({'No internet service': 'No', 'No phone service': 'No'})

    return df