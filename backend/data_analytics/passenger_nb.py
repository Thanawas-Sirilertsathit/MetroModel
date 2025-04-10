from data_analytics.passenger_model import PassengerModelBase
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler

class PassengerNaiveBayesModel(PassengerModelBase):
    """Naive Bayes model for passenger related data"""
    def __init__(self):
        """Initialize Naive Bayes"""
        super().__init__()
        self.model = CategoricalNB(alpha=1)
        self.target_encoder = LabelEncoder()
        self.X_test = None
        self.y_test = None

    def train(self, X_train, y_train, X_test, y_test):
        """Train model"""
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test

    def evaluate(self):
        """Evaluate model"""
        y_pred = self.model.predict(self.X_test)
        print(classification_report(self.y_test, y_pred, zero_division=0))

    def predict(self, X_new):
        """Deploy model using it to predict value"""
        for col, le in self.label_encoders.items():
            if col in X_new.columns:
                X_new[col] = le.transform(X_new[col])
        return self.model.predict(X_new)
