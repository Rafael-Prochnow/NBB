import time
from bs4 import BeautifulSoup
import pandas as pd

# teste
dados = pd.read_csv('teste_07.csv')

divisao1 = dados["Indicador_01"]

a1 = divisao1.str.replace('Fim de partida', '1/fim_partida;')
a2 = a1.str.replace('Início de partida', '1/inicio_partida;')
a3 = a2.str.replace('Início do  primeiro quarto', '1/inicio_quarto;')
a4 = a3.str.replace('Início do  segundo quarto', '1/inicio_quarto;')
a5 = a4.str.replace('Início do  terceiro quarto', '1/inicio_quarto;')
a6 = a5.str.replace('Início do  quarto quarto', '1/inicio_quarto;')
a7 = a6.str.replace('Fim  do quarto quarto', '/fim_quarto;')
a8 = a7.str.replace('Fim  do terceiro quarto', '1/fim_quarto;')
a9 = a8.str.replace('Fim  do segundo quarto', '1/fim_quarto;')
a10 = a9.str.replace('Fim  do primeiro quarto', '1/fim_quarto;')

####################################################################################################
# esses são os valores que estão os indicadores
a11 = a10.str.replace('É de três  ', '')
a12 = a11.str.replace(' acerta arremesso de três pontos', '/3_Pts_C;1')
a13 = a12.str.replace(' erra tentativa para três pontos', '/3_Pts_T;1')
# lance livre
a14 = a13.str.replace(' acerta o lance livre', '/LL_Pts_C;1')
a15 = a14.str.replace(' erra o lance livre', '/LL_Pts_T;1')
# Dois pontos
a16 = a15.str.replace(' acerta arremesso de dois pontos', '/2_Pts_C;1')
a17 = a16.str.replace(' erra tentativa para dois pontos', '/2_Pts_T;1')
# rebotes
a18 = a17.str.replace(' pega rebote defensivo', '/RD;1')
a19 = a18.str.replace(' pega rebote ofensivo', '/RO;1')
# recuperação de bola
a20 = a19.str.replace(' recupera a bola', '/BR;1')
# assistencia
a21 = a20.str.replace('Assistência do ', '/AS;')
# faltas recebidas
a22 = a21.str.replace(' sofre falta', '/FR;1')
# faltas cometidas
a23 = a22.str.replace(' comete falta técnica', '/FC_T;1')
a24 = a23.str.replace(' comete falta antidesportiva', '/FC_A;1')
a25 = a24.str.replace(' comete falta ofensiva', '/FC_O;1')
a26 = a25.str.replace(' comete falta', '/FC;1')
# substituição
a27 = a26.str.replace('Entra ', '/substituicao_entra;')
a28 = a27.str.replace('Sai ', '/substituicao_sai;')
# erros
a29 = a28.str.replace(' perde posse de bola', '/ER;1')
a30 = a29.str.replace('Estouro dos 24s', '/ER;1')
a31 = a30.str.replace(' andou com a bola', '/ER;1')
a32 = a31.str.replace(' comete violação de saída de quadra', '/ER;1')
# tocos
a33 = a32.str.replace(' dá um toco', '/TO;1')
# tempo técnico
a34 = a33.str.replace('Técnico da equipe ', '')
a35 = a34.str.replace(' pede tempo ', '/tempo_tecnico;')
# cravada
a36 = a35.str.replace('Cravada ', '')
a37 = a36.str.replace(' acerta enterrada', '/EN;1')

# primeira separação é coloco na ordem dos nomes e depois indicadores
# o ; é para fazer a primeira separação
# 1 é para conter um valor apenas, pois quando separo e junto, caso não tenha um valor, o resultado retira os valores
mudados_00 = a37.str.split(';')
mudados_01 = mudados_00.str.get(1)
mudados_02 = mudados_00.str.get(0)

alinhados = mudados_01 + mudados_02
# agora que juntou e alinhou os nomes
# organizar novamente
alinhados_01 = alinhados.str.split('/')
alinhados_02 = alinhados_01.str.get(0)
alinhados_03 = alinhados_01.str.get(1)

# depois de separado vamos organizar por nomes e retirar os valores que ajudaram na primeira separação, como 1 e espaço

alinhados_04 = alinhados_02.str.replace('1 ', '')
alinhados_05 = alinhados_04.str.replace(' 1', '')

dados["Indicador"] = alinhados_03
dados["Nomes"] = alinhados_05
dados.drop('Indicador_01', axis=1, inplace=True)
dados.to_csv("teste_08.csv", index=None)

