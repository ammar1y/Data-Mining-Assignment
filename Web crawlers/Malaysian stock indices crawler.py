"""
This script crawls data about Malaysian stock indices and stores the output in a csv file.
"""

import requests
from bs4 import BeautifulSoup
import time

#Website to get the indices
base_url = 'https://www.investing.com/indices/malaysia-indices?'

print('Scraping: ' + base_url)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
           '10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/72.0.3626.109 Safari/537.36'}
html_doc = requests.get(base_url, headers=headers).text
        # parse the HTML contents using BeautifulSoup parser
soup = BeautifulSoup(html_doc, 'html.parser')

#KLCI
indiceKLCI = soup.select_one('#pair_29078 > td.bold.left.noWrap.elp.plusIconTd > a').text
LastA = soup.select_one('#pair_29078 > td.pid-29078-last').text
LastA = LastA.replace(",","")                        
HighA = soup.select_one('#pair_29078 > td.pid-29078-high').text 
HighA = HighA.replace(",","")                                               
LowA = soup.select_one('#pair_29078 > td.pid-29078-low').text
LowA = LowA.replace(",","")                                             

#Malaysia ACE                        
indiceMalaysiaACE = soup.select_one('#pair_29075 > td.bold.left.noWrap.elp.plusIconTd > a').text
LastB = soup.select_one('#pair_29075 > td.pid-29075-last').text 
LastB = LastB.replace(",","")                        
HighB = soup.select_one('#pair_29075 > td.pid-29075-high').text
HighB = HighB.replace(",","")                        
LowB =  soup.select_one('#pair_29075 > td.pid-29075-low').text                       
LowB = LowB.replace(",","")                      

#FTSE BM Mid 70
indiceFTSEBMMid70 = soup.select_one('#pair_29076 > td.bold.left.noWrap.elp.plusIconTd > a').text                                    
LastC = soup.select_one('#pair_29076 > td.pid-29076-last').text
LastC = LastC.replace(",","")                        
HighC = soup.select_one('#pair_29076 > td.pid-29076-high').text
HighC = HighC.replace(",","")                        
LowC = soup.select_one('#pair_29076 > td.pid-29076-low').text
LowC = LowC.replace(",","")                       

#Malaysia Top 100                        
indiceMalaysiaTop100 = soup.select_one('#pair_29077 > td.bold.left.noWrap.elp.plusIconTd > a').text
LastD = soup.select_one('#pair_29077 > td.pid-29077-last').text
LastD = LastD.replace(",","")                        
HighD = soup.select_one('#pair_29077 > td.pid-29077-high').text
HighD = HighD.replace(",","")                        
LowD = soup.select_one('#pair_29077 > td.pid-29077-low').text
LowD = LowD.replace(",","")                       
                                             
indice_name = [indiceKLCI, indiceMalaysiaACE, 
                   indiceFTSEBMMid70, indiceMalaysiaTop100]
Last = [LastA, LastB, LastC, LastD]
High = [HighA, HighB, HighC, HighD]
Low = [LowA, LowB, LowC, LowD]
Time = [time.strftime('%H:%M'),time.strftime('%H:%M') , 
        time.strftime('%H:%M'), time.strftime('%H:%M')]
Date = [time.strftime('%d-%b-%Y'),time.strftime('%d-%b-%Y'),
        time.strftime('%d-%b-%Y'),time.strftime('%d-%b-%Y')]

# save the scraped prices to a file whose name contains the
# current datetime
file_name = 'indices_' + time.strftime('%d-%b-%Y_%H-%M') + '.csv'
with open(file_name, 'w') as f:
    for A, B, C, D, G, H in zip(indice_name, Last, High, 
    Low, Date, Time):
        f.write(A + ',' + B + ',' + C + ',' + D + ','  +  '[' + G + '|' + H + ']' + '\n')
        
        
