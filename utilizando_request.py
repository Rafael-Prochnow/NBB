import requests
from bs4 import BeautifulSoup

r = requests.get('https://lnb.com.br/noticias/e-do-mogi-paulistano/')
soup = BeautifulSoup(r.content, 'html.parser')

tabela_casa = soup.find_all(id="team_home_stats")
tabela_fora = soup.find_all(id="team_away_stats")


