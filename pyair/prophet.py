import pandas as pd
from fbprophet import Prophet
import sys
sys.path.append("../")
from pyair.process_data import *
from pyair.imputer import *

    
def get_prophet(n):
    #n means predicting days 
    df = main()
    
    df=time_interpolation_impute(df).reset_index().rename(columns={'index':'ds', 'Shanghai':'y'})
    model = Prophet()
    model.fit(df)
    
    future = model.make_future_dataframe(periods=n)
    
    forecast = model.predict(future)
    forecast[['ds','yhat','yhat_lower','yhat_upper']]
    fig2 = model.plot(forecast)
    model.plot_components(forecast)





# df_main = main()
# get_prophet(df_main)
    
    