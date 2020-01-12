import pymysql
import pymysql.cursors
import os
import re
import pandas as pd

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='PASS',
                             db='data_mining_assignment',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

news_data = pd.read_csv('theedgemarkets_news_corporate.csv').reset_index(drop=True)

for i in range(news_data.shape[0]):
    news_item = news_data.iloc[i, :]
    company_symbol = news_item['company_symbol']
    headline = news_item['headline']
    url = news_item['url']
    datetime = news_item['datetime']
    text = news_item['text']
    in_headline = news_item['in_headline']
    is_fullname = news_item['is_fullname']
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `TheEdgeMarketsNews` (`company_symbol`, `headline`, `url`, `datetime`,"\
                " `text`, `in_headline`, `is_fullname`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (company_symbol, headline, url, datetime, text, str(in_headline), str(is_fullname)))
        connection.commit()
    except BaseException:
        print('Error while inserting a new entry into the database')
        print(BaseException)
connection.close()
