import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=34')
soup = BeautifulSoup(r.content, 'html.parser')


def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


list_inoutControl = get_links_from(soup)
ano = 16
# jogo do pinheiros_x_vitória não aparece as estatísticas do jogo
del(list_inoutControl[1])
# jogo do mogi_x_vitoria não aparece as estatísticas do jogo 246
del(list_inoutControl[246])



