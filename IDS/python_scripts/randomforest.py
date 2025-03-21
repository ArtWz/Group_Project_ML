import joblib

class RandomForest:

    def preprocess(self, datapoint):

        print('Model: Random Forest')

        dropped_features = [
            "srv_serror_rate", "serror_rate", "dst_host_srv_serror_rate", "srv_rerror_rate",
            "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "dst_host_same_srv_rate",
            "dst_host_serror_rate", "wrong_fragment", "urgent", "diff_srv_rate", "same_srv_rate",
            "srv_diff_host_rate" , "dst_host_srv_diff_host_rate", "rerror_rate"
        ]

        datapoint = datapoint.drop(columns=dropped_features)
        return datapoint

    def predict(self, datapoint):

        # Load trained model
        model = joblib.load('models/randomforest.gz')

        # Classify datapoint
        prediction = model.predict(datapoint)
        return prediction