from arl_naive import ARLNaiveBayes
from arl_quantile import ARLQuantileRegressor
from constant import RATING_MAP, EXAMPLE_DATA


nb = ARLNaiveBayes()
df = nb.preprocess()
nb.train(df)
nb.evaluate()


qr = ARLQuantileRegressor(quantile=0.51)
X_train, X_test, y_train, y_test = qr.preprocess(df, RATING_MAP)
qr.train(X_train, y_train, X_test, y_test)
qr.evaluate()


example_data = EXAMPLE_DATA
predicted_ratings = nb.predict(example_data)
print("Naive Bayes Predicted Ratings:", predicted_ratings.tolist())


example_data = qr.rating_map(example_data, predicted_ratings, RATING_MAP)
print(example_data)


predicted_counts = qr.predict(example_data)
predicted_counts = [int(round(x)) for x in predicted_counts]
print("Quantile Regression Predicted Passenger Count:", predicted_counts)
