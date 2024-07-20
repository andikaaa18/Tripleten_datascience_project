import datetime
import joblib
import json
import numpy as np
import pandas as pd
import streamlit as st

def input_form():
    # load data
    with open("./assets/categorical_input.json", 'r') as f:
        cat_in = json.load(f)
    with open("./deployment/brand_vehicleType_model.json", 'r') as f:
        basic_spec = {i:j for i,j in json.load(f).items() if i != '//comment'}

    # title of input form
    st.title("Advanced Predictive Modeling and In-Depth Data Analysis for Determining Used Car Market Value")

    # vehicle general information panel
    st.header("General vehicle information", divider='grey')
    row1 = st.columns(2)
    Brand = row1[0].selectbox(label="Brand", options=list(basic_spec.keys()))
    VehicleType = row1[0].selectbox(label="Vehicle Type", 
                                    options= [i for i,j in basic_spec[Brand].items() if len(j)>0],
                                    disabled=False if Brand!=None else True)
    Model = row1[1].selectbox(label="Model", 
                              options=basic_spec[Brand][VehicleType],
                              disabled=False if (Brand!=None)&(VehicleType!=None) else True)

    # engine and transmission specifications panel
    st.header("Engine and transmission specifications", divider='grey')
    Power = st.slider(label="Power (hp)", min_value=100, max_value=2000, value=300, step=1)
    row2 = st.columns(2)
    Gearbox = row2[0].radio(label="Gearbox", options=["manual", "automatic"])
    FuelType = row2[1].selectbox(label="Fuel Type", options=cat_in['FuelType'])

    # vehicle condition and history panel
    st.header("Vehicle condition and history", divider='grey')
    row3 = st.columns(3)
    Mileage = row3[0].number_input(label="Mileage (km)", min_value=0, step=1)
    RegistrationYear = row3[1].number_input(label="Registration Year", min_value=1888, max_value=2030, step=1)
    NotRepaired = row3[2].radio(label="Not Repaired", options=[0, 1], format_func=lambda x: 'No' if x==00 else 'Yes')

    # profile Information panel
    st.header("Profile information", divider='grey')
    row4 = st.columns(2)
    DateCreated = row4[0].date_input(label="Date Created", value=datetime.datetime.now()-datetime.timedelta(1))
    LastSeen = row4[1].date_input(label="Last Seen", value=datetime.datetime.now())

    # Input validation
    pos_car_age = (DateCreated.year - RegistrationYear) >= 0
    pos_post_age = (LastSeen - DateCreated).days >= 0
    is_valid = True if pos_car_age&pos_post_age else False
    execute = st.button("Run the model")
    if  (not is_valid) & execute:
        st.warning("WARNING! Please review/complete your input data", icon='⚠️')

    if  is_valid & execute:
        cols = ['VehicleType', 'Gearbox', 'Power', 'Model', 'Mileage',
                'FuelType', 'Brand', 'NotRepaired', 'car_age', 'post_age']
        
        df = pd.DataFrame(columns=cols, data=[len(cols)*[np.nan]])
        df['VehicleType'] = VehicleType
        df['Gearbox'] = Gearbox
        df['Power'] = Power
        df['Model'] = Model
        df['Mileage'] = Mileage
        df['FuelType'] = FuelType
        df['Brand'] = Brand
        df['NotRepaired'] = NotRepaired
        df['car_age'] = DateCreated.year - RegistrationYear
        df['post_age'] = (LastSeen - DateCreated).days
        
        return df

# make predictions
with st.spinner("In progres..."):
    pipeline = joblib.load('./assets/used_car_price_predictor_pipeline.pkl')

    input_df = input_form()
    if input_df.__class__ == pd.DataFrame:
        st.divider()
        
        st.subheader("Used-Car Price Prediction")
        predict_price = pipeline.predict(input_df)[0]
        st.markdown(f"The market price of the used car is: :green[<b>{predict_price:.2f}</b>] Euro",
                    unsafe_allow_html=True)

        st.divider()


