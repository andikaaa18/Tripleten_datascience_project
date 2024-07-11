# <img src="./assets/oil-rig.png" height="160px" align="left" style="background-color:white;"> **Identifying the Best Oil Well Exploration Locations for a Mining Company:** Integrating predictive models of oil reserve volumes, business calculations, and statistics to calculate potential profit and risk.

***

# **About the Project**
## Background and Objectives
<div style="text-align:center"><img src="./assets/oil-rig2.png" height="200px"></div><br>

**OilyGiant** is a company operating in the oil and gas mining industry. The company plans to construct 200 new oil wells in one of its mining areas. The company has budgeted 100 million USD for this construction, and the produced oil will be sold at 4.5 USD per barrel. To identify the best 200 locations, 500 data samples will be taken from each area, and the 200 wells with the highest reserve volumes will be used as references to determine if an area is profitable from a business perspective. Therefore, this project aims to build a predictive model that can forecast oil reserve volumes using collected data.

The project involves several processes:
* Conducting exploratory data analysis (EDA).
* Building a machine learning model.
* Performing a business valuation to identify areas with a risk level below 2.5%.

## Scope Limitations
There are several problem limitations in this project, both related to the machine learning modeling process and the business process, including:

* **Only linear regression is suitable for model training** (others are inadequate for prediction).
* During the exploration phase, **500 data samples will be taken from an area**. Using the predictive model, **the best 200 locations will be selected for oil wells**.
* The budget for developing 200 oil wells is **100 million USD**.
* One barrel of raw material generates 4.5 USD in revenue. **Revenue from one unit of product is 4,500 USD** (1 unit of product = 1,000 barrels).
* After evaluating risk, retain only areas with a loss risk **below 2.5%**. From the list of areas that meet this criterion, select the area with the highest average profit.

# **Project Outcome**
## Exploratory Data Analysis (EDA)
* The average oil reserve volume of all wells in the three regions indicates values less than the minimum average volume required to avoid losses for **OilyGiant**, which is 111.1 thousand barrels.
* Region 2 has the highest average oil reserve volume compared to the other two regions. Region 1, on the other hand, has the smallest average oil reserve volume.
* Here are the average and standard deviation values of oil reserve volumes in the three regions:
    * **Region 0:** $\mu$ = 92.5 thousand barrels ; $\sigma$ = 44.3 thousand barrels.
    * **Region 1:** $\mu$ = 68.8 thousand barrels ; $\sigma$ = 45.9 thousand barrels.
    * **Region 2:** $\mu$ = 95.0 thousand barrels ; $\sigma$ = 44.7 thousand barrels.
* Across all regions, the oil reserve volume at a well site tends to be determined by the `f2` feature as it exhibits stronger correlation compared to other features.

## Model Development
* Based on the model evaluation results, Area-1 exhibits the highest predictive capability, whereas Area-2 is the most challenging region to predict according to the model.
* Below are the RMSE (Root Mean Square Error) values for model evaluation in each region:
    * Area-0: 37.72 thousand barrels per well
    * Area-1: 0.89 thousand barrels per well
    * Area-2: 39.98 thousand barrels per well

## Business Valuation
* If sampling is conducted for 500 well points followed by selecting the top 200 points according to the model's predictions, Region 1 will yield the lowest loss risk and the highest average profit compared to the other regions. Below are the average profits and loss probabilities for each area:
    * Area-0: $4,252,654.13 USD (4.40%)
    * Area-1: $4,677,351.29 USD (0.60%)
    * Area-2: $3,377,842.86 USD (9.00%)
    <br><br><div style="text-align:center"><img src="./assets/Risk Level of Loss for the Construction of 200 Oil Wells in Each Area.png" width="100%"></div><br>
* The model accuracy and the number of sample acquisitions will greatly influence the profit evaluation in each region. **High accuracy and more sample acquisitions will lead to average profits closer to the best scenario**.
* **Among the three regions, only Region 1 is suitable for further development**, as it has a loss risk of less than 2.5% and the highest profit.
