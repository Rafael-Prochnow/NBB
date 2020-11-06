import requests
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# teste
r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=54&wherePlaying=-1&played=-1')
soup = BeautifulSoup(r.content, 'html.parser')


def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


list_inoutControl = get_links_from(soup)
del(list_inoutControl[:40])

########################################################################################################################
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

r1 = requests.get(list_inoutControl[1])
soup01 = BeautifulSoup(r1.content, 'html.parser')

informacoes_1 = soup01.find_all("div", class_="float-left text-right")
informacoes_2 = soup01.find_all("div", class_="float-right text-left")

nome_casa = informacoes_1[0].find("span", class_="show-for-large").get_text()
nome_fora = informacoes_2[0].find("span", class_="show-for-large").get_text()

# acontece erro por conta de nomes com siglas ai eu preciso substituir
nome_casa = nome_casa.replace('/', ' ')
nome_fora = nome_fora.replace('/', ' ')

dados = pd.DataFrame(
    {'Quarto': quarto,
     'Tempo': tempo,
     'Time_01': time_site,
     'Placar': placar,
     'Inf_2': acao_pessoa02
     })


# erro de espaços vindo de cima
Indicador02 = dados['Time_01'].str.replace(
            '                                                                    \n\n', '')

Indicador03 = dados['Inf_2'].str.replace(
            '                                                                    \n\n', '')

# esses valores estão invertidos ou seja
# Nome; Indicador
# Indicador ; Nome
# não posso separa-los diretamente então vou fazer uma gambiarra
# esses são os valores onde apresentam os nomes
b = Indicador02.apply(lambda x: re.sub("(Fim de partida.|Fim  do quarto quarto.|Início do  quarto quarto.|"
                                       "Fim  do terceiro quarto.|Início do  terceiro quarto.|Fim  do segundo quarto.|"
                                       "Início do  segundo quarto.|Fim  do primeiro quarto.|Início de partida.|"
                                       "Fim  do período de prorragação.|Início do  de período de prorragação.)", "", x))
dados['Time'] = b
dados.drop('Time_01', axis=1, inplace=True)

a = Indicador03.apply(lambda x: re.sub("(Fim  do quarto quarto.|Fim  do terceiro quarto.|"
                                       "Fim  do segundo quarto.|Fim  do primeiro quarto.|"
                                       "Fim  do período de prorragação.)", "1/fim_quarto;", x))

a = a.apply(lambda x: re.sub("(Início do  quarto quarto.|Início do  terceiro quarto.|"
                             "Início do  segundo quarto.|Início do  de período de prorragação.)"
                             , "1/inicio_quarto;", x))

a = a.str.replace('Fim de partida.', '1/fim_partida;')
a = a.str.replace('Início de partida.', '1/inicio_partida;')

# dados["Nome"] = a
# dados.drop('Inf_2', axis=1, inplace=True)

# esses são os valores que estão os indicadores
a = a.str.replace('É de três! ', '')
a = a.str.replace(' acerta arremesso de três pontos.', '/3_Pts_C;1')
a = a.str.replace(' erra tentativa para três pontos.', '/3_Pts_T;1')
# lance livre
a = a.str.replace(' acerta o lance livre.', '/LL_Pts_C;1')
a = a.str.replace(' erra o lance livre.', '/LL_Pts_T;1')
# Dois pontos
a = a.str.replace(' acerta arremesso de dois pontos.', '/2_Pts_C;1')
a = a.str.replace(' erra tentativa para dois pontos.', '/2_Pts_T;1')
# rebotes
a = a.str.replace(' pega rebote defensivo.', '/RD;1')
a = a.str.replace(' pega rebote ofensivo.', '/RO;1')
# recuperação de bola
a = a.str.replace(' recupera a bola.', '/BR;1')
# assistencia
a = a.str.replace('Assistência do ', '/AS;')
# faltas recebidas
a = a.str.replace(' sofre falta.', '/FR;1')
# faltas cometidas
a = a.str.replace(' comete falta técnica.', '/FC_T;1')
a = a.str.replace(' comete falta antidesportiva.', '/FC_A;1')
a = a.str.replace(' comete falta ofensiva.', '/FC_O;1')
a = a.str.replace(' comete falta.', '/FC;1')
# substituição
a = a.str.replace('Entra ', '/substituicao_entra;')
a = a.str.replace('Sai ', '/substituicao_sai;')
# tocos
a = a.str.replace(' dá um toco.', '/TO;1')
# tempo técnico
a = a.str.replace('Técnico da equipe ', '')
a = a.str.replace(' pede tempo.', '/tempo_tecnico;')
# erros
a = a.apply(lambda x: re.sub("( perde posse de bola.|Estouro dos 24s.| andou com a bola.|"
                             " comete violação de saída de quadra.| comete violação de volta de quadra.)", "/ER;1", x))
# cravada
a = a.str.replace('Cravada ', '')
a = a.str.replace(' acerta enterrada.', '/EN;1')

divisao1_placar = dados["Placar"].str.split(" x ")
placar_casa = divisao1_placar.str.get(0)
placar_visitante = divisao1_placar.str.get(1)
dados['placar_casa'] = placar_casa
dados['placar_visitante'] = placar_visitante
dados.drop('Placar', axis=1, inplace=True)

# primeira separação é coloco na ordem dos nomes e depois indicadores
# o ; é para fazer a primeira separação: obtem os nomes
# 1 é para conter um valor apenas, pois quando separo e junto, caso não tenha um valor, o resultado retira os valores
mudados_00 = a.str.split(';')
mudados_01 = mudados_00.str.get(1)
mudados_02 = mudados_00.str.get(0)

alinhados = mudados_01 + mudados_02
# agora que juntou e alinhou os nomes
# organizar novamente
alinhados_01 = alinhados.str.split('/')
alinhados_02 = alinhados_01.str.get(0)
alinhados_03 = alinhados_01.str.get(1)

# depois de separado vamos organizar por nomes e retirar os valores que ajudaram na primeira separação,
# como 1 e espaço
alinhados_04 = alinhados_02.str.replace('1 ', '')
alinhados_05 = alinhados_04.str.replace('1', '')

dados["Indicador"] = alinhados_03
dados["Nome"] = alinhados_05
dados.drop('Inf_2', axis=1, inplace=True)
dados = dados[['Quarto', 'Tempo', 'placar_casa', 'placar_visitante', 'Time', 'Indicador', 'Nome']]

# se ER não tiver ninguém é pq foi estouro de 24s
dados.to_csv('parte_3.csv')

