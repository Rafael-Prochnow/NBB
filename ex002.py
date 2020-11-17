import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException
import io
import re
import numpy as np
import datetime as dt

'''
def get_links_from(teste):
    links = []
    for a in teste.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


tabela_geral = pd.DataFrame([])
lista_cada_temporada = pd.DataFrame([])
lista_funcionando = []
lista_falha = []
list_sites_falha = []
list_sites_funciona = []
l1 = pd.DataFrame([])
l2 = pd.DataFrame([])

# essa é a ordem das temporadas
temporada = 2019
lista_de_temporadas = [54, 47, 41, 34, 27, 20, 15]

for x in lista_de_temporadas:
    print(f'Temporada {temporada}')
    r = requests.get(f'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D={x}')
    soup = BeautifulSoup(r.content, 'html.parser')
    list_inoutControl = get_links_from(soup)
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
            if (i == 'https://lnb.com.br/partidas/nbb-20162017-paulistano-x-caxias-do-sul-20122016-1930/')|\
                    (i == 'https://lnb.com.br/noticias/com_personalidade_/')|\
                    (i == 'https://lnb.com.br/noticias/mais-do-que-especial-2/')|\
                    (i == 'https://lnb.com.br/noticias/agora-sim-5/'):
                print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
                lista_falha.append(i)
                numero_jogo += 1
            elif erro_na_pagina02 != 'Fatal error':
                print(f'Jogo {numero_jogo}')
                lista_funcionando.append(i)
            elif erro_na_pagina02 == 'Fatal error':
                print(f'Essa página {i} não está funcionando')
                lista_falha.append(i)
                numero_jogo += 1
    # retorna uma tabela geral de cada temporada
    lista_cada_temporada = pd.concat([tabela_geral, lista_cada_temporada], axis=0)
    tabela_geral.to_csv('Dados01/temporada ' + f'{temporada}' + '/Total_de_acao_acao_' + f'{temporada}' + '.csv')
    # retorna os sites que funcionam de cada temoporada
    list_sites_funciona = pd.DataFrame(lista_funcionando)
    list_sites_funciona.to_csv('Dados01/temporada ' + f'{temporada}' + '/funcionando_' + f'{temporada}' + '.csv')
    l1 = pd.concat([list_sites_funciona, l1], axis=0)
    # retorna os sites que NÃO funcionam de cada temoporada
    list_sites_falha = pd.DataFrame(lista_falha)
    list_sites_falha.to_csv('Dados01/temporada ' + f'{temporada}' + '/falha_' + f'{temporada}' + '.csv')
    l2 = pd.concat([list_sites_falha, l2], axis=0)
    # zera informações das temporadas
    tabela_geral = pd.DataFrame([])
    list_sites_funciona = []
    list_sites_falha = []
    temporada -= 1


lista_cada_temporada.to_csv('Dados01/Total_de_acao_acao.csv')
l1.to_csv('Dados01/funcionando.csv')
l2.to_csv('Dados01/falha.csv')'''

df = pd.read_csv('parte_3.csv')

df.drop(index=df[df['Jogador'] == 'Ações coletivas'].index, inplace=True)
a = df[df['Jogador'] == 'Equipe']['Min']
df['Min'] = df.Min.astype(str)
df['Min'] = df['Min'].str.replace('.', ':')


df['Min'] = df['Min'].apply(lambda x: dt.datetime.strptime(x, '%M:%S'))
df['Min'] = df['Min'].apply(lambda x: dt.time(x.hour, x.minute, x.second))
df['Min'] = df['Min'].apply(lambda x: (x.hour * 60 + x.minute) * 60 + x.second)
print(df['Min'])
