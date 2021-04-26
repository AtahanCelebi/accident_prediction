"""
Created: 27/04/2021
@author: AtahanCelebi
"""
import pandas as pd
from datetime import datetime
accident_data = pd.read_json("C:\\Users\\HU-ISSD\Desktop\\tweets.json",orient="split")

fmt = '%Y-%m-%d %H:%M:%S'


shaped_time_tweets = ['%s-%s-%s %s:%s:%s' % (
    datetime.strptime(str(i), fmt).strftime("%Y"), datetime.strptime(str(i), fmt).strftime("%m"),
    datetime.strptime(str(i), fmt).strftime("%d"), datetime.strptime(str(i), fmt).strftime("%H"),
    datetime.strptime(str(i), fmt).strftime("%M"),
    datetime.strptime(str(i), fmt).strftime("%S")) for i in accident_data.created_at]

