import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

os.chdir(os.path.dirname(os.path.realpath(__file__)))

url = 'https://www.theedgemarkets.com/categories/corporate?page={}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
           '10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/72.0.3626.109 Safari/537.36'}

company_symbols = []
with open("data/company_symbols.txt") as f:
    for line in f:
        company_symbols.append(line.strip())

company_fullnames = []
with open("data/company_fullnames.txt") as f:
    for line in f:
        company_fullnames.append(line.strip())

company_fullnames = [re.sub(r'(.*:\s*)|(\s*\(.*\))|(\s*BERHAD)|(\s*BHD)', '', com_fn) for com_fn in company_fullnames]
company_fullnames = [re.sub(r'(^CW\s*)|(^PW\s*)', '', com_fn) for com_fn in company_fullnames]
company_fullnames = [x.lower() for x in company_fullnames]
# company_symbols = [x.lower() for x in company_symbols]

if not os.path.exists('theedgemarkets_news_corporate.csv'):
    news_df = pd.DataFrame(columns=['company_symbol', 'headline', 'url', 'datetime', 'text', 'in_headline', 'is_fullname'])
else:
    news_df = pd.read_csv('theedgemarkets_news_corporate.csv')

counter = news_df.shape[0]
errors = []
for i in range(1, 500):
    print('[', i, ']')
    page_url = url.format(i)
    res = requests.get(page_url, headers=headers).text
    soup = BeautifulSoup(res, 'html.parser')
    news_elems = soup.select('.views-field-title .field-content a')
    for news_e in news_elems:
        article_headline = news_e.text
        article_url = 'https://www.theedgemarkets.com' + news_e.get('href')
        try:
            article_res = requests.get(article_url, headers=headers).text
            article_soup = BeautifulSoup(article_res, 'html.parser')
            article_text = article_soup.select_one('.field-type-text-with-summary .field-items .field-item')
            if article_text is None:
                article_text = article_soup.select_one('.field-type-text-long .field-items .field-item')
            article_text = article_text.text
            article_date = article_soup.select_one('.content-first .post-meta .post-created').text
            if article_url not in news_df['url'].tolist():
                for j in range(len(company_fullnames)):
                    if (re.search(pattern=r'\b'+re.escape(company_fullnames[j])+r'\b', string=article_headline.lower())):
                        news_df.loc[news_df.shape[0], :] = (company_symbols[j], article_headline, article_url, article_date, article_text, 'Yes', 'Yes')
                        counter += 1
                    elif (re.search(pattern=r'\b'+re.escape(company_symbols[j])+r'\b', string=article_headline)):
                        news_df.loc[news_df.shape[0], :] = (company_symbols[j], article_headline, article_url, article_date, article_text, 'Yes', 'No')
                        counter += 1
                    elif (re.search(pattern=r'\b'+re.escape(company_fullnames[j])+r'\b', string=article_text.lower())):
                        news_df.loc[news_df.shape[0], :] = (company_symbols[j], article_headline, article_url, article_date, article_text, 'No', 'Yes')
                        counter += 1
                    elif (re.search(pattern=r'\b'+re.escape(company_symbols[j])+r'\b', string=article_text)):
                        news_df.loc[news_df.shape[0], :] = (company_symbols[j], article_headline, article_url, article_date, article_text, 'No', 'No')
                        counter += 1
        except:
            print(article_url)
    print(counter)

news_df.to_csv('theedgemarkets_news_corporate.csv', index=False)
