from pk_naive import PKNaiveBayes
from pk_quantile import PKQuantileRegressor
from constant import RATING_MAP, EXAMPLE_DATA


nb = PKNaiveBayes()
df = nb.preprocess()
nb.train(df)
nb.evaluate()


qr = PKQuantileRegressor(quantile=0.45)
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
