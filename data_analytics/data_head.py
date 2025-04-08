import sys
import os
import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm
from statsmodels.regression.quantile_regression import QuantReg
from sklearn.naive_bayes import CategoricalNB
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from matplotlib import pyplot as plt

integrated_df = pd.read_csv("integrated_weather_and_train.csv")
print(integrated_df.head())
