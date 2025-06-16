from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib



def train_model(df):
    x = df.drop('Churn', axis=1)
    y = df['Churn']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

     # Pipeline with scaler + logistic regression
    pipeline = ImbPipeline([
         ('smote', SMOTE(random_state=42)),
         ('scaler', StandardScaler()),
         ('clf', LogisticRegression(random_state=42, C=1, penalty='l2', solver='lbfgs', max_iter=1000))
     ])

    pipeline.fit(x_train, y_train)

     # Save test set for evaluation
    return pipeline, x_test, y_test

def save_model(model, filepath):
    joblib.dump(model, filepath)

def load_model(filepath):
    return joblib.load(filepath)
