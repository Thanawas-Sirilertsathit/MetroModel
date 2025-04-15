import unittest
from data_analytics.pk_naive import PKNaiveBayes
from data_analytics.pk_quantile import PKQuantileRegressor
from data_analytics.constant import RATING_MAP, EXAMPLE_DATA

class TestARLPrediction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nb_model = PKNaiveBayes()
        cls.df = cls.nb_model.preprocess()
        cls.nb_model.train(cls.df)

        cls.qr_model = PKQuantileRegressor(quantile=0.45)
        X_train, X_test, y_train, y_test = cls.qr_model.preprocess(cls.df, RATING_MAP)
        cls.qr_model.train(X_train, y_train, X_test, y_test)

    def test_naive_bayes_prediction(self):
        predicted_ratings = self.nb_model.predict(EXAMPLE_DATA.copy())
        self.assertEqual(len(predicted_ratings), len(EXAMPLE_DATA))

    def test_rating_mapping(self):
        predicted_ratings = self.nb_model.predict(EXAMPLE_DATA.copy())
        mapped_df = self.qr_model.rating_map(EXAMPLE_DATA.copy(), predicted_ratings, RATING_MAP)
        self.assertIn("Passenger_Rating", mapped_df.columns)

    def test_quantile_regression_prediction(self):
        predicted_ratings = self.nb_model.predict(EXAMPLE_DATA.copy())
        mapped_df = self.qr_model.rating_map(EXAMPLE_DATA.copy(), predicted_ratings, RATING_MAP)


        for col, le in self.qr_model.label_encoders.items():
            if col in mapped_df.columns:
                mapped_df[col] = le.transform([
                    x if x in le.classes_ else le.classes_[0] for x in mapped_df[col]
                ])

        predicted_counts = self.qr_model.predict(mapped_df)
        self.assertEqual(len(predicted_counts), len(EXAMPLE_DATA))