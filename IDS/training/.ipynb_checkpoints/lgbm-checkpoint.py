import pandas as pd
import numpy as np
from common_stage import prepareData
import joblib
# from imblearn.combine import SMOTEENN
from lightgbm import LGBMClassifier


dropped_features = [
    "srv_serror_rate", "serror_rate", "dst_host_srv_serror_rate", "srv_rerror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "dst_host_same_srv_rate",
    "dst_host_serror_rate", "wrong_fragment", "urgent", "diff_srv_rate", "same_srv_rate",
    "srv_diff_host_rate" , "dst_host_srv_diff_host_rate", "rerror_rate"
]

x_train, y_train, x_test, y_test = prepareData(removed_features=dropped_features)

# smote_enn = SMOTEENN(sampling_strategy = "minority",random_state=42)
# X_resampled, y_resampled = smote_enn.fit_resample(x_train, y_train)

lightgbm_model = LGBMClassifier(
    n_estimators=400,  
    max_depth=3, 
    lambda_l2 = 2,
    #class_weight="balanced",  
    random_state=42,
    n_jobs=-1,
    boosting_type="dart",  # Gradient boosting decision trees
    num_leaves=20,  # Default LightGBM value
    learning_rate=0.01,  # Default learning rate
    min_child_samples=5,
    verbose = -1
    #subsample=0.7,
    #colsample_bytree=0.4
)

lightgbm_model.fit(x_train, y_train)
joblib.dump(lightgbm_model, '../models/lgbm.gz')