import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import joblib
import io
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from xgb import XGBoost
from randomforest import RandomForest
from lgbm import LightGBM

normal = open('logs/normal.txt', 'a')
attacks = open('logs/attacks.txt', 'a')
model_name = sys.argv[1]
record = sys.argv[2]

match model_name:
    case 'xgboost':
        model = XGBoost()
    case 'randomforest':
        model = RandomForest()
    case 'lightgbm':
        model = LightGBM()
    case _:
        print('Invalid model selected.')

# Create dataframe from captured connection record
datapoint = pd.read_csv(io.StringIO(record), header=None)

# Assign column names
all_columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land',
    'wrong_fragment', 'urgent', 'count', 'srv_count', 'serror_rate',
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]

datapoint.columns = all_columns

# Model-specific preprocessing
datapoint = model.preprocess(datapoint)

# Split datapoint into continuous and categorical features
categorical_cols = ['protocol_type', 'service', 'flag', 'land']
continuous = datapoint.drop(columns=categorical_cols, errors='ignore')
categorical = datapoint.filter(categorical_cols)

# Encode categorical features
ohe = joblib.load('preprocessing/onehotencoder.gz')
categorical = ohe.transform(categorical)

# Rejoin features into single dataframe
datapoint = continuous.join(categorical)

# Classify datapoint
prediction = model.predict(datapoint)
print(prediction)

# Decode prediction
le = joblib.load('preprocessing/labelencoder.gz')
prediction = le.inverse_transform(prediction)
print(prediction)

# attack = prediction == 1

# # Write record to log
# record = record + "\n"
# if (attack):
#     attacks.write(record)
#     print("Attack detected!")
# else:
#     normal.write(record)