import time
from bs4 import BeautifulSoup
import pandas as pd
import requests

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=47')
soup = BeautifulSoup(r.content, 'html.parser')


def get_links_from(teste):
    links = []
    for a in teste.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


list_inoutControl = get_links_from(soup)

print(list_inoutControl)

'''pagina = requests.get('https://lnb.com.br/noticias/primeira-vitoria-corinthians-paulistano-nbb/')
erro_na_pagina = BeautifulSoup(pagina.content, 'html.parser')
erro_na_pagina01 = erro_na_pagina.find_all("b")
erro_na_pagina02 = erro_na_pagina01[0].get_text()'''

ii = 1
lista_funcionando = []
lista_falha = []
for i in list_inoutControl:
    pagina = requests.get(f'{i}')
    erro_na_pagina = BeautifulSoup(pagina.content, 'html.parser')
    erro_na_pagina01 = erro_na_pagina.find_all("b")
    erro_na_pagina02 = erro_na_pagina01[0].get_text()

    if erro_na_pagina02 != 'Fatal error':
        print(f'{ii}')
        lista_funcionando.append(i)
        ii += 1
    elif erro_na_pagina02 == 'Fatal error':
        print(f'Essa página {i} não está funcionando')
        lista_falha.append(i)
        ii += 1

print(len(lista_funcionando))
print(len(lista_falha))
