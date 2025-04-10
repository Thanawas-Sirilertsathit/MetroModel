import pandas as pd
import numpy as np
from sklearn.utils import resample
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from data_analytics.passenger_nb import PassengerNaiveBayesModel

class RLNaiveBayes(PassengerNaiveBayesModel):
    """Naive Bayes model for Red Line"""
    def __init__(self, quantile_edges=None, labels=None, features=None):
        """Initialize Naive Bayes"""
        super().__init__()
        self.quantile_edges = quantile_edges or [0.0, 0.02, 0.07, 0.5, 0.93, 0.98, 1.0]
        self.labels = labels or ["Very Low", "Low", "Moderate", "Crowded", "Dense", "Very Dense"]
        self.features = features or ["temperature_c", "humidity", "pressure_mb", "Time_Block", "Day_of_Week", "Hour"]

    def preprocess(self, df=pd.read_csv("integrated_weather_and_train.csv"), organization="RL"):
        """Preprocess data for Red Line"""
        df = df[df["Organization"] == organization].copy()
        df = df.dropna(subset=self.features + ["Passenger_Count"])
        quantiles = df["Passenger_Count"].quantile(self.quantile_edges).values
        bins = np.unique(quantiles)
        labels = self.labels[:len(bins) - 1]
        df["Passenger_Rating"] = pd.cut(
            df["Passenger_Count"], bins=bins, labels=labels, include_lowest=True
        )
        for col in ["Time_Block", "Day_of_Week"]:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.label_encoders[col] = le
        return df

    def resample_data(self, df):
        """Oversampling data for each passenger rating"""
        max_count = df["Passenger_Rating"].value_counts().max()
        resampled_df = pd.DataFrame()

        for label in df["Passenger_Rating"].unique():
            group = df[df["Passenger_Rating"] == label]
            resampled = resample(group, replace=True, n_samples=max_count, random_state=42)
            resampled_df = pd.concat([resampled_df, resampled])
        return resampled_df

    def train(self, df):
        """Train Naive Bayes model"""
        df = self.resample_data(df)
        X = df[self.features]
        y = df["Passenger_Rating"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, stratify=y, test_size=0.1, random_state=42
        )
        for col in X_train.columns:
            X_test[col] = X_test[col].clip(upper=X_train[col].max())
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test

    def predict(self, X_new: pd.DataFrame):
        """Predict the value using itself"""
        for col in ["Time_Block", "Day_of_Week"]:
            if col in X_new.columns and col in self.label_encoders:
                X_new[col] = self.label_encoders[col].transform(X_new[col])
        for col in X_new.columns:
            if col in self.X_test.columns:
                X_new[col] = X_new[col].clip(upper=self.X_test[col].max())

        X_new = X_new[self.X_test.columns]
        preds = self.model.predict(X_new)
        return preds
