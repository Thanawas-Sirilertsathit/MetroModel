import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg
from passenger_qr import PassengerQuantileRegressor
from srt_naive import SRTNaiveBayes
from rating_map import RATING_MAP

class SRTQuantileRegressor(PassengerQuantileRegressor):
    """Quantile Regression model for SRT train line"""
    def __init__(self, quantile=0.48):
        """Initialize Quantile Regressor."""
        super().__init__(quantile=quantile)

    def preprocess(self, df, rating_map=None):
        """Preprocess data for SRT"""
        df = df[df["Organization"] == "SRT"].copy()
        df = df.drop(columns=["Organization", "Datetime","Rating_Label"], errors="ignore")
        if rating_map:
            df["Passenger_Rating"] = df["Passenger_Rating"].map(rating_map)
        for col in ["Time_Block", "Day_of_Week"]:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.label_encoders[col] = le
        df = df.dropna(subset=["Passenger_Count"])
        X = df.drop(columns=["Passenger_Count", "Date"], errors='ignore')
        y = df["Passenger_Count"]
        X = X.apply(pd.to_numeric, errors="coerce")
        X = X.apply(lambda col: col.astype(int) if col.dtype == "bool" else col)
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self, X_train, y_train, X_test, y_test):
        """Train quantile regression model"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        X_train_scaled = sm.add_constant(X_train_scaled)
        X_test_scaled = sm.add_constant(X_test_scaled)
        self.model = QuantReg(y_train, X_train_scaled)
        self.result = self.model.fit(q=self.quantile)
        self.X_test_scaled = X_test_scaled
        self.y_test = y_test
    
    def rating_map(self, df, nb_result, rating_map):
        """Prepare the data from Naive Bayes to prediction"""
        df["Passenger_Rating"] = pd.Series(nb_result).map(rating_map)
        return df


if __name__ == '__main__':
    nb = SRTNaiveBayes()
    df = nb.preprocess()
    nb.train(df)
    nb.evaluate()
    qr = SRTQuantileRegressor(quantile=0.48)
    X_train, X_test, y_train, y_test = qr.preprocess(df, RATING_MAP)
    qr.train(X_train, y_train, X_test, y_test)
    qr.evaluate()
    example_data = pd.DataFrame({
    "Hour": [9, 13, 17],    
    "Time_Block": ["Morning", "Afternoon", "Evening"],
    "Day_of_Week": ["Saturday", "Friday", "Sunday"],
    "temperature_c": [30.2, 36.5, 37.5],
    "humidity": [70, 82, 50],
    "pressure_mb": [1005.1, 1003.7, 1100.2],
    })
    predicted_ratings = nb.predict(example_data)
    print("Naive Bayes Predicted Ratings:", predicted_ratings.tolist())
    example_data = qr.rating_map(example_data, predicted_ratings, RATING_MAP)
    print(example_data)
    predicted_counts = qr.predict(example_data)
    predicted_counts = [int(round(x)) for x in predicted_counts]
    print("Quantile Regression Predicted Passenger Count:", predicted_counts)
