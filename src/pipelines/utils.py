import pandas as pd

def preprocess_input(input_data, df_columns):
    """
    Preprocess a single input record to align with model input features.
    
    Parameters:
        input_data (dict): User input dictionary.
        df_columns (list): Model training DataFrame column names (after encoding).
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame with columns aligned to training data.
    """
    input_df = pd.DataFrame([input_data])

    # Safely map binary Yes/No to 1/0
    binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
    for col in binary_cols:
        if col in input_df.columns:
            input_df[col] = input_df[col].map({'Yes': 1, 'No': 0})

    # Numeric conversions with error handling
    input_df['SeniorCitizen'] = int(input_df.get('SeniorCitizen', 0))
    input_df['tenure'] = int(input_df.get('tenure', 0))
    input_df['MonthlyCharges'] = float(input_df.get('MonthlyCharges', 0))
    input_df['TotalCharges'] = pd.to_numeric(input_df.get('TotalCharges', 0), errors='coerce').fillna(0)

    # One-hot encode multi-category fields
    multi_cat_cols = ['gender', 'InternetService', 'Contract', 'PaymentMethod',
                      'MultipleLines', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                      'TechSupport', 'StreamingTV', 'StreamingMovies']

    for col in multi_cat_cols:
        categories = [c for c in df_columns if c.startswith(col + '_')]
        for cat_col in categories:
            category = cat_col[len(col)+1:]
            input_df[cat_col] = 1 if input_df.get(col, [''])[0] == category else 0
        input_df.drop(col, axis=1, inplace=True, errors='ignore')

    # Align with training columns
    input_df = input_df.reindex(columns=df_columns, fill_value=0)

    return input_df