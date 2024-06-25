import datetime
import joblib
import json
import numpy as np
import pandas as pd
import streamlit as st

def input_form(): 
    with open("./deployment/streamlit_app/config.json", 'r') as file:
        config = json.load(file)
        in2out = config['in2out']

    # title input form
    st.title("Churn Analysis and Prediction for Telecommunication Services")

    # personal information form
    st.header("Personal Information", divider='grey')
    row1 = st.columns(4)
    Gender = row1[0].radio("Gender", list(in2out['gender'].values()), 
                        format_func=lambda value: list(filter(lambda key:in2out['gender'][key]==value, 
                                                                in2out['gender']))[0])
    SeniorCitizen = row1[1].radio("Senior Citizen", list(in2out['yes/no'].values()), 
                                format_func=lambda value: list(filter(lambda key:in2out['yes/no'][key]==value, 
                                                                        in2out['yes/no']))[0])
    Partner = row1[2].radio("Partner", list(in2out['yes/no'].values()), 
                            format_func=lambda value: list(filter(lambda key:in2out['yes/no'][key]==value, 
                                                                in2out['yes/no']))[0])
    Dependents = row1[3].radio("Dependents", list(in2out['yes/no'].values()),
                            format_func=lambda value: list(filter(lambda key:in2out['yes/no'][key]==value, 
                                                                    in2out['yes/no']))[0])

    # contract information form
    st.header("Contract Information", divider='grey')
    row2 = st.columns(2)
    BeginDate = row2[0].date_input("Begin Date", value=datetime.datetime.today() - datetime.timedelta(weeks=52))
    EndDate = row2[1].date_input("End Date")

    row3 = st.columns([0.70, 0.30], gap='large')
    Type = row3[0].radio("Contract Type", list(in2out['contract_type'].values()), 
                        format_func=lambda value: list(filter(lambda key:in2out['contract_type'][key]==value, 
                                                            in2out['contract_type']))[0], 
                        horizontal=True)
    PaperlessBilling = row3[1].radio("Paperless Billing", list(in2out['yes/no'].values()),
                                    format_func=lambda value: list(filter(lambda key:in2out['yes/no'][key]==value, 
                                                                        in2out['yes/no']))[0],
                                    horizontal=True)

    row4 = st.columns([0.70, 0.30], gap='large')
    PaymentMethod = row4[0].radio("Payment Method", list(in2out['payment_method'].values()), 
                                format_func=lambda value: list(filter(lambda key:in2out['payment_method'][key]==value, 
                                                                        in2out['payment_method']))[0],
                                horizontal=True)
    MonthlyCharges = row4[1].number_input('Avg. Monthly Charges', value=None, placeholder="eg: USD 300")

    st.markdown("Primary service used")
    row5 = st.columns(2)
    MainService_phone = row5[0].checkbox('Phone Service', value=False)
    MainService_net = row5[1].checkbox('Internet Service', value=False)

    # Phone service information form
    st.header("Phone Service", divider='grey')
    ChannelType = st.radio('Channel Type', list(in2out['channel_type'].values()),
                        format_func=lambda value: list(filter(lambda key:in2out['channel_type'][key]==value, 
                                                                in2out['channel_type']))[0], 
                        index=0 if MainService_phone else None,
                        disabled= not MainService_phone)

    # Internet service information form
    st.header("Internet Service", divider='grey')
    row6 = st.columns([0.25, 0.75])
    CableType = row6[0].radio('Cable Type', list(in2out['cable_type'].values()),
                            format_func=lambda value: list(filter(lambda key:in2out['cable_type'][key]==value,
                                                                        in2out['cable_type']))[0],
                            index=0 if MainService_net else None,
                            disabled= not MainService_net)

    NetAddon = row6[1].multiselect("Internet Add-ons", list(in2out['net_addon'].values()), 
                                   default=list(in2out['net_addon'].values()) if MainService_net else [],
                                   format_func=lambda value: list(filter(lambda key:in2out['net_addon'][key]==value,
                                                                         in2out['net_addon']))[0],
                                   disabled= not MainService_net)

    # Check the completeness of data input
    is_complete = (MainService_net or MainService_phone) & (MonthlyCharges!=None)
    execute = st.button("Run the model")
    if  (not is_complete) & execute:
        st.warning("WARNING! Please review/complete your input data", icon='⚠️')

    if  is_complete & execute:
        input_df = pd.DataFrame(data=[len(cluster_pipeline.feature_names_in_)*[np.nan]],
                                columns=cluster_pipeline.feature_names_in_)
        input_df['gender'] = Gender
        input_df['SeniorCitizen'] = SeniorCitizen
        input_df['Partner'] = Partner
        input_df['Dependents'] = Dependents
        input_df['Type'] = Type
        input_df['PaperlessBilling'] = PaperlessBilling
        input_df['PaymentMethod'] = PaymentMethod
        input_df['MonthlyCharges'] = MonthlyCharges
        input_df['Duration'] = (EndDate-BeginDate).days
        input_df['InternetService'] = CableType if MainService_net else "No internet"
        input_df['PhoneService'] = ChannelType if MainService_phone else "No line"
        input_df['Net_Addons_Num'] = len(NetAddon)
        input_df[list(in2out['net_addon'].values())] = [list(map(lambda x:1 if x in NetAddon else 0, list(in2out['net_addon'].values())))]

        return input_df

def cluster_info(df):
    cluster = cluster_pipeline.predict(df)[0]
    st.markdown(f"This client has a close similarity to clients from :blue[<b>CLUSTER-{cluster}</b>]. "
                f"Clients in this cluster have common characteristics, including:", 
                unsafe_allow_html=True)

    if cluster == 0:
        st.markdown("<li> Premium category customers. They typically spend around USD 94.75 per month on the services they use."
                    "<li> Loyal customers. Their retention rate ranges from 2.5 to 3 years."
                    "<li> Generally users of fiber optic internet with an additional 2 to 6 additional services."
                    "<li> The additional services they prefer are TV and movie streaming."
                    "<li> Typically, clients in this group are individuals without dependents.",
                    unsafe_allow_html=True)
    elif cluster == 1:
        st.markdown("<li> Basic category customers. They typically spend around USD 20.25 per month on the services they use."
                    "<li> Loyal customers. Their retention rate is around 3 years."
                    "<li> Generally, they do not use the internet, so their average monthly bill is not very large."
                    "<li> Typically, clients in this group are individuals with dependents.",
                    unsafe_allow_html=True)
    elif cluster == 2:
        st.markdown("<li> Regular category customers. They typically spend around USD 79.28 per month on the services they use."
                    "<li> They are loyal customers. Their retention rate is around 4.5 years."
                    "<li> Generally users of DSL internet with an additional 2 to 6 additional services."
                    "<li> Some clients in this group enjoy TV and movie streaming services."
                    "<li> Typically, clients in this group are individuals with dependents.",
                    unsafe_allow_html=True)
    elif cluster == 3:
        st.markdown("<li> Basic category customers. They typically spend around USD 20.25 per month on the services they use."
                    "<li> They have low retention. Their retention rate is around 3 months."
                    "<li> Generally, they do not use the internet, so their average monthly bill is not very large."
                    "<li> Typically, clients in this group are individuals without dependents.",
                    unsafe_allow_html=True)
    elif cluster == 4:
        st.markdown("<li> Regular category customers. They typically spend around USD 69.65 per month on the services they use."
                    "<li> They have low retention. Their retention rate is around 10 months."
                    "<li> Generally, they use the internet, with some using DSL and others using fiber optic in a relatively balanced proportion."
                    "<li> They use fewer than 3 add-ons. TV or movie streaming services are not favored by this group."
                    "<li> Typically, clients in this group are individuals without dependents.",
                    unsafe_allow_html=True)

# make predictions
with st.spinner("In progres..."):
    cluster_pipeline = joblib.load('./assets/cluster_pipeline.pkl')
    churn_predictor_pipeline = joblib.load('./assets/churn_predictor_pipeline.pkl')

    input_df = input_form()
    if input_df.__class__ == pd.DataFrame:
        st.divider()
        
        churn_prob = churn_predictor_pipeline.predict_proba(input_df)[:,1][0]
        threshold = 0.40

        if churn_prob>=threshold:
            st.markdown(f"Client is predicted :red[<b>TO UNSUBSCRIBE</b>] 😥.<br>"
                        f"The probability of the client discontinuing their subscription is :red[<b>{churn_prob:.2%}</b>].",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"Client is predicted :green[<b>TO CONTINUE SUBSCRIBING</b>] 🥳.<br>"
                        f"The probability of the client discontinuing their subscription is :green[<b>{churn_prob:.2%}</b>].",
                        unsafe_allow_html=True)

        cluster_info(input_df)

        st.divider()




        




