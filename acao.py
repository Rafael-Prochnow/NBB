import time
from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


lista_funcionando = []
lista_falha = []
# essa é a ordem das temporadas
temporada = 2015
lista_de_temporadas = [27, 20, 15]

tabela_geral = pd.DataFrame([])
for x in lista_de_temporadas:
    print(f'Temporada {temporada}')
    r = requests.get(f'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D={x}')
    soup = BeautifulSoup(r.content, 'html.parser')
    list_inoutControl = get_links_from(soup)
    print(list_inoutControl)
    numero_jogo = 1
    for i in list_inoutControl:
        pagina = requests.get(f'{i}')
        erro_na_pagina = BeautifulSoup(pagina.content, 'html.parser')
        if not erro_na_pagina.find_all("b"):
            print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
            lista_falha.append(i)
            numero_jogo += 1
        else:
            erro_na_pagina01 = erro_na_pagina.find_all("b")
            erro_na_pagina02 = erro_na_pagina01[0].get_text()
            # por motivos de erro da página coloquei isso
            if (i == 'https://lnb.com.br/partidas/nbb-20162017-paulistano-x-caxias-do-sul-20122016-1930/') | \
                    (i == 'https://lnb.com.br/noticias/com_personalidade_/') | \
                    (i == 'https://lnb.com.br/noticias/mais-do-que-especial-2/') | \
                    (i == 'https://lnb.com.br/noticias/agora-sim-5/'):
                print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
                lista_falha.append(i)
                numero_jogo += 1
            elif erro_na_pagina02 != 'Fatal error':
                print(f'Jogo {numero_jogo}')
                lista_funcionando.append(i)
                numero_jogo += 1
            elif erro_na_pagina02 == 'Fatal error':
                print(f'Essa página {i} não está funcionando')
                lista_falha.append(i)
                numero_jogo += 1
    temporada -= 1
