import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get('https://lnb.com.br/partidas/nbb-2019-2020-unifacisa-x-rio-claro-12102019-1600/')
soup = BeautifulSoup(r.content, 'html.parser')

informacoes_1 = soup.find_all("div", class_="float-left text-right")
informacoes_2 = soup.find_all("div", class_="float-right text-left")

nome_casa = informacoes_1[0].find("span", class_="show-for-large").get_text()
nome_fora = informacoes_2[0].find("span", class_="show-for-large").get_text()

print(nome_casa)
print(nome_fora)

'''
r = requests.get('https://lnb.com.br/noticias/basquete-cearense-87-x-90-renata-rio-claro/')
soup = BeautifulSoup(r.content, 'html.parser')

informacoes_1 = soup.find_all("div", class_="score_header large-12 small-12 medium-12 columns")
informacoes_2 = soup.find_all("div", class_="float-right text-left score_header_right")

nome_casa = informacoes_1[0].find("span", class_="show-for-large").get_text()
nome_fora = informacoes_2[0].find("span", class_="show-for-large").get_text()
print(nome_casa)
print(nome_fora)

'''
'''
tabela_casa = soup.find_all("div", class_="stats_real_time_table_away table-wrapper float-left")
df_casa = pd.read_html(str(tabela_casa))[0]
print(df_casa)

r = requests.get('https://lnb.com.br/noticias/e-do-mogi-paulistano/')
soup = BeautifulSoup(r.content, 'html.parser')

tabela_casa = soup.find_all(id="team_home_stats")
df_casa = pd.read_html(str(tabela_casa))[0]
print(tabela_casa)

tabela_fora = soup.find_all(id="team_away_stats")
df_fora = pd.read_html(str(tabela_fora))[0]
print(df_fora)
'''
