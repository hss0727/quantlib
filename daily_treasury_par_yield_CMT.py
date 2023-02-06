from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import numpy as np

def get_rates(time_period: str):
  """
  Get Treasury Pary Yiedl (CMT) data from US Department of the Treasury
  https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics
  :param time_period: YYYY or YYYYMM (ex. '2023', '202322'
  :return: DataFrame
  """
  url_base = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xmlview?data=daily_treasury_yield_curve&field_tdr_date_value_month='
  period = str(time_period)
  url = url_base + period

  # Get Market Information
  req = requests.get(url)
  soup = BeautifulSoup(req.text, 'lxml')
  data = soup.find_all("content")

  # Create DataFrame
  mat = ['date','1m','2m','3m','4m','6m','1y','2y','3y','5y','7y','10y','20y','30y']
  df_rates = pd.DataFrame(columns = mat)

  # Append data to DataFrame
  for i in range(len(data)):
    yields = data[i].find('m:properties').text.split('\n')[1:-2]
    df_rates.loc[i] = yields

  df_rates.set_index('date', drop=True, inplace=True)
  df_rates.index = pd.to_datetime(df_rates.index)

  return df_rates