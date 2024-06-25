# import library
from deployment.fast_api.data_schema import user_data
from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd

# Creating RESTful API with FAST API
app = FastAPI()

@app.get("/api")
def read():
    return {"Welcome": "Welcome to our API!"}

@app.post("/api/churn_prediction")
def predict(data:user_data): 
    def data_preparation(data:user_data):
        # create blueprint of input data
        input_df = pd.DataFrame(data=[len(cluster_pipeline.feature_names_in_)*[np.nan]],
                                    columns=cluster_pipeline.feature_names_in_)
        
        # adjust the values for each feature
        input_df['gender'] = data.gender
        input_df['SeniorCitizen'] = data.SeniorCitizen
        input_df['Partner'] = data.Partner
        input_df['Dependents'] = data.Dependents
        input_df['Type'] = data.Type
        input_df['PaperlessBilling'] = data.PaperlessBilling
        input_df['PaymentMethod'] = data.PaymentMethod
        input_df['MonthlyCharges'] = data.MonthlyCharges
        input_df['Duration'] = (data.EndDate - data.BeginDate).days
        input_df['InternetService'] = data.InternetService
        input_df['PhoneService'] = data.PhoneService
        input_df['Net_Addons_Num'] = len(data.NetAddon) if data.NetAddon != None else 0

        list_addons = list(user_data.__annotations__['NetAddon'].__args__[0].__args__[0].__args__)
        if data.NetAddon != None:
            input_df[list_addons] = [list(map(lambda x:1 if x in data.NetAddon else 0, list_addons))]
        else:
            input_df[list_addons] = [len(list_addons)*[0]]

        return input_df

    def cluster_info(cluster):
        if cluster == 0:
            return ["Premium category customers. They typically spend around USD 94.75 per month on the services they use.",
                    "Loyal customers. Their retention rate ranges from 2.5 to 3 years."
                    "Generally users of fiber optic internet with an additional 2 to 6 additional services."
                    "The additional services they prefer are TV and movie streaming."
                    "Typically, clients in this group are individuals without dependents."]
        elif cluster == 1:
            return ["Basic category customers. They typically spend around USD 20.25 per month on the services they use.",
                    "Loyal customers. Their retention rate is around 3 years.",
                    "Generally, they do not use the internet, so their average monthly bill is not very large.",
                    "Typically, clients in this group are individuals with dependents."]
        elif cluster == 2:
            return ["Regular category customers. They typically spend around USD 79.28 per month on the services they use.",
                    "They are loyal customers. Their retention rate is around 4.5 years.",
                    "Generally users of DSL internet with an additional 2 to 6 additional services.",
                    "Some clients in this group enjoy TV and movie streaming services.",
                    "Typically, clients in this group are individuals with dependents."]
        elif cluster == 3:
            return ["Basic category customers. They typically spend around USD 20.25 per month on the services they use.",
                    "They have low retention. Their retention rate is around 3 months.",
                    "Generally, they do not use the internet, so their average monthly bill is not very large.",
                    "Typically, clients in this group are individuals without dependents."]
        elif cluster == 4:
            return ["Regular category customers. They typically spend around USD 69.65 per month on the services they use.",
                    "They have low retention. Their retention rate is around 10 months.",
                    "Generally, they use the internet, with some using DSL and others using fiber optic in a relatively balanced proportion.",
                    "They use fewer than 3 add-ons. TV or movie streaming services are not favored by this group.",
                    "Typically, clients in this group are individuals without dependents."]

    # load the model
    cluster_pipeline = joblib.load('./assets/cluster_pipeline.pkl')
    churn_predictor_pipeline = joblib.load('./assets/churn_predictor_pipeline.pkl')
    
    # data preparation
    data_prep = data_preparation(data)

    # predict churn
    churn_prob = churn_predictor_pipeline.predict_proba(data_prep)[:,1][0]
    threshold = 0.40 # based on findings at EDA process
    churn = 1 if churn_prob >= threshold else 0

    # cluster analysis
    cluster = cluster_pipeline.predict(data_prep)[0]
    cluster_info = cluster_info(cluster)

    return {'message':"API for churn prediction",
            'churn_prob': float(churn_prob),
            'threshold': float(threshold),
            'churn': churn,
            'cluster': int(cluster),
            'cluster_info': cluster_info
            }