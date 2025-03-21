import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import joblib


def prepareData(scaling=False, removed_features=[]):

    # Load data into a DataFrame
    train_df = pd.read_csv("Dataset/kddcup.data_10_percent.gz", compression='gzip', header=None)
    test_df = pd.read_csv("Dataset/corrected.gz", compression='gzip', header=None)
    
    # Take 10% subset of test set
    # test_df = test_df.sample(frac=0.1, replace=False, axis=0, ignore_index=True)
    
    # Assign column names
    all_columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land',
        'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
        'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
        'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
        'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
        'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
        'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
        'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate',
        'label'
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
    
    # Remove test examples with attack types not included in training set
    test_df = test_df[test_df['label'].isin(train_df['label'].unique())]
    
    # Replace specific attack labels with more general attack categories
    attack_categories = {
        'normal.' : 'Normal',
        
        'back.' : 'DoS', 'land.' : 'DoS', 'neptune.' : 'DoS', 'pod.' : 'DoS', 'smurf.' : 'DoS','teardrop.' : 'DoS',
        
        'buffer_overflow.':'U2R', 'loadmodule.':'U2R', 'perl.':'U2R', 'rootkit.': 'U2R',
        
        'ftp_write.' : 'R2L' , 'guess_passwd.':'R2L', 'imap.':'R2L', 'multihop.':'R2L', 'phf.':'R2L', 'spy.':'R2L',
        'warezclient.':'R2L', 'warezmaster.':'R2L',
        
        'ipsweep.':'Probing', 'nmap.':'Probing', 'portsweep.':'Probing', 'satan.': 'Probing'
    }
    train_df['label'] = train_df['label'].map(attack_categories)
    test_df['label'] = test_df['label'].map(attack_categories)
    
    # Remove instances of U2R attack type
    train_df = train_df[train_df['label'] != 'U2R']
    test_df = test_df[test_df['label'] != 'U2R']
    
    # Reset dataframe index
    train_df.reset_index(drop=True, inplace=True)
    test_df.reset_index(drop=True, inplace=True)
    
    # Split datasets into continuous features, categorical features, and labels
    categorical_cols = ['protocol_type', 'service', 'flag', 'land']
    train_con = train_df.drop(columns=categorical_cols+['label'], errors='ignore')
    test_con = test_df.drop(columns=categorical_cols+['label'], errors='ignore')
    train_cat = train_df.filter(categorical_cols)
    test_cat = test_df.filter(categorical_cols)
    train_labels = train_df.filter(['label'])
    test_labels = test_df.filter(['label'])
    
    # Scale continuous features
    if scaling == True:
        scaler = StandardScaler().set_output(transform='pandas')
        train_con = scaler.fit_transform(train_con)
        test_con = scaler.transform(test_con)
    
    # Encode categorical features
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore').set_output(transform='pandas')
    train_cat = ohe.fit_transform(train_cat)
    test_cat = ohe.transform(test_cat)
    
    # Encode labels
    le = LabelEncoder()
    train_labels = train_labels.apply(le.fit_transform)
    test_labels = test_labels.apply(le.transform)
    
    # Rejoin features and labels into single dataframe
    train_df = train_con.join([train_cat, train_labels])
    test_df = test_con.join([test_cat, test_labels])
    
    # Export scaler and encoder and return transformed datasets
    joblib.dump(ohe, 'IDS/preprocessing/onehotencoder.gz')
    joblib.dump(le, 'IDS/preprocessing/labelencoder.gz')
    if scaling == True:
        joblib.dump(scaler, 'IDS/preprocessing/scaler.gz')

    x_train = train_df.drop(columns=['label'])
    y_train = train_df['label']
    x_test = test_df.drop(columns=['label'])
    y_test = test_df['label']
    return x_train, y_train, x_test, y_test
