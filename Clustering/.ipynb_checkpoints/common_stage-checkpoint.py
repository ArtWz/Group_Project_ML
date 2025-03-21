import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib


def prepareData(scaling=False, removed_features=[]):
    # Load data into a DataFrame
    train_df = pd.read_csv("kddcup.data_10_percent.gz", compression='gzip', header=None)
    test_df = pd.read_csv("corrected.gz", compression='gzip', header=None)
    
    # Take 10% subset of test set
    test_df = test_df.sample(frac=0.1, replace=False, axis=0, ignore_index=True)
    
    all_columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land',
        'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
        'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
        'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
        'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
        'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_count',
        'dst_host_diff_srv_count', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
        'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'target'
    ]
    
    train_df.columns = all_columns
    test_df.columns = all_columns
    
    # Remove "content" features
    content_cols = ['hot', 'num_failed_logins', 'logged_in', 'num_compromised',
        'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
        'num_outbound_cmds', 'is_host_login', 'is_guest_login']
    
    train_df = train_df.drop(columns=content_cols)
    test_df = test_df.drop(columns=content_cols)

    # Remove any other specified features
    train_df = train_df.drop(columns=removed_features)
    test_df = test_df.drop(columns=removed_features)

    # Split datasets into continuous features, categorical features, and labels
    categorical_cols = ['protocol_type', 'service', 'flag', 'land']
    train_con = train_df.drop(columns=categorical_cols+['target'], errors='ignore')
    test_con = test_df.drop(columns=categorical_cols+['target'], errors='ignore')
    train_cat = train_df.filter(categorical_cols)
    test_cat = test_df.filter(categorical_cols)
    train_labels = train_df.filter(['target'])
    test_labels = test_df.filter(['target'])

    # Scale continuous features
    if scaling == True:
        scaler = StandardScaler()
        train_con = scaler.fit_transform(train_con)
        test_con = scaler.transform(test_con)

    # Encode categorical features
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='infrequent_if_exist')
    train_cat = encoder.fit_transform(train_cat)
    test_cat = encoder.transform(test_cat)

    # Rejoin features and labels into single dataframe
    train_df = pd.DataFrame(np.concatenate((train_con, train_cat, train_labels), axis=1))
    test_df = pd.DataFrame(np.concatenate((test_con, test_cat, test_labels), axis=1))

    # Export scaler and encoder and return transformed datasets
    joblib.dump(encoder, 'encoder.gz')
    if scaling == True:
        joblib.dump(scaler, 'scaler.gz')

    return train_df, test_df
