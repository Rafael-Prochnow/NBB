import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException
import io

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=27&wherePlaying=-1&played=-1')
soup = BeautifulSoup(r.content, 'html.parser')


def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


list_inoutControl = get_links_from(soup)

option = Options()
option.headless = True
driver = webdriver.Firefox()
# options=option
driver.get(list_inoutControl[1])
time.sleep(10)

driver.find_element_by_xpath(
    "//div[@class='row tabs_content']//ul//li//a[@id='movethemove-label']").click()

element = driver.find_element_by_xpath("//div[@class='move_action_scroll column']")
html_content = element.get_attribute('outerHTML')


# passear o conteúdo em HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 3 encontra o time, está separado dos demais
items02 = soup.find_all(class_='large-10 small-8 medium-10 columns move_action_content move_action_content_one')
time_site = [nome_time.find('p').get_text() for nome_time in items02]
# passa para primeira inf encontra quarto tempo placar
items = soup.find_all(class_='large-2 small-4 medium-2 columns move_action_time')
quarto = [nome_quarto.find(class_='quarter').get_text() for nome_quarto in items]
tempo = [nome_tempo.find(class_='time').get_text() for nome_tempo in items]
placar = [nome_placar.find(class_='points').get_text() for nome_placar in items]
# passa para outra parte pegando nome e indicador que depois precisa fazer a separação
items01 = soup.find_all(class_='move_action_content_text')
acao_pessoa02 = [nome_acao_pessoa02.find("p", class_='').get_text() for nome_acao_pessoa02 in items01]

dados = pd.DataFrame(
    {'Quarto': quarto,
     'Tempo': tempo,
     'Time_01': time_site,
     'Placar': placar,
     'Inf_2': acao_pessoa02
     })

# erro de espaços vindo de cima

Indicador01 = dados['Time_01'].str.replace(
    '.                                                                    \n\n', '')
# limpeza dos dados tirando Fim de partida e dos quartos

erro02 = Indicador01.str.replace('Fim de partida', 'NaN')
erro03 = erro02.str.replace('Fim  do quarto quarto', 'NaN')
erro04 = erro03.str.replace('Início do  quarto quarto', 'NaN')
erro05 = erro04.str.replace('Fim  do terceiro quarto', 'NaN')
erro06 = erro05.str.replace('Início do  terceiro quarto', 'NaN')
erro07 = erro06.str.replace('Fim  do segundo quarto', 'NaN')
erro08 = erro07.str.replace('Início do  segundo quarto', 'NaN')
erro09 = erro08.str.replace('Fim  do primeiro quarto', 'NaN')
erro10 = erro09.str.replace('Início do  primeiro quarto', 'NaN')
Indicador_consertado = erro10.str.replace('Início de partida', 'NaN')
# deve ter prorrogação!!!!

dados['Time'] = Indicador_consertado
dados.drop('Time_01', axis=1, inplace=True)
# erro de espaços vinda de cima
Indicador02 = dados['Inf_2'].str.replace(
    '                                                                    \n\n', '')

divisao1_retirado = Indicador02.str.translate({ord(c): " " for c in ".!_+"})
dados['Indicador_01'] = divisao1_retirado
dados.drop('Inf_2', axis=1, inplace=True)
################################################################################################################
divisao1_placar = dados["Placar"].str.split(" x ")
placar_casa = divisao1_placar.str.get(0)
placar_visitante = divisao1_placar.str.get(1)
dados['placar_casa'] = placar_casa
dados['placar_visitante'] = placar_visitante
dados.drop('Placar', axis=1, inplace=True)


# esses valores estão invertidos ou seja
# Nome; Indicador
# Indicador ; Nome
# não posso separa-los diretamente então vou fazer uma gambiarra
# esses são os valores onde apresentam os nomes
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
a12 = a11.str.replace(' acerta arremesso de três pontos ', '/3_Pts_C;1')
a13 = a12.str.replace(' erra tentativa para três pontos ', '/3_Pts_T;1')
# lance livre
a14 = a13.str.replace(' acerta o lance livre ', '/LL_Pts_C;1')
a15 = a14.str.replace(' erra o lance livre ', '/LL_Pts_T;1')
# Dois pontos
a16 = a15.str.replace(' acerta arremesso de dois pontos ', '/2_Pts_C;1')
a17 = a16.str.replace(' erra tentativa para dois pontos ', '/2_Pts_T;1')
# rebotes
a18 = a17.str.replace(' pega rebote defensivo ', '/RD;1')
a19 = a18.str.replace(' pega rebote ofensivo ', '/RO;1')
# recuperação de bola
a20 = a19.str.replace(' recupera a bola ', '/BR;1')
# assistencia
a21 = a20.str.replace(' Assistência do ', '/AS;')
# faltas recebidas
a22 = a21.str.replace(' sofre falta ', '/FR;1')
# faltas cometidas
a23 = a22.str.replace(' comete falta técnica ', '/FC_T;1')
a24 = a23.str.replace(' comete falta antidesportiva ', '/FC_A;1')
a25 = a24.str.replace(' comete falta ofensiva ', '/FC_O;1')
a26 = a25.str.replace(' comete falta ', '/FC;1')
# substituição
a27 = a26.str.replace('Entra ', '/substituicao_entra;')
a28 = a27.str.replace('Sai ', '/substituicao_sai;')
# erros
a29 = a28.str.replace(' perde posse de bola ', '/ER;1')
a30 = a29.str.replace('Estouro dos 24s ', '/ER;1')
a31 = a30.str.replace(' andou com a bola ', '/ER;1')
a32 = a31.str.replace(' comete violação de saída de quadra ', '/ER;1')
# tocos
a33 = a32.str.replace(' dá um toco ', '/TO;1')
# tempo técnico
a34 = a33.str.replace('Técnico da equipe ', '')
a35 = a34.str.replace(' pede tempo ', '/tempo_tecnico;')
# cravada
a36 = a35.str.replace('Cravada ', '')
a37 = a36.str.replace(' acerta enterrada', '/EN;1')

# primeira separação é coloco na ordem dos nomes e depois indicadores
# o ; é para fazer a primeira separação
# 1 é para conter um valor apenas, pois quando separo e junto, caso não tenha um valor, o resultado retira
# os valores
mudados_00 = a37.str.split(';')
mudados_01 = mudados_00.str.get(1)
mudados_02 = mudados_00.str.get(0)

# outra forma de tirar o (% de algo)
mudados_03 = mudados_01.str.split('(')
mudados_04 = mudados_03.str.get(0)

alinhados = mudados_04 + mudados_02

# agora que juntou e alinhou os nomes
# organizar novamente
alinhados_01 = alinhados.str.split('/')
alinhados_02 = alinhados_01.str.get(0)
alinhados_03 = alinhados_01.str.get(1)

# depois de separado vamos organizar por nomes e retirar os valores que ajudaram na primeira separação,
# como 1 e espaço

alinhados_04 = alinhados_02.str.replace('1 ', '')
alinhados_05 = alinhados_04.str.replace(' 1', '')

dados["Indicador"] = alinhados_03
dados["Nomes"] = alinhados_05
dados.drop('Indicador_01', axis=1, inplace=True)

r1 = requests.get(list_inoutControl[1])
soup01 = BeautifulSoup(r1.content, 'html.parser')
informacoes_1 = soup01.find_all("div", class_="float-left text-right")
informacoes_2 = soup01.find_all("div", class_="float-right text-left")

nome_casa = informacoes_1[0].find("span", class_="show-for-large").get_text()
nome_fora = informacoes_2[0].find("span", class_="show-for-large").get_text()

# acontece erro por conta de nomes com siglas ai eu preciso substituir
nome_casa = nome_casa.replace('/', ' ')
nome_fora = nome_fora.replace('/', ' ')

dados.to_csv("teste_06.csv", index=None)
nome_inf_coluna = nome_casa + "_x_" + nome_fora
print(nome_inf_coluna)
