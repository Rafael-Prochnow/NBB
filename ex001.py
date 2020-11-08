import time
from bs4 import BeautifulSoup
import pandas as pd
import requests

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=41&wherePlaying=-1&played=-1')
soup = BeautifulSoup(r.content, 'html.parser')


def get_links_from(teste):
    links = []
    for a in teste.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links

#
#

'''
lista_de_temporadas = ['https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=54&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=47',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=41&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=34',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=27&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=15',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=8&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=4',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=3&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=2',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=1&wherePlaying=-1&played=-1']
                       
'''

lista_de_temporadas = ['https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=41&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=34']


lista_funcionando = []
lista_falha = []
list_sites_funciona = []
list_sites_falha = []



'''

list_inoutControl = get_links_from(soup)del(list_inoutControl[:134])
print(list_inoutControl)

r = requests.get(list_inoutControl[1])

erro_na_pagina = BeautifulSoup(r.content, 'html.parser')
# erro_na_pagina01 = erro_na_pagina.find_all("b")

# erro_na_pagina02 = erro_na_pagina01[0].get_text()
# print(erro_na_pagina02)'''


iii = 17
for x in lista_de_temporadas:
    print(f'Temporada {iii}')
    r = requests.get(x)
    soup = BeautifulSoup(r.content, 'html.parser')
    list_inoutControl = get_links_from(soup)
    ii = 1
    for i in list_inoutControl:
        pagina = requests.get(f'{i}')
        erro_na_pagina = BeautifulSoup(pagina.content, 'html.parser')
        if not erro_na_pagina.find_all("b"):
            print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
            lista_falha.append(i)
            print(lista_falha)
            ii += 1
        else:
            erro_na_pagina01 = erro_na_pagina.find_all("b")
            erro_na_pagina02 = erro_na_pagina01[0].get_text()
            if erro_na_pagina02 != 'Fatal error':
                print(f'{ii}')
                lista_funcionando.append(i)
                ii += 1
            elif erro_na_pagina02 == 'Fatal error':
                print(f'Essa página {i} não está funcionando')
                lista_falha.append(i)
                print(lista_falha)
                ii += 1
    iii -= 1
    list_sites_funciona.append(lista_funcionando)
    list_sites_falha.append(lista_falha)

print(list_sites_funciona)
print(len(list_sites_funciona))
print(list_sites_falha)
print(len(list_sites_falha))
