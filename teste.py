import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

top50ranking = {}
ranking = {
    
    'points': {'field': 'PTS', 'label': 'PTS'},
    'Assistants': {'field': 'AST', 'label': 'AST'},
    'Rebound': {'field': 'REB', 'label': 'REB'},
    'Steals': {'field': 'STL', 'label': 'STL'},
    'Blocks': {'field': 'BLK', 'label': 'BLK'}
}

def buildrank(type):
    field = ranking[type]['field']
    label = ranking[type]['label']

    driver.find_element_by_xpath(f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()
    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    # Parsear o conteúdo HTML - BeutifulSoulp
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # estruturar conteúdo em uma Data Frame - Pandas
    df_full = pd.read_html(str(table))[0]
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    # Transformar os Dados em um Dicionário de dados próprio
    return df.to_dict('records')

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(
    'https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1')
time.sleep(10)

for k in ranking:
    top50ranking[k] = buildrank(k)

# converter e salvar em arquvivo JSON
js = json.dumps(top50ranking)
df = pd.read_json(js)
df.to_csv("tabnba.csv", index = None)

#top50ranking.to_csv(r"tabnba.csv", index = None)
#fp = open('ranking.json', 'w')
#fp.write(js)
#fp.close()
