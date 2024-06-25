# library for data processing
import pandas as pd
import numpy as np
from sklearn.compose import make_column_transformer
from sklearn.compose import make_column_selector
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler

# library for building models
import optuna
from sklearn.linear_model import LogisticRegression

# library model evaluation
from sklearn.metrics import roc_auc_score

# other
import warnings
warnings.filterwarnings('ignore')

def data_preparation():
    def remove_data(customer_ids, *df):
        df_list = []
        for data in df:
            data = data.query("~customerID.isin(@customer_ids)")
            data = data.reset_index(drop=True)
            df_list.append(data)

        return df_list

    contract = pd.read_csv("./datasets/final_provider/contract.csv")
    internet = pd.read_csv("./datasets/final_provider/internet.csv")
    personal = pd.read_csv("./datasets/final_provider/personal.csv")
    phone = pd.read_csv("./datasets/final_provider/phone.csv")

    # membuang data client dengan nilai empty string pada data contract di kolom 'TotalCharges' 
    remove_ids = contract[contract['TotalCharges'] == ' ']['customerID'].values
    contract, internet, personal, phone = remove_data(remove_ids, contract, internet, personal, phone)
    
    # replace nilai 'No' di kolom 'EndDate' menjadi np.nan
    contract = contract.replace({'EndDate':'No'}, np.nan)

    # transformasi nilai 'No' menjadi 0 dan 'Yes' menjadi 1
    contract = contract.replace(['No', 'Yes'], [0, 1])
    internet = internet.replace(['No', 'Yes'], [0, 1])
    personal = personal.replace(['No', 'Yes'], [0, 1])
    phone = phone.replace(['No', 'Yes'], [0, 1])

    # memperbaiki tipe data
    contract['BeginDate'] = pd.to_datetime(contract['BeginDate'], format="%Y-%m-%d")
    contract['EndDate'] = pd.to_datetime(contract['EndDate'], format="%Y-%m-%d %H:%M:%S")
    contract['TotalCharges'] = contract['TotalCharges'].astype(float)

    # menambahkan kolom 'Churn' pada data contract
    contract['Churn'] = (~contract['EndDate'].isna()).apply(lambda x: 1 if x==True else 0)

    # menambahkan kolom 'Duration' pada data contract
    contract['Duration'] = (contract['EndDate'].fillna('2020/02/01') - contract['BeginDate']).dt.days

    # menambahkan kolom 'Net_Addons_Num' pada data internet
    net_add_ons = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    internet['Net_Addons_Num'] = internet[net_add_ons].sum(axis=1)

    # mengatur nilai untuk klien yang tidak berlangganan layanan internet
    internet = contract[['customerID']].merge(internet, on='customerID', how='left')
    internet['InternetService'] = internet['InternetService'].fillna('No internet')
    internet = internet.fillna(0)

    # mengatur nilai untuk klien yang tidak berlangganan layanan telepon
    phone = contract[['customerID']].merge(phone, on='customerID', how='left')
    phone['MultipleLines'] = phone['MultipleLines'].fillna('No line')
    phone['MultipleLines'] = phone['MultipleLines'].replace({0: 'Single line', 1: 'Multi line'})
    phone = phone.rename(columns={'MultipleLines': 'PhoneService'})

    # data merging
    df = personal.merge(contract, how='left', on='customerID')
    df = df.merge(internet, how='left', on='customerID')
    df = df.merge(phone, how='left', on='customerID')

    # melakukan reduksi data
    df = df.drop(columns=['BeginDate', 'EndDate'])

    return df

def feature_engineering(df):
    feature = df.drop(columns=['customerID', 'TotalCharges', 'gender', 'Churn']) 
    target = df['Churn']
    feature_train, feature_val, target_train, target_val = train_test_split(feature, target, test_size=0.4, stratify=target,
                                                                            random_state=101010)
    feature_val, feature_test, target_val, target_test = train_test_split(feature_val, target_val, test_size=0.5, stratify=target_val,
                                                                          random_state=101010)
    
    # membuat pipeline feature engineering
    feat_eng_pipe = make_column_transformer(
        (OneHotEncoder(drop='first', sparse_output=False), make_column_selector(dtype_include=object)),
        (StandardScaler(), ['MonthlyCharges', 'Duration', 'Net_Addons_Num']),
        remainder='passthrough', n_jobs=-1
    )

    # transformasi data
    feature_train = feat_eng_pipe.fit_transform(feature_train)
    feature_val = feat_eng_pipe.transform(feature_val)
    feature_test = feat_eng_pipe.transform(feature_test)

    return feature_train, target_train, feature_val, target_val, feature_test, target_test

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
        prop_minority = trial.suggest_categorical('prop_minority', [None, 0.3, 0.35, 0.4, 0.45, 0.5])
        shrinkage = trial.suggest_float('shrinkage', 0, 3)
        C = trial.suggest_float('C', 1e-4, 1)
        l1_ratio = trial.suggest_float('l1_ratio', 0, 1)

        # oversampling
        if prop_minority:
            oversampler = RandomOverSampler(sampling_strategy=prop_minority/(1-prop_minority), random_state=101010, shrinkage=shrinkage)
            train_data = oversampler.fit_resample(feature_train, target_train)
        else:
            train_data = (feature_train, target_train)

        # training
        lr = LogisticRegression(penalty='elasticnet', solver='saga', C=C, l1_ratio=l1_ratio, 
                                class_weight='balanced', random_state=101010, n_jobs=-1)
        
        lr.fit(*train_data)
        val_pred_proba = lr.predict_proba(feature_val)

        return roc_auc_score(target_val, val_pred_proba[:, 1])

    # atur logger agar tidak menampilkan log DEBUG dan INFO, tetapi hanya menampilkan log WARNING, ERROR dan CRITICAL
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    df = data_preparation()
    feature_train, target_train, feature_val, target_val, feature_test, target_test = feature_engineering(df)

    study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler(seed=101010))
    study.optimize(objective, n_trials=n_trials, callbacks=[logging_callback])

if __name__ == '__main__':
    hyperparameter_tuning(n_trials=100)