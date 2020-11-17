import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import datetime as dt


def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


def positivo(numero):
    if numero >= 0:
        pass
    else:
        numero *= -1
    return numero


def negativo(numero):
    if numero <= 0:
        pass
    else:
        numero *= -1
    return numero


r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=54')
soup = BeautifulSoup(r.content, 'html.parser')

table_inf = soup.find(name='table')
# estruturar conteúdo em uma Data Frame - Pandas
informacoes = pd.read_html(str(table_inf))[0]
Data = informacoes['DATA'][2]
Fase = informacoes['FASE'][2]
Campeonato = informacoes['CAMPEONATO'][2]


list_inoutControl = get_links_from(soup)

ano = 2019
######################################################################################################################

option = Options()
option.headless = True
driver = webdriver.Firefox()
# options=option

driver.get(list_inoutControl[2])
time.sleep(10)

driver.find_element_by_xpath(
    "//div[@class='row tabs_content']//ul//li//a[@id='stats-label']").click()

element = driver.find_element_by_xpath("//table[@class='team_general_table tablesorter tablesorter-default']")

html_content = element.get_attribute('outerHTML')

driver.find_element_by_xpath(
    "//a[@id='team_away_stats-label']").click()

element_2 = driver.find_element_by_xpath("//table[@class='team_two_table tablesorter tablesorter-default']")
html_content_2 = element_2.get_attribute('outerHTML')

# passear o conteúdo em HTML
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')


soup_2 = BeautifulSoup(html_content_2, 'html.parser')
table_2 = soup_2.find(name='table')

r1 = requests.get(list_inoutControl[2])
soup01 = BeautifulSoup(r1.content, 'html.parser')

informacoes_1 = soup01.find_all("div", class_="float-left text-right")
informacoes_2 = soup01.find_all("div", class_="float-right text-left")

nome_casa = informacoes_1[0].find("span", class_="show-for-large").get_text()
nome_fora = informacoes_2[0].find("span", class_="show-for-large").get_text()

# acontece erro por conta de nomes com siglas ai eu preciso substituir
nome_casa = nome_casa.replace('/', ' ')
nome_fora = nome_fora.replace('/', ' ')

###################################################################################################################
time_casa = pd.read_html(str(table))[0]
linhas = len(time_casa)
tamanho_casa = [nome_casa for item in range(linhas)]
tamanho_casa_adversario = [nome_fora for item01 in range(linhas)]
tamanho01_casa = ['casa' for item02 in range(linhas)]
ano_casa = [ano for item03 in range(linhas)]
Data_casa = [Data for item04 in range(linhas)]
Fase_casa = [Fase for item05 in range(linhas)]
Turno_casa = [Campeonato for item06 in range(linhas)]

time_casa['Time'] = tamanho_casa
time_casa['Casa/Fora'] = tamanho01_casa
time_casa['Oponente'] = tamanho_casa_adversario
time_casa['Temporada'] = ano_casa
time_casa['Data'] = Data_casa
time_casa['Semana'] = Fase_casa
time_casa['Classificatoria/Playoffs'] = Turno_casa


time_fora = pd.read_html(str(table_2))[0]
linhas_fora = len(time_fora)
tamanho_fora = [nome_fora for itens in range(linhas_fora)]
tamanho01_fora = ['fora' for itens01 in range(linhas_fora)]
ano_fora = [ano for itens02 in range(linhas_fora)]
tamanho_fora_adversario = [nome_casa for itens03 in range(linhas_fora)]
Data_fora = [Data for itens04 in range(linhas_fora)]
Fase_fora = [Fase for itens05 in range(linhas_fora)]
Turno_fora = [Campeonato for itens06 in range(linhas_fora)]

time_fora['Time'] = tamanho_fora
time_fora['Casa/Fora'] = tamanho01_fora
time_fora['Oponente'] = tamanho_fora_adversario
time_fora['Temporada'] = ano_fora
time_fora['Data'] = Data_fora
time_fora['Semana'] = Fase_fora
time_fora['Classificatoria/Playoffs'] = Turno_fora


#########################################################################################
df_full = pd.concat([time_casa, time_fora], axis=0)
df_full.drop(index=df_full[df_full['Jogador'] == 'Ações coletivas'].index, inplace=True)
df_full.drop('JO', axis=1, inplace=True)
df_full.drop('+/-', axis=1, inplace=True)
df_full.drop('EF', axis=1, inplace=True)
# divisão 1 separa da porcentagem
divisao1 = df_full["Pts"].str.split(" ")
# separar os convertidos e tentados
divisao = df_full["Pts"].str.split("/")
# resultado dos convertidos
Pts_C = divisao.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
Pts_T1 = divisao.str.get(1)
divisao3 = Pts_T1.str.split(" ")
# resultado da separação
Pts_T = divisao3.str.get(0)
# add nos dados
df_full["Pts_C"] = Pts_C.astype(int)
df_full["Pts_T"] = Pts_T.astype(int)

# tirei a coluna "Pts C/T %"
df_full.drop('Pts', axis=1, inplace=True)
################################################################################################################
# divisão 1 separa da porcentagem
divisao1_3 = df_full["3P%"].str.split(" ")
# separar os convertidos e tentados
divisao_3 = df_full["3P%"].str.split("/")
# resultado dos convertidos
Pts_C_3 = divisao_3.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
Pts_T1_3 = divisao_3.str.get(1)
divisao3_3 = Pts_T1_3.str.split(" ")
# resultado da separação
Pts_T_3 = divisao3_3.str.get(0)
# add nos dados
df_full["Pts_3_C"] = Pts_C_3.astype(int)
df_full["Pts_3_T"] = Pts_T_3.astype(int)
# tirei a coluna "Pts C/T %"
df_full.drop('3P%', axis=1, inplace=True)
################################################################################################################
# 2 PONTOS
# divisão 1 separa da porcentagem
divisao1_2 = df_full["2P%"].str.split(" ")
# separar os convertidos e tentados
divisao_2 = df_full["2P%"].str.split("/")
# resultado dos convertidos
Pts_C_2 = divisao_2.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
Pts_T1_2 = divisao_2.str.get(1)
divisao3_2 = Pts_T1_2.str.split(" ")
# resultado da separação
Pts_T_2 = divisao3_2.str.get(0)
# add nos dados
df_full["Pts_2_C"] = Pts_C_2.astype(int)
df_full["Pts_2_T"] = Pts_T_2.astype(int)
# tirei a coluna "Pts C/T %"
df_full.drop('2P%', axis=1, inplace=True)
################################################################################################################
# LANCE LIVRE
# divisão 1 separa da porcentagem
divisao1_LL = df_full["LL%"].str.split(" ")
# separar os convertidos e tentados
divisao_LL = df_full["LL%"].str.split("/")
# resultado dos convertidos
Pts_C_LL = divisao_LL.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
Pts_T1_LL = divisao_LL.str.get(1)
divisao3_LL = Pts_T1_LL.str.split(" ")
# resultado da separação
Pts_T_LL = divisao3_LL.str.get(0)
# add nos dados
df_full["LL_C"] = Pts_C_LL.astype(int)
df_full["LL_T"] = Pts_T_LL.astype(int)
# tirei a coluna "Pts C/T %"
df_full.drop('LL%', axis=1, inplace=True)
################################################################################################################
# REBOTES
# divisão 1 separa da porcentagem
divisao1_RT = df_full["RD+RO RT"].str.split(" ")
# resultado da porcentagem
RT = divisao1_RT.str.get(1)
# separar os convertidos e tentados
divisao_RO = df_full["RD+RO RT"].str.split("+")
# resultado dos convertidos
RD = divisao_RO.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
RO1 = divisao_RO.str.get(1)
divisaoRD = RO1.str.split(" ")
# resultado da separação
RO = divisaoRD.str.get(0)
# add nos dados
df_full["RO"] = RO.astype(int)
df_full["RD"] = RD.astype(int)
df_full["RT"] = RT.astype(int)
# tirei a coluna "Pts C/T %"
df_full.drop("RD+RO RT", axis=1, inplace=True)
####################################################################################################
# precisa colocar tirar a marcação (T) pois atapalha os nomes e não tem em todas as tabelas
nome_com_T = df_full['Jogador'].str.translate({ord(c): "," for c in "()"})
nome_sem_T = nome_com_T.str.replace(' ,T,', '')
df_full['Jogador'] = nome_sem_T

# deixando os minutos normais (deixado com :)
df_full['Min'] = df_full.Min.astype(str)
df_full['Min'] = df_full['Min'].str.replace('.', ':')
df_full['Min'] = df_full['Min'].apply(lambda x: dt.datetime.strptime(x, '%M:%S'))
df_full['Min'] = df_full['Min'].apply(lambda x: dt.time(x.hour, x.minute, x.second))
df_full['Min'] = df_full['Min'].apply(lambda x: (x.hour * 60 + x.minute) * 60 + x.second)

# ACRESCENTAR OS ARREMESSOS
df_full['Ar_Pts_C'] = df_full['Pts_3_C'] + df_full['Pts_2_C']
df_full['Ar_Pts_T'] = df_full['Pts_3_T'] + df_full['Pts_2_T']
df_full['posse_de_bola'] = round(df_full['Ar_Pts_T'] - df_full['RO'] + df_full['ER'] + (0.4 * df_full['LL_T']), 0)
df_full['posse_de_bola'] = df_full.posse_de_bola.astype(int)


# substituir os nomes de Equipes e Total. Deixar padrão.
df_full['Jogador'] = df_full['Jogador'].str.replace('Total', 'Equipe')


# substitui os valores nulos por 0
df_full.fillna(0, inplace=True)
# para verificar só aplicar linha abaixo
# enulo = dados.isnull().sum()
# converter os dados de float para int
df_full['AS'] = df_full.AS.astype(int)
df_full['BR'] = df_full.BR.astype(int)
df_full['TO'] = df_full.TO.astype(int)
df_full['FC'] = df_full.FC.astype(int)
df_full['FR'] = df_full.FR.astype(int)
df_full['ER'] = df_full.ER.astype(int)
df_full['EN'] = df_full.EN.astype(int)
df_full['Pts_C'] = df_full.Pts_C.astype(int)
df_full['Pts_T'] = df_full.Pts_T.astype(int)
df_full[''] = df_full..astype(int)
df_full[''] = df_full..astype(int)
df_full[''] = df_full..astype(int)
df_full[''] = df_full..astype(int)
df_full[''] = df_full..astype(int)
df_full[''] = df_full..astype(int)
df_full[''] = df_full..astype(int)
#########################################################################################################

placar_do_jogo = df_full[df_full['Jogador'] == 'Equipe']['Pts_C'].diff(periods=-1)
placar = list(placar_do_jogo)
dif = int(placar[0])
# valores positivos e negatovos

resultado_jogo = ['vitória' if ((x == 'casa') & (dif >= 0)) | ((x == 'fora') & (dif <= 0)) else 'derrota' for x
                  in df_full['Casa/Fora']]

dif_placar = [f'{int(positivo(dif))}' if ((x == 'casa') & (dif >= 0)) | ((x == 'fora') & (dif <= 0)) else
              f'{int(negativo(dif))}' for x in df_full['Casa/Fora']]

df_full['Vitoria/Derrota'] = resultado_jogo
df_full['Diferenca_Placar'] = dif_placar


df_full = df_full[['Temporada', 'Time', 'Oponente', 'Data', 'Semana', 'Classificatoria/Playoffs', 'Casa/Fora',
                   'Vitoria/Derrota', 'Diferenca_Placar', 'Jogador', 'Min', 'Pts_C', 'Ar_Pts_C', 'Pts_T',
                   'Ar_Pts_T', 'Pts_3_C', 'Pts_3_T', 'Pts_2_C', 'Pts_2_T', 'LL_C', 'LL_T', 'RO',
                   'RD', 'RT', 'AS', 'BR', 'TO', 'FC', 'FR', 'ER', 'EN', 'posse_de_bola']]


'''porcentagem frequencia relativa dos indicadores de cada atleta de acordo com o resultado final da partida

precisa fazer a coluna de vitória ou derrota do time e a diferença de placar '''

df_full.to_csv('parte_3.csv')
