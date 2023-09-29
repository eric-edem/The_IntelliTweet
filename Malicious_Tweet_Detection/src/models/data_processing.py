# data_preprocessing.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold
from sklearn.preprocessing import StandardScaler, Normalizer

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def preprocessing():

    scale = StandardScaler()

    X_train_original = X_train0.drop(columns=['Full_Text'])
    # X_train_original = X_train0
    Baseline_y_train_original = Baseline_y_train0

    for k in range(25):
        globals()[f"X_train_original{k}"] = globals()[f"X_train{k}"]
        globals()[f"Baseline_y_train_original{k}"] = globals()[f"Baseline_y_train{k}"]
        globals()[f"scaledX{k}"]  = scale.fit_transform(globals()[f"X_train{k}"].drop(columns=['Full_Text']))
        globals()[f"X_test{k}s"] = scale.fit_transform(globals()[f"X_test{k}"].drop(columns=['Full_Text']))

        from imblearn.over_sampling import SMOTE
        oversample = SMOTE()
        globals()[f"X_train{k}sa"], globals()[f"Baseline_y_train{k}sa"] = oversample.fit_resample(globals()[f"scaledX{k}"], globals()[f"Baseline_y_train{k}"])
        globals()[f"X_train{k}sa"] = pd.DataFrame(globals()[f"X_train{k}sa"], columns=X_train_original.columns)


        globals()[f"X_train{k}s"], globals()[f"Baseline_y_train{k}s"] =  globals()[f"scaledX{k}"], globals()[f"Baseline_y_train_original{k}"]
        globals()[f"X_train{k}s"] = pd.DataFrame(globals()[f"X_train{k}s"], columns=X_train_original.columns)
        globals()[f"X_test{k}s"] = pd.DataFrame(globals()[f"X_test{k}s"], columns=X_train_original.columns)

        globals()[f"X_train{k}o"], globals()[f"Baseline_y_train{k}o"] =  globals()[f"X_train_original{k}"].drop(columns=['Full_Text']), globals()[f"Baseline_y_train_original{k}"]


def Augment_data(data):
    dff = data[data["Tweet_Label"] != 0]
    d1 = data[data["Tweet_Label"] != 0]
    d2 = data[data["Tweet_Label"] == 0]

    cols_to_adjust = ['account_age', 'Follower Count', 'Following Count',
                      'User Favourite Count', 'no_lists', 'noTweet']

    dff = dff[['account_age', 'Follower Count', 'Following Count',
               'User Favourite Count', 'no_lists', 'noTweet']]
    np.random.seed(42)

    for j, i in enumerate(dff.columns):
        if dff[i].dtype.kind == 'i':
            count = 0
            for row in dff[i].values:
                x = np.random.randint(-5, 5)
                val = row + x

                if val < 0:
                    x = np.random.randint(0, 3)
                    val = row + x
                dff.iloc[count, j] = val
                count = count + 1

    d1[cols_to_adjust] = dff[cols_to_adjust].values
    data = d2.append(d1)
    return data

def select_samples_randomized(df, label_column, labels_to_select, num_samples_per_label=2000):
    selected_samples = pd.DataFrame()

    for label in labels_to_select:
        label_samples = df[df[label_column] == label]
        if len(label_samples) <= num_samples_per_label:
            selected_samples = pd.concat([selected_samples, label_samples])
        else:
            selected_samples = pd.concat([selected_samples, label_samples.sample(n=num_samples_per_label, random_state=42)])

    return selected_samples

def split_data(data, test_size=0.2, random_state=None):
    x_feat = data[['Full_Text', 'account_age', 'Follower Count', 'Following Count',
                   'User Favourite Count', 'no_lists', 'noTweet', 'Retweet Count',
                   'no_hashtag', 'no_mentions', 'no_urls', 'no_char', 'no_digit',
                   'URL_Length', 'Shortining_Service', 'Domain_registeration_length',
                   'Request_URL', 'URL_of_Anchor', 'Abnormal_URL', 'Redirect', 'Iframe',
                   'age_of_domain', 'web_traffic', 'Links_pointing_to_page', 'sub', 'pol']]
    #    'Subjectivity','Polarity']]

    y_feat = data[["Tweet_Label"]]
    # y_feat = y_feat.replace([0, 1, 2],[0, 1, 0])

    x_featt = x_feat.to_numpy()
    y_featt = y_feat.to_numpy()
    return x_featt, y_featt, x_feat, y_feat

def SKF_CV(data):
    rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)

    count = 0
    x_featt, y_featt, x_feat, y_feat = split_data(data)
    for train_index, test_index in rskf.split(x_featt, y_featt):
        print("TRAIN:", train_index, "TEST:", test_index)
        globals()[f"X_train{count}"], globals()[f"X_test{count}"] = x_featt[train_index], x_featt[test_index]
        globals()[f"train_{count}_Indexes"], globals()[f"test_{count}_Indexes"] = [train_index], [test_index]
        globals()[f"X_train{count}"], globals()[f"X_test{count}"] = pd.DataFrame(globals()[f"X_train{count}"],
                                                                                 columns=x_feat.columns), pd.DataFrame(
            globals()[f"X_test{count}"], columns=x_feat.columns)
        globals()[f"y_train{count}"], globals()[f"y_test{count}"] = y_featt[train_index], y_featt[test_index]
        globals()[f"y_train{count}"], globals()[f"y_test{count}"] = pd.DataFrame(globals()[f"y_train{count}"],
                                                                                 columns=y_feat.columns), pd.DataFrame(
            globals()[f"y_test{count}"], columns=y_feat.columns)
        count = count + 1
