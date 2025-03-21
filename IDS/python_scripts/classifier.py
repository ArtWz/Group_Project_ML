import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import joblib
import io
from xgboost import XGBClassifier

normal = open('logs/normal.txt', 'a')
attacks = open('logs/attacks.txt', 'a')
record = sys.argv[1]

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

# Import encoders and scaler
ohe = joblib.load('preprocessing/onehotencoder.gz')
le = joblib.load('preprocessing/labelencoder.gz')
### Need to add scaler

# Need to generalise this
dropped_features = [
    "srv_serror_rate", "serror_rate", "dst_host_srv_serror_rate", "srv_rerror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "dst_host_same_srv_rate",
    "dst_host_serror_rate", "wrong_fragment", "urgent", "diff_srv_rate", "same_srv_rate",
    "srv_diff_host_rate" , "dst_host_srv_diff_host_rate", "rerror_rate"
]

datapoint = datapoint.drop(columns=dropped_features)

# Split datapoint into continuous and categorical features
categorical_cols = ['protocol_type', 'service', 'flag', 'land']
continuous = datapoint.drop(columns=categorical_cols, errors='ignore')
categorical = datapoint.filter(categorical_cols)

# Encode categorical features
categorical = ohe.transform(categorical)

# Rejoin features into single dataframe
datapoint = continuous.join(categorical)

# Load trained model
model = joblib.load('models/xgb.gz')

# Classify datapoint
prediction = model.predict(datapoint)
print(prediction)

# Decode prediction
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