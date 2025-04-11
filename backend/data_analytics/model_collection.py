from data_analytics.pk_naive import PKNaiveBayes
from data_analytics.pk_quantile import PKQuantileRegressor
from data_analytics.yl_naive import YLNaiveBayes
from data_analytics.yl_quantile import YLQuantileRegressor
from data_analytics.srt_naive import SRTNaiveBayes
from data_analytics.srt_quantile import SRTQuantileRegressor
from data_analytics.rl_naive import RLNaiveBayes
from data_analytics.rl_quantile import RLQuantileRegressor
from data_analytics.arl_naive import ARLNaiveBayes
from data_analytics.arl_quantile import ARLQuantileRegressor
from data_analytics.mrt_naive import MRTNaiveBayes
from data_analytics.mrt_quantile import MRTQuantileRegressor
from data_analytics.bts_naive import BTSNaiveBayes
from data_analytics.bts_quantile import BTSQuantileRegressor
from data_analytics.constant import RATING_MAP

class ModelCollections:
    """Collection of all models"""
    RATING_MAP = RATING_MAP
    def __init__(self):
        """Create models objects as attributes and put in the list."""
        self.pk_nb = PKNaiveBayes()
        self.pk_qr = PKQuantileRegressor()
        self.yl_nb = YLNaiveBayes()
        self.yl_qr = YLQuantileRegressor()
        self.srt_nb = SRTNaiveBayes()
        self.srt_qr = SRTQuantileRegressor()
        self.rl_nb = RLNaiveBayes()
        self.rl_qr = RLQuantileRegressor()
        self.arl_nb = ARLNaiveBayes()
        self.arl_qr = ARLQuantileRegressor()
        self.mrt_nb = MRTNaiveBayes()
        self.mrt_qr = MRTQuantileRegressor()
        self.bts_nb = BTSNaiveBayes()
        self.bts_qr = BTSQuantileRegressor()
        self.model_list = []
        self.initialize_list()
    
    def initialize_list(self):
        """Put models into the list as dictionary."""
        self.model_list.clear()
        self.model_list.append({"id":1, "org": "SRT","nb": self.srt_nb, "qr": self.srt_qr})
        self.model_list.append({"id":2, "org": "RL","nb": self.rl_nb, "qr": self.rl_qr})
        self.model_list.append({"id":3, "org": "ARL","nb": self.arl_nb, "qr": self.arl_qr})
        self.model_list.append({"id":4, "org": "MRT","nb": self.mrt_nb, "qr": self.mrt_qr})
        self.model_list.append({"id":5, "org": "BTS","nb": self.bts_nb, "qr": self.bts_qr})
        self.model_list.append({"id":6, "org": "YL","nb": self.yl_nb, "qr": self.yl_qr})
        self.model_list.append({"id":7, "org": "PK","nb": self.pk_nb, "qr": self.pk_qr})

    def train_all(self):
        """Train models for all."""
        for model_dict in self.model_list:
            print(f"Now training model for {model_dict['org']} train line.")
            print("____________________________________________________________")
            nb = model_dict["nb"]
            df = nb.preprocess()
            nb.train(df)
            nb.evaluate()
            qr = model_dict["qr"]
            X_train, X_test, y_train, y_test = qr.preprocess(df, self.RATING_MAP)
            qr.train(X_train, y_train, X_test, y_test)
            qr.evaluate()

    def get_model_dict(self, key):
        """Return model dictionary for further usage."""
        for model_dict in self.model_list:
            if key == model_dict["id"]:
                return model_dict
    
    def predict(self, key ,df):
        """Predict the passenger count and return the value out."""
        model_dict = self.get_model_dict(key)
        if not model_dict:
            raise ValueError("Incorrect key for organization.")
        nb = model_dict["nb"]
        qr = model_dict["qr"]
        predicted_rating = nb.predict(df)
        df = qr.rating_map(df, predicted_rating, self.RATING_MAP)
        predicted_count = qr.predict(df)
        predicted_count = [int(round(x)) for x in predicted_count]
        return predicted_rating, predicted_count

# const blocks = [
#   { title: "State railway of Thailand (Normal train)", description: "Service time: 5:30 - 0:00", key: 1 },
#   { title: "Red line", description: "Service time: 5:30 - 0:00", key: 2 },
#   { title: "Airport rail link", description: "Service time: 5:30 - 0:00", key: 3 },
#   { title: "MRT (Blue line)", description: "Service time: 5:30 - 0:00", key: 4 },
#   { title: "BTS (Green line)", description: "Service time: 6:00 - 0:00", key: 5 },
#   { title: "Yellow line", description: "Service time: 6:00 - 0:00", key: 6 },
#   { title: "Pink line", description: "Service time: 6:00 - 0:00", key: 7 },
#   { title: "Overall", description: "Service time: 5:30 - 0:00", key: 8 },
# ];
