# library for data processing
import pandas as pd
import numpy as np
from sklearn.compose import make_column_transformer
from sklearn.compose import make_column_selector
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# library for building models
import optuna
from sklearn.linear_model import LinearRegression

# library model evaluation
from sklearn.metrics import mean_absolute_error

# other
import warnings
warnings.filterwarnings('ignore')

def data_split(df):
    # memisahkan data khusus untuk training set
    less5_Model = df['Model'].value_counts()[lambda x:x<5].index.values
    less5_Brand = df['Brand'].value_counts()[lambda x:x<5].index.values

    train_add = df[df['Model'].isin(less5_Model) | df['Brand'].isin(less5_Brand)]
    remaining_df = df[~df['Model'].isin(less5_Model) & ~df['Brand'].isin(less5_Brand)]

    # membagi dataset
    train, val = train_test_split(remaining_df, test_size=0.4, random_state=101010, stratify=remaining_df[['Model']])
    val, test = train_test_split(val, test_size=0.5, random_state=101010, stratify=val[['Model']])

    # menggabungkan data training additional
    train = pd.concat([train, train_add])

    # memisahkan fitur dan target
    train_x, train_y = train.drop(columns=['Price']), train['Price']
    val_x, val_y = val.drop(columns=['Price']), val['Price']
    test_x, test_y = test.drop(columns=['Price']), test['Price']

    return train_x, train_y, val_x, val_y, test_x, test_y

def features_transformer(train_x, val_x, test_x, min_freq):
    # membuat transformer
    features_transformer = make_column_transformer(
        (StandardScaler(), make_column_selector(dtype_include=np.number)),
        (OneHotEncoder(drop='first', sparse_output=False, min_frequency=min_freq), make_column_selector(dtype_include=object)),
        n_jobs=-1)

    # transformasi data
    features_train = features_transformer.fit_transform(train_x)
    features_val = features_transformer.transform(val_x)
    features_test = features_transformer.transform(test_x)

    return features_train, features_val, features_test

def logging_callback(study, frozen_trial):
    previous_best_value = study.user_attrs.get('previous_best_value', None)
    if previous_best_value != study.best_value:
        previous_best_value = study.set_user_attr('previous_best_value', study.best_value)
        print("Trial {} finished with best value: {} and parameters: {}. ".format(
            frozen_trial.number,
            frozen_trial.value,
            frozen_trial.params,
            )
        )

def hyperparameter_tuning(n_trials=10):
    def objective(trial):
        # hyperparameter
        min_freq = trial.suggest_float('min_freq', 0, 1)

        # feature engineering
        df = pd.read_csv("./datasets/cleaned_car_data.csv")
        train_x, train_y, val_x, val_y, test_x, test_y = data_split(df)
        train_x, val_x, test_x = features_transformer(train_x, val_x, test_x, min_freq=min_freq)

        # training
        lr = LinearRegression()
        
        lr.fit(train_x, train_y)
        val_pred = lr.predict(val_x)

        return mean_absolute_error(val_y, val_pred)

    # atur logger agar tidak menampilkan log DEBUG dan INFO, tetapi hanya menampilkan log WARNING, ERROR dan CRITICAL
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    study = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=101010))
    study.optimize(objective, n_trials=n_trials, callbacks=[logging_callback])

if __name__ == '__main__':
    hyperparameter_tuning(n_trials=500)
