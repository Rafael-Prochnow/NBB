import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import io
import requests

########################################################################################################################
# primeira parte eu preciso nomear as duas tabelas confome o nome dos times
# Estão todos os dados da temporada 2019/2020

url1 = requests.get('https://lnb.com.br/nbb/tabela-de-jogos')
soup = BeautifulSoup(url1.content, 'html.parser')

resultado = soup.find(style="position:relative;")
# print(times)

tabela = pd.read_html(str(resultado))[0]
erro1 = tabela[['DATA']]
divisao1_3 = erro1["DATA"].str.split(" ")
Data = divisao1_3.str.get(0)
Hora = divisao1_3.str.get(1)

tabela["Data"] = Data
tabela["Hora"] = Hora
tabela.drop('DATA', axis=1, inplace=True)

df_01 = tabela[['Data', 'Hora', 'Unnamed: 3', 'Unnamed: 7', 'FASE', 'TRANSMISSÃO']]
df_01.columns = ['Data', 'Hora', 'Casa', 'Visitante', 'Fase', 'Local']

df_01.to_csv("tabela_01.csv", index=None)

########################################################################################################################
########################################################################################################################
# preciso pegar o conteùde de cada tabela de 1 jogo

url = 'https://lnb.com.br/nbb/tabela-de-jogos'

option = Options()
option.headless = True
driver = webdriver.Firefox()
# options=option

driver.get(url)
time.sleep(10)

########################################################################################################################
# função

driver.find_element_by_xpath(
    "//div[@class='tablebig large-12 small-12 medium-12 columns']//table//tbody//tr//td//a[@class='small-12 medium-12 "
    "large-12 float-left match_score_relatorio']").click()
time.sleep(10)

driver.find_element_by_xpath(
    "//div[@class='row tabs_content']//ul//li//a[@id='stats-label']").click()

# ai precisa fazer uma separação de conteúdos
# primeiro para uma tabelas

element = driver.find_element_by_xpath("//div[@class='stats_real_time_table_home table-wrapper float-left']//table")
html_content = element.get_attribute('outerHTML')

# passear o conteúdo em HTML
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

# Estruturar conteúdos em uma Data Frame
df_full = pd.read_html(str(table))[0]

########################################################################################################################
# divisão 1 separa da porcentagem
divisao1 = df_full["Pts C/T %"].str.split(" ")
# resultado da porcentagem
Pts_P = divisao1.str.get(1)
# separar os convertidos e tentados
divisao = df_full["Pts C/T %"].str.split("/")
# resultado dos convertidos
Pts_C = divisao.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1 = divisao.str.get(1)
divisao3 = Pts_T1.str.split(" ")
# resultado da separação
Pts_T = divisao3.str.get(0)
# add nos dados
df_full["Pts_C"] = Pts_C
df_full["Pts_T"] = Pts_T
df_full["Pts_P"] = Pts_P
# tirei a coluna "Pts C/T %"
df_full.drop('Pts C/T %', axis=1, inplace=True)

########################################################################################################################
# Organizar as colunas

# 3 PONTOS
# divisão 1 separa da porcentagem
divisao1_3 = df_full["3 P C/T %"].str.split(" ")
# resultado da porcentagem
Pts_P_3 = divisao1_3.str.get(1)
# separar os convertidos e tentados
divisao_3 = df_full["3 P C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_3 = divisao_3.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_3 = divisao_3.str.get(1)
divisao3_3 = Pts_T1_3.str.split(" ")
# resultado da separação
Pts_T_3 = divisao3_3.str.get(0)
# add nos dados
df_full["3_Pts_C"] = Pts_C_3
df_full["3_Pts_T"] = Pts_T_3
df_full["3_Pts_P"] = Pts_P_3
# tirei a coluna "Pts C/T %"
df_full.drop('3 P C/T %', axis=1, inplace=True)

# 2 PONTOS
# divisão 1 separa da porcentagem
divisao1_2 = df_full["2 P C/T %"].str.split(" ")
# resultado da porcentagem
Pts_P_2 = divisao1_2.str.get(1)
# separar os convertidos e tentados
divisao_2 = df_full["2 P C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_2 = divisao_2.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_2 = divisao_2.str.get(1)
divisao3_2 = Pts_T1_2.str.split(" ")
# resultado da separação
Pts_T_2 = divisao3_2.str.get(0)
# add nos dados
df_full["2_Pts_C"] = Pts_C_2
df_full["2_Pts_T"] = Pts_T_2
df_full["2_Pts_P"] = Pts_P_2
# tirei a coluna "Pts C/T %"
df_full.drop('2 P C/T %', axis=1, inplace=True)

# LANCE LIVRE
# divisão 1 separa da porcentagem
divisao1_LL = df_full["LL C/T %"].str.split(" ")
# resultado da porcentagem
Pts_P_LL = divisao1_LL.str.get(1)
# separar os convertidos e tentados
divisao_LL = df_full["LL C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_LL = divisao_LL.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_LL = divisao_LL.str.get(1)
divisao3_LL = Pts_T1_LL.str.split(" ")
# resultado da separação
Pts_T_LL = divisao3_LL.str.get(0)
# add nos dados
df_full["LL_Pts_C"] = Pts_C_LL
df_full["LL_Pts_T"] = Pts_T_LL
df_full["LL_Pts_P"] = Pts_P_LL
# tirei a coluna "Pts C/T %"
df_full.drop('LL C/T %', axis=1, inplace=True)

# REBOTES
# divisão 1 separa da porcentagem
divisao1_RT = df_full["RO+RD RT"].str.split(" ")
# resultado da porcentagem
RT = divisao1_RT.str.get(1)
# separar os convertidos e tentados
divisao_RO = df_full["RO+RD RT"].str.split("+")
# resultado dos convertidos
RO = divisao_RO.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
RO1 = divisao_RO.str.get(1)
divisaoRD = RO1.str.split(" ")
# resultado da separação
RD = divisaoRD.str.get(0)
# add nos dados
df_full["RO"] = RO
df_full["RD"] = RD
df_full["RT"] = RT
# tirei a coluna "Pts C/T %"
df_full.drop('RO+RD RT', axis=1, inplace=True)

########################################################################################################################
########################################################################################################################
# agora para a tabela do Visitante

elementaway = driver.find_element_by_xpath("//div[@class='stats_real_time_table_away table-wrapper float-left']//table")
html_content = elementaway.get_attribute('outerHTML')

# passear o conteúdo em HTML
soupaway = BeautifulSoup(html_content, 'html.parser')
table = soupaway.find(name='table')

# Estruturar conteúdos em uma Data Frame
df_fullaway = pd.read_html(str(table))[0]

# divisão 1 separa da porcentagem
divisao1 = df_fullaway["Pts C/T %"].str.split(" ")
# resultado da porcentagem
Pts_P = divisao1.str.get(1)
# separar os convertidos e tentados
divisao = df_fullaway["Pts C/T %"].str.split("/")
# resultado dos convertidos
Pts_C = divisao.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1 = divisao.str.get(1)
divisao3 = Pts_T1.str.split(" ")
# resultado da separação
Pts_T = divisao3.str.get(0)
# add nos dados
df_fullaway["Pts_C"] = Pts_C
df_fullaway["Pts_T"] = Pts_T
df_fullaway["Pts_P"] = Pts_P
# tirei a coluna "Pts C/T %"
df_fullaway.drop('Pts C/T %', axis=1, inplace=True)

########################################################################################################################
# Organizar as colunas

# 3 PONTOS
# divisão 1 separa da porcentagem
divisao1_3 = df_fullaway["3 P C/T %"].str.split(" ")
# resultado da porcentagem
Pts_P_3 = divisao1_3.str.get(1)
# separar os convertidos e tentados
divisao_3 = df_fullaway["3 P C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_3 = divisao_3.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_3 = divisao_3.str.get(1)
divisao3_3 = Pts_T1_3.str.split(" ")
# resultado da separação
Pts_T_3 = divisao3_3.str.get(0)
# add nos dados
df_fullaway["3_Pts_C"] = Pts_C_3
df_fullaway["3_Pts_T"] = Pts_T_3
df_fullaway["3_Pts_P"] = Pts_P_3
# tirei a coluna "Pts C/T %"
df_fullaway.drop('3 P C/T %', axis=1, inplace=True)

# 2 PONTOS
# divisão 1 separa da porcentagem
divisao1_2 = df_fullaway["2 P C/T %"].str.split(" ")
# resultado da porcentagem
Pts_P_2 = divisao1_2.str.get(1)
# separar os convertidos e tentados
divisao_2 = df_fullaway["2 P C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_2 = divisao_2.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_2 = divisao_2.str.get(1)
divisao3_2 = Pts_T1_2.str.split(" ")
# resultado da separação
Pts_T_2 = divisao3_2.str.get(0)
# add nos dados
df_fullaway["2_Pts_C"] = Pts_C_2
df_fullaway["2_Pts_T"] = Pts_T_2
df_fullaway["2_Pts_P"] = Pts_P_2
# tirei a coluna "Pts C/T %"
df_fullaway.drop('2 P C/T %', axis=1, inplace=True)

# LANCE LIVRE
# divisão 1 separa da porcentagem
divisao1_LL = df_fullaway["LL C/T %"].str.split(" ")
# resultado da porcentagem
Pts_P_LL = divisao1_LL.str.get(1)
# separar os convertidos e tentados
divisao_LL = df_fullaway["LL C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_LL = divisao_LL.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_LL = divisao_LL.str.get(1)
divisao3_LL = Pts_T1_LL.str.split(" ")
# resultado da separação
Pts_T_LL = divisao3_LL.str.get(0)
# add nos dados
df_fullaway["LL_Pts_C"] = Pts_C_LL
df_fullaway["LL_Pts_T"] = Pts_T_LL
df_fullaway["LL_Pts_P"] = Pts_P_LL
# tirei a coluna "Pts C/T %"
df_fullaway.drop('LL C/T %', axis=1, inplace=True)

# REBOTES
# divisão 1 separa da porcentagem
divisao1_RT = df_fullaway["RO+RD RT"].str.split(" ")
# resultado da porcentagem
RT = divisao1_RT.str.get(1)
# separar os convertidos e tentados
divisao_RO = df_fullaway["RO+RD RT"].str.split("+")
# resultado dos convertidos
RO = divisao_RO.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
RO1 = divisao_RO.str.get(1)
divisaoRD = RO1.str.split(" ")
# resultado da separação
RD = divisaoRD.str.get(0)
# add nos dados
df_fullaway["RO"] = RO
df_fullaway["RD"] = RD
df_fullaway["RT"] = RT
# tirei a coluna "Pts C/T %"
df_fullaway.drop('RO+RD RT', axis=1, inplace=True)

########################################################################################################################
########################################################################################################################
# juntar as duas tabelas para que seja um só dado
partida = pd.concat([df_fullaway, df_full], axis=0)

# salvar em csv
partida.to_csv("tabela_02.csv", index=None)

########################################################################################################################
# Preciso pegar as informações jogada a jogada do jogo

driver.find_element_by_xpath(
    "//div[@class='row tabs_content']//ul//li//a[@id='movethemove-label']").click()

element = driver.find_element_by_xpath("//div[@class='move_action_scroll']")
html_content = element.get_attribute('outerHTML')

# passear o conteúdo em HTML
soup_01 = BeautifulSoup(html_content, 'html.parser')

acoes = soup_01.get_text()
a = acoes.replace(' 1º', '\n1')
a1 = a.replace(' 2º', '\n2')
a2 = a1.replace(' 3º', '\n3')
a3 = a2.replace(' 4º', '\n4')
a4 = a3.replace('.			 ', ';')
a5 = a4.replace('      ', ';')
a6 = a5.replace('  ', ';')
a7 = a6.replace('    ', ';')
a8 = a7.replace('			 ', ';')
a9 = a8.replace('			 ', ';')
a10 = a9.replace('			', '')

# fazer um if caso tenha prorrogação

data = io.StringIO(a10)
df = pd.read_csv(data, sep=';', index_col=False,
                 usecols=[0, 1, 2, 3, 4, 5], header=None)
df.columns = ['Quarto', 'Tempo', 'Placar', 'Time', 'Inf_1', 'Inf_2']

divisao1_placar = df["Placar"].str.split(" x ")

placar_casa = divisao1_placar.str.get(0)
placar_visitante = divisao1_placar.str.get(1)
df['placar_casa'] = placar_casa
df['placar_visitante'] = placar_visitante
df.drop('Placar', axis=1, inplace=True)

dados = df.assign(inf_3=df.Inf_1.astype(str) + ' ' + df.Inf_2.astype(str))
dados.drop('Inf_1', axis=1, inplace=True)
dados.drop('Inf_2', axis=1, inplace=True)

divisao1_01 = dados["inf_3"]

divisao1_retirado = divisao1_01.str.translate({ord(c): " " for c in "!_+"})

a11 = divisao1_retirado.str.replace('FIM DE PARTIDA Fim de partida', 'fim_partida;')

a12 = a11.str.replace('nan', '')
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
a47 = a46.str.replace('FIM DE QUARTO Fim', 'fim_quarto;')
a48 = a47.str.replace('TEMPO TÉCNICO Técnico da equipe ', 'tempo_tecnico;')
a49 = a48.str.replace(' pede tempo', '')
a50 = a49.str.replace('do quarto quarto', '')

# adicionar e tirar os dados
dados['mudados'] = a50
dados.drop('inf_3', axis=1, inplace=True)

separar_01 = dados['mudados'].str.split(";")
Indicador = separar_01.str.get(0)
inf_02 = separar_01.str.get(1)
dados['indicador'] = Indicador
dados['inf_02'] = inf_02
dados.drop('mudados', axis=1, inplace=True)

separar_02 = dados['inf_02'].str.split(" ")
Nome = separar_02.str.get(0)
dados['Nome'] = Nome
dados.drop('inf_02', axis=1, inplace=True)

dados.to_csv("tabela_03.csv", index=None)

driver.quit()

