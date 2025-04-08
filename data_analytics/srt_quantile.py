import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg
from passenger_qr import PassengerQuantileRegressor
from srt_naive import SRTNaiveBayes
from constant import RATING_MAP

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
