"""
This script stores crawled The Star news data in a MySQL database table.
"""

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
                             password='Asdlkj987!23',
                             db='data_mining_assignment',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

company_info = pd.read_csv('../data/company_info.csv').reset_index(drop=True)

											

for i in range(company_info.shape[0]):
    item = company_info.iloc[i, :]
    company_full_name = str(item['company_full_name'])
    company_symbol = str(item['company_symbol'])
    last_quarter = str(item['last_quarter'])
    last_quarter_revenue_000 = str(item['last_quarter_revenue_000'])
    last_quarter_net_profit_000 = str(item['last_quarter_net_profit_000'])
    board = str(item['board'])
    shariah_compliant = str(item['shariah_compliant'])
    sector = str(item['sector'])
    sub_sector = str(item['sub_sector'])
    market_capital = str(item['market_capital'])
    num_of_share = str(item['num_of_share'])
    roe = str(item['roe'])

    try:
        with connection.cursor() as cursor:
            # Create new records
            sql = "INSERT INTO `CompanyInfo` (`company_fullname`, `company_symbol`, `last_quarter`, `last_quarter_revenue_000`,"\
                " `last_quarter_net_profit_000`, `board`, `shariah_compliant`, `sector`, `sub_sector`, `market_capital`,"\
                " `num_of_share`, `roe`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (company_full_name, company_symbol, last_quarter, last_quarter_revenue_000, last_quarter_net_profit_000, board,
                                 shariah_compliant, sector, sub_sector, market_capital, num_of_share, roe))
        connection.commit()
    except Exception as e:
        # print('Error while inserting a new entry into the database')
        print(e)
connection.close()
