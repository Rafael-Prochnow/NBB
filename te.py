import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import io
import html5lib

dados = pd.read_csv('teste_06.csv')

divisao1 = dados["inf_3"]

divisao1_retirado = divisao1.str.translate({ord(c): " " for c in "!_+"})
a1 = divisao1_retirado.str.replace('FIM DE PARTIDA Fim de partida', 'fim_partida;')
a2 = a1.str.replace('INÍCIO DE QUARTO Início de partida', 'inicio_partida;')
a3 = a2.str.replace('INÍCIO DE QUARTO Início do quarto quarto', 'inicio_quarto;')
a4 = a3.str.replace('INÍCIO DE QUARTO Início do terceiro quarto', 'inicio_quarto;')
a5 = a4.str.replace('INÍCIO DE QUARTO Início do segundo quarto', 'inicio_quarto;')
a6 = a5.str.replace('FIM DE QUARTO Fim do quarto quarto', 'fim_quarto;')
a7 = a6.str.replace('FIM DE QUARTO Fim do terceiro quarto', 'fim_quarto;')
a8 = a7.str.replace('FIM DE QUARTO Fim do segundo quarto', 'fim_quarto;')
a9 = a8.str.replace('FIM DE QUARTO Fim do primeiro quarto', 'fim_quarto;')

# fora revisados os dados na primeira planilha. eu sei que está certo uma olhada pq
# os dados apresentam padrão na escrita
########################################################################################################################
# três pontos
a10 = a9.str.replace("Tentativa para três pontos ", "3_Pts_T;")
a11 = a10.str.replace('É DE TRÊS  É de três  ', '3_Pts_C;')
a12 = a11.str.replace(' erra tentativa para três pontos', '')
a13 = a12.str.replace(' acerta arremesso de três pontos', '')
# lance livre
a14 = a13.str.replace(' 1 PONTO ', 'LL_Pts_C;')
a15 = a14.str.replace('Lance Livre Errado ', 'LL_Pts_T;')
a16 = a15.str.replace(' acerta o lance livre', '')
a17 = a16.str.replace(' erra o lance livre', '')
# dois pontos
a18 = a17.str.replace('Tentativa para dois pontos ', '2_Pts_T;')
a19 = a18.str.replace(' 2 PONTOS ', '2_Pts_C;')
a20 = a19.str.replace(' erra tentativa para dois pontos', '')
a21 = a20.str.replace(' acerta arremesso de dois pontos', '')
# rebotes
a22 = a21.str.replace('REBOTE DEFENSIVO ', 'RD;')
a23 = a22.str.replace('REBOTE OFENSIVO ', 'RO;')
a24 = a23.str.replace(' pega rebote ofensivo', '')
a25 = a24.str.replace(' pega rebote defensivo', '')
# recuperação da bola
a26 = a25.str.replace('Bola recuperada ', 'BR;')
a27 = a26.str.replace(' recupera a bola', '')
# assistência
a28 = a27.str.replace('ASSISTÊNCIA Assistência do ', 'AS;')
# faltas recebidas
a29 = a28.str.replace('Falta sofrida ', 'FR;')
a30 = a29.str.replace(' sofre falta', '')
# faltas cometidas
a31 = a30.str.replace('FALTA OFENSIVA', 'FC_O;')
a32 = a31.str.replace(' comete falta ofensiva', '')
a34 = a32.str.replace('FALTA ANTIDESPORTIVA ', 'FC_A;')
a35 = a34.str.replace(' antidesportiva', '')
# substituições
a36 = a35.str.replace('Substituição Entra ', 'substituicao_entra;')
a37 = a36.str.replace('Substituição Sai ', 'substituicao_sai;')
# Erros
a38 = a37.str.replace(' Violação Estouro dos 24s', 'ER;')
a39 = a38.str.replace('Violação ', 'ER;')
a40 = a39.str.replace('Erro ', 'ER;')
a41 = a40.str.replace(' perde posse de bola', '')
a42 = a41.str.replace(' comete violação de saída de quadra', '')
a43 = a42.str.replace('nan', '')
# tocos
a44 = a43.str.replace('TOCO  ', 'TO;')
a45 = a44.str.replace(' dá um toco', '')
# tempo técnico
a46 = a45.str.replace(' TEMPO TÉCNICO Técnico da equipe ', 'tempo_tecnico;')
a47 = a46.str.replace(' pede tempo', '')
# enterrada
a48 = a47.str.replace('CRAVADA  Cravada ', 'EN;')
a49 = a48.str.replace(' acerta enterrada ', '')
#########################################################################################################
# outra revisão
a50 = a49.str.replace('FALTA TÉCNICA ', 'FC_T;')
a51 = a50.str.replace(' comete falta técnica', '')
a52 = a51.str.replace('FALTA ', 'FC;')
a53 = a52.str.replace(' comete falta', '')
# a = a.str.replace(' andou com a bola', '/ER;1')

# adicionar e tirar os dados
dados['mudados'] = a53
dados.drop('inf_3', axis=1, inplace=True)

separar_01 = dados['mudados'].str.split(";")
Indicador = separar_01.str.get(0)
dados['Indicador'] = Indicador
inf_02 = separar_01.str.get(1)

teste = inf_02.str.translate({ord(c): "," for c in "("})

teste2 = teste.str.split(',')
teste3 = teste2.str.get(0)
dados['Nomes'] = teste3
dados.drop('mudados', axis=1, inplace=True)

dados.to_csv("teste_08.csv", index=None)
