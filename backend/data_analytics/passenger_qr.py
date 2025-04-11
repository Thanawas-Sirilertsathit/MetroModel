from data_analytics.passenger_model import PassengerModelBase
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.regression.quantile_regression import QuantReg
import statsmodels.api as sm
import numpy as np
import pandas as pd

class PassengerQuantileRegressor(PassengerModelBase):
    """Quantile Regression for passenger related data"""
    def __init__(self, quantile=0.5):
        super().__init__()
        self.quantile = quantile
        self.model = None
        self.result = None
        self.X_test_scaled = None
        self.y_test = None

    def train(self, X_train, y_train, X_test, y_test):
        """Train model"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        X_train_scaled = sm.add_constant(X_train_scaled)
        X_test_scaled = sm.add_constant(X_test_scaled)
        self.model = QuantReg(y_train, X_train_scaled)
        self.result = self.model.fit(q=self.quantile)
        self.X_test_scaled = X_test_scaled
        self.y_test = y_test

    def evaluate(self):
        """Evaluate model"""
        y_pred = self.result.predict(self.X_test_scaled)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)
        print(self.result.summary())
        print(f"\nMSE: {mse:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")

    def predict(self, X_new):
        """Deploy model using it to predict value"""
        for col, le in self.label_encoders.items():
            if col in X_new.columns:
                X_new[col] = le.transform(X_new[col])

        X_new = X_new.apply(pd.to_numeric, errors="coerce")
        X_new_scaled = self.scaler.transform(X_new)
        X_new_scaled = sm.add_constant(X_new_scaled, has_constant="add")
        pred = self.result.predict(X_new_scaled)
        return np.clip(pred, 100, None)
