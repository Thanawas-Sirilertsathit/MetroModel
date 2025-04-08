from abc import ABC, abstractmethod
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


class PassengerModelBase(ABC):
    """Abstract class for any models to predict passenger related data"""
    def __init__(self, features=None):
        """Initialize class"""
        self.features = features or ["temperature_c", "humidity", "pressure_mb", "Time_Block", "Day_of_Week"]
        self.label_encoders = {}
        self.scaler = StandardScaler()

    def encode_features(self, df):
        """Encode features using label encoding"""
        for col in ["Time_Block", "Day_of_Week"]:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.label_encoders[col] = le
        return df

    def preprocess(self, df, target_column, drop_columns=None, organization=None):
        """Preprocess dataframe before going to further steps"""
        df = df[df["Organization"] == organization].copy()
        df = df.dropna(subset=self.features + [target_column])
        if drop_columns:
            df = df.drop(columns=drop_columns, errors="ignore")
        df = self.encode_features(df)
        X = df[self.features]
        y = df[target_column]
        X = X.apply(pd.to_numeric, errors="coerce")
        X = X.apply(lambda col: col.astype(int) if col.dtype == "bool" else col)
        return train_test_split(X, y, test_size=0.2, random_state=42)

    @abstractmethod
    def train(self, X_train, y_train, X_test, y_test):
        """Train the model"""
        pass

    @abstractmethod
    def evaluate(self):
        """Evaluate the model"""
        pass

    @abstractmethod
    def predict(self, X_new):
        """Deploy the model by using it to predict value"""
        pass
