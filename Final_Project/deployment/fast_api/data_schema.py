from datetime import date
from pydantic import BaseModel, model_validator, ValidationError
from typing import Literal, Optional, Tuple, Union
from typing_extensions import Self

class user_data(BaseModel):
    # personal information
    gender: Literal['Male', 'Female']
    SeniorCitizen: Literal[0, 1]
    Partner: Literal[0, 1]
    Dependents: Literal[0, 1]

    # contract information
    BeginDate: date
    EndDate: date
    Type: Literal['Month-to-month', 'One year', 'Two year']
    PaymentMethod: Literal['Bank transfer (automatic)', 'Electronic check',
                           'Credit card (automatic)', 'Mailed check']
    PaperlessBilling: Literal[0, 1]
    MonthlyCharges: Union[int, float]
    
    # phone service
    PhoneService: Literal['No line', 'Single line', 'Multi line']

    # internet service
    InternetService: Literal['No internet', 'DSL', 'Fiber optic']
    NetAddon: Optional[Union[Tuple[Literal['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                                          'TechSupport', 'StreamingTV', 'StreamingMovies'], ...], None]]

    # input data validation
    @model_validator(mode='after')
    def user_verification(self) -> Self:
        InternetService = self.InternetService
        PhoneService = self.PhoneService

        if (InternetService == 'No internet') & (PhoneService == 'No line'):
            raise ValueError("Users must use at least one of the main services, namely either telephone service or internet service.")
        return self
    
    @model_validator(mode='after')
    def check_valid_net_addon(self) -> Self:
        InternetService = self.InternetService
        NetAddon = self.NetAddon

        if (InternetService == 'No internet') & (NetAddon != None):
            raise ValueError("If InternetService is 'No internet', NetAddon must be None")
        return self

# data scheme trial
if __name__ == '__main__':
    data1 = {
        'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 0, 'Dependents': 0, 'BeginDate': date(2024, 1, 1), 
        'EndDate': date.today(), 'Type': 'Month-to-month', 'PaymentMethod': 'Bank transfer (automatic)', 
        'PaperlessBilling': 1, 'MonthlyCharges': 55.6, 'PhoneService': 'Single line', 'InternetService': 'DSL', 
        'NetAddon': ('OnlineSecurity', 'OnlineBackup')
    }

    data2 = {
        'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 0, 'Dependents': 0, 'BeginDate': date(2024, 1, 1), 
        'EndDate': date.today(), 'Type': 'Month-to-month', 'PaymentMethod': 'Bank transfer (automatic)', 
        'PaperlessBilling': 1, 'MonthlyCharges': 55.6, 'PhoneService': 'Single line', 'InternetService': 'DSL', 
        'NetAddon': None
    }

    try:
        print(user_data(**data1).model_dump())
        print()
        print(user_data(**data2).model_dump())
    
    except ValidationError as e:
        print(e)

