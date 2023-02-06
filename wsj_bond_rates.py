import pandas as pd
import numpy as np
import requests
import datetime
from bs4 import BeautifulSoup

def get_rates_WSJ():
  """
  Get Treasury Bond rates from Wall Street Journal
  :return: quote_date, DataFrame
  """
  mat = ['01M', '03M', '06M', '01Y', '02Y', '03Y', '05Y', '07Y', '10Y', '30Y']
  headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

  # Create empty DataFrame
  cols = ['tenor', 'maturity', ' days_to_mat', 'coupon', 'rate', 'price']
  df = pd.DataFrame(columns=cols)
  df['tenor'] = mat
  df.set_index('tenor')

  for i in range(len(mat)):
    url_base = 'https://www.wsj.com/market-data/quotes/bond/BX/TMUBMUSD' 
    url = url_base + mat[i] + '?mod=md_bond_overview_quote'
  
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')

    quote_date = soup.find("span", id="quote_dateTime").text
    rate = soup.find("span", id="quote_val").text.replace("%","")
    p = soup.find("span", id="price_quote_val").text
    p_split1 = p.split(" ")
    p_split2 = p_split1[1].split("/")
    price = float(p_split1[0]) + float(p_split2[0]) / float(p_split2[1])

    other_data = soup.find_all("span", {"class": "data_data"})

    if i > 3:
      coupon = other_data[2].text.replace("%","")
    else:
      coupon = 0

    eff_date = pd.to_datetime(quote_date, format="%I:%M %p %Z %m/%d/%y")
    maturity = pd.to_datetime(other_data[3].text, format="%m/%d/%y").tz_localize('EST')
    days_to_mat = (maturity - eff_date).days

    result = [mat[i], maturity, days_to_mat, coupon, rate, price]
    df.loc[df['tenor']==mat[i]] = result
  
  df['maturity'] = df['maturity'].apply(lambda x: x.date())

  return quote_date, df