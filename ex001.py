import time
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import re

dados = pd.read_csv('parte_3.csv')
# pegar a coluna individual, separar o que precisa ser separado e depois juntar a coluna principal

divisao1 = dados["Inf_1"]

# pesquisar replace com translate (pq o sinal de + fode tudo)
divisao1_retirado = divisao1.str.translate({ord(c): " " for c in "!_+"})

a11 = divisao1_retirado.str.replace('FIM DE PARTIDA Fim de partida', 'fim_partida;')
a12 = a11.str.replace('FIM DE QUARTO Fim', 'fim_quarto;')
a13 = a12.str.replace("Tentativa para três pontos ", "3_Pts_T;")
a14 = a13.str.replace('É DE TRÊS  É de três  ', '3_Pts_C;')
a15 = a14.str.replace(' 1 PONTO ', 'LL_Pts_C;')
a16 = a15.str.replace('Lance Livre Errado ', 'LL_Pts_T;')
a17 = a16.str.replace('Tentativa para dois pontos ', '2_Pts_T;')
a18 = a17.str.replace(' 2 PONTOS ', '2_Pts_C;')
a19 = a18.str.replace('Falta sofrida ', 'FR;')
a20 = a19.str.replace('FALTA ', 'FC;')
a21 = a20.str.replace('REBOTE DEFENSIVO ', 'RD;')
a22 = a21.str.replace('REBOTE OFENSIVO ', 'RO;')
a23 = a22.str.replace('Substituição Entra ', 'substituicao_entra;')
a24 = a23.str.replace('Substituição Sai ', 'substituicao_sai;')
a25 = a24.str.replace('Bola recuperada ', 'BR;')
a26 = a25.str.replace('ASSISTÊNCIA Assistência do ', 'AS;')
a27 = a26.str.replace('INÍCIO DE QUARTO Início do', 'inicio_quarto;')
a28 = a27.str.replace('INÍCIO DE QUARTO Início de partida', 'inicio_partida;')

#################################################################################
# separação das colunas

a29 = a28.str.replace(' erra tentativa para três pontos', '')
a30 = a29.str.replace(' acerta arremesso de três pontos', '')
a31 = a30.str.replace(' pega rebote ofensivo', '')
a32 = a31.str.replace(' pega rebote defensivo', '')
a33 = a32.str.replace(' erra tentativa para dois pontos', '')
a34 = a33.str.replace(' acerta arremesso de dois pontos', '')
a35 = a34.str.replace(' comete falta ofensiva', '')
a36 = a35.str.replace(' sofre falta', '')
a37 = a36.str.replace(' comete falta', '')
a38 = a37.str.replace(' perde posse de bola', '')
a39 = a38.str.replace(' acerta o lance livre', '')
a40 = a39.str.replace(' erra o lance livre', '')
a41 = a40.str.replace(' comete violação de saída de quadra', '')
a42 = a41.str.replace(' recupera a bola', '')
a43 = a42.str.replace('Erro ', 'ER;')
########################################################################################################################
# alguns que faltaram
a44 = a43.str.replace('Violação ', 'ER;')
a45 = a44.str.replace('TOCO  ', 'TO;')
a46 = a45.str.replace(' dá um toco', '')

# adicionar e tirar os dados
dados['mudados'] = a46
dados.drop('Inf_1', axis=1, inplace=True)

separar_01 = dados['mudados'].str.split(";")
Indicador = separar_01.str.get(0)
Nome = separar_01.str.get(1)
dados['indicador'] = Indicador
dados['nome'] = Nome
dados.drop('mudados', axis=1, inplace=True)

mudados_01 = dados['Inf_2']
mudados_02 = mudados_01.str.translate({ord(c): "zzz " for c in "("})
mudados_03 = mudados_02.replace('^.*zzz.*$', np.nan, regex=True)
dados['inf_2'] = mudados_03
dados.drop('Inf_2', axis=1, inplace=True)

########################################################################################################################
dados.to_csv("teste_01.csv", index=None)

# 'TEMPO TÉCNICO Técnico da equipe ', 'TEMPO_TÉCNICO;'
