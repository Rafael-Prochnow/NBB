import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import io
import re
import datetime as dt

'''
# Odeio o site da NBB depois de mudar 4 vezes por causa do tipo da tabela 
# eu tenho que mudar novamente pq tem a 5 tipo de tabela

a = a.replace("INÍCIO DE QUARTO Início do", ";inicio_quarto")
a = a.replace("FIM DE QUARTO Fim", ";fim_quarto")

a = re.sub('(do terceiro quarto|terceiro quarto|do segundo quarto|segundo quarto|do primeiro quarto|'
           'quarto quarto)', '', a)

a = a.replace('FIM DE PARTIDA Fim de partida', ';fim_partida;')
a = a.replace('INÍCIO DE QUARTO Início de partida', ';inicio_partida;')

# três pontos
a = a.replace("Tentativa para três pontos ", "3_Pts_T;")
a = a.replace('É DE TRÊS É de três ', '3_Pts_C;')
# lance livre
a = a.replace('1 PONTO ', 'LL_Pts_C;')
a = a.replace('Lance Livre Errado ', 'LL_Pts_T;')
# dois pontos
a = a.replace('Tentativa para dois pontos ', '2_Pts_T;')
a = a.replace('2 PONTOS ', '2_Pts_C;')
# rebotes
a = a.replace('REBOTE DEFENSIVO ', 'RD;')
a = a.replace('REBOTE OFENSIVO ', 'RO;')
# recuperação da bola
a = a.replace('Bola recuperada ', 'BR;')
# assistência
a = a.replace('ASSISTÊNCIA Assistência do ', 'AS;')
# faltas recebidas
a = a.replace('Falta sofrida ', 'FR;')
# faltas cometidas
a = a.replace('FALTA OFENSIVA', 'FC_O;')
a = a.replace('FALTA ANTIDESPORTIVA ', 'FC_A;')
a = a.replace('FALTA TÉCNICA ', 'FC_T;')
a = a.replace('FALTA ', 'FC;')
# substituições
a = a.replace('Substituição Entra ', 'substituicao_entra;')
a = a.replace('Substituição Sai ', 'substituicao_sai;')
# tocos
a = a.replace('TOCO ', 'TO;')
# tempo técnico
a = a.replace('TEMPO TÉCNICO Técnico da equipe ', 'tempo_tecnico;')
# Erros
a = re.sub('( Violação Estouro dos 24s|Violação |Erro )', 'ER;', a)
# enterrada
a = a.replace('CRAVADA Cravada', 'EN;')
# retiradas de informações inúteis
a = re.sub('( erra tentativa para três pontos| acerta arremesso de três pontos| acerta o lance livre|'
           ' erra tentativa para dois pontos| acerta arremesso de dois pontos| pega rebote ofensivo|'
           ' erra o lance livre| pega rebote defensivo| recupera a bola| sofre falta| comete falta ofensiva|'
           ' antidesportiva| perde posse de bola| comete violação de saída de quadra|nan| dá um toco|'
           ' pede tempo| acerta enterrada | comete falta técnica| comete falta|Estouro dos 24s|'
           ' acerta enterrada|Técnico do | andou com a bola| comete violação de volta de quadra|'
           ' comete violação de 5s com a posse de bola)', '', a)

'''

'''
r = requests.get('https://lnb.com.br/ldb/tabela-de-jogos/?season%5B%5D=64&wherePlaying=-1&played=-1')
soup = BeautifulSoup(r.content, 'html.parser')

def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links

list_inoutControl = get_links_from(soup)

list_inoutControl = list_inoutControl[14:16]
print(list_inoutControl)'''

jogo = 'https://lnb.com.br/partidas/ldb-2021-rio-claro-abdc-x-praia-clube-gabarito-30072021-0900/'
#######################################################################################################################
option = Options()
option.headless = True
driver = webdriver.Firefox()
# options=option
driver.get(jogo)
time.sleep(10)


# primeio tipo de tabela
# encontrar a table jogada-jogada no site da NBB
driver.find_element_by_xpath(
    "//div[@class='row tabs_content']//ul//li//a[@id='movethemove-label']").click()
# encontrar elementos do site com os dados das jogadas
element = driver.find_element_by_xpath("//div[@class='move_action_scroll']")
# atribuir os dados do site em html
html_content = element.get_attribute('outerHTML')
# passear o conteúdo em HTML e pegar o texto
soup = BeautifulSoup(html_content, 'html.parser')
acoes = soup.get_text()

def limpeza_tabela_um(acoes):
    lista = [' 1º', ' 2º', ' 3º', ' 4º', ' 5º', ' 6º', ' 7º']
    lista1 = ['\n1', '\n2', '\n3', '\n4', '\n5', '\n6', '\n7']
    for n in range(len(lista)):
        acoes = acoes.replace(lista[n], lista1[n])

    c = re.sub('(			 |			 |			 )', ';', acoes)
    c = c.replace('    ', ';')
    c = c.translate({ord(c): "" for c in ".!_+"})

    c = re.sub("(Fim  do quarto quarto|Fim  do terceiro quarto|"
               "Fim  do segundo quarto|Fim  do primeiro quarto|"
               "Fim  do período de prorragação)", ";1>fim_quarto;", c)

    c = re.sub("(Início do  quarto quarto|Início do  terceiro quarto|"
               "Início do  segundo quarto|Início do  de período de prorragação)", ";1>inicio_quarto;", c)

    lista2 = ['Fim de partida', 'Início de partida', 'acerta arremesso de três pontos',
              'erra tentativa para três pontos',
              'acerta o lance livre', 'erra o lance livre', 'acerta arremesso de dois pontos',
              'erra tentativa para dois pontos', 'pega rebote defensivo', 'pega rebote ofensivo', 'recupera a bola',
              ' recupera posse de bola', 'Assistência do ', 'sofre falta', 'comete falta técnica',
              'comete falta antidesportiva', 'comete falta ofensiva', 'comete falta desqualificante',
              'comete falta', 'Entra ', 'Sai ', 'dá um toco', 'pede tempo', 'acerta enterrada',
              'erra tentativa de enterrada']

    lista3 = [';1>fim_partida;', ';1>inicio_partida;', '>3_Pts_C;1', '>3_Pts_T;1', '>LL_Pts_C;1', '>LL_Pts_T;1',
              '>2_Pts_C;1', '>2_Pts_T;1', '>RD;1', '>RO;1', '>BR;1', '>BR;1', '>AS;', '>FR;1', '>FC_T;1', '>FC_A;1',
              '>FC_O;1', '>FC_D;1', '>FC;1', '1>substituicao_entra;', '1>substituicao_sai;', '>TO;1', '>tempo_tecnico;',
              '1>EN;1', '1>2_Pts_T;1']

    for n in range(len(lista2)):
        c = c.replace(lista2[n], lista3[n])

    # erros
    c = re.sub("( perde posse de bola|Estouro dos 24s| andou com a bola|"
               " comete violação de saída de quadra| comete violação de volta de quadra|"
               " comete violação de condução|  comete violação de 5s com a posse de bola)", ">ER;1", c)

    # tirar os parenteses
    c = c.replace(' (', ';')

    # retiradas de informações inúteis
    c = re.sub('(INÍCIO DE QUARTO |FIM DE QUARTO |FIM DE PARTIDA |'
               'Tentativa para três pontos |É DE TRÊS |1 PONTO |Lance Livre Errado |Tentativa para dois pontos |'
               '2 PONTOS |REBOTE DEFENSIVO |REBOTE OFENSIVO |Bola recuperada |ASSISTÊNCIA |'
               'Falta sofrida |FALTA OFENSIVA|FALTA ANTIDESPORTIVA |FALTA TÉCNICA |FALTA DESQUALIFICANTE |FALTA |'
               'Substituição |Substituição Sai |TOCO |TEMPO TÉCNICO Técnico da equipe |'
               ' Violação Estouro dos 24s|Violação |Erro |CRAVADA |TEMPO TÉCNICO |É de três |'
               'Técnico da equipe |Cravada|Técnico do |Tentativa de Enterrada)', '', c)

    return c

c = limpeza_tabela_um(acoes)

# depois de ajustar os espaços eu substititui os indicadores por nomes padronizados
data = io.StringIO(c)
# depois para DataFrame
dados = pd.read_csv(data, sep=';', index_col=False,
                 usecols=[0, 1, 2, 3], header=None)
dados.columns = ['inf1', 'Time', 'inf2', 'inf3']

separar = dados['inf1'].str.replace('  ', ',')
separar_01 = separar.str.split(',')
separar_02 = separar_01.str.get(0)
separar_03 = separar_01.str.get(1)
separar_04 = separar_01.str.get(2)
dados['Quarto'] = separar_02
dados['Tempo_1'] = separar_03
dados['Placar'] = separar_04
dados.drop('inf1', axis=1, inplace=True)

alinhados = dados['inf2']
alinhados_01 = alinhados.str.split('>')
alinhados_02 = alinhados_01.str.get(0)
alinhados_03 = alinhados_01.str.get(1)
mudado = dados['inf3']
juntar = mudado + alinhados_02
juntar = juntar.str.replace('1', '')
juntar = juntar.str.strip()

dados['Nome'] = juntar
dados['Indicador'] = alinhados_03
dados.drop('inf2', axis=1, inplace=True)
dados.drop('inf3', axis=1, inplace=True)

dados['Time'] = dados['Time'].str.replace(' ', '')

# separando o placar em duas colunas (casa/visitante)
divisao1_placar = dados["Placar"].str.split(" x ")
placar_casa = divisao1_placar.str.get(0)
placar_visitante = divisao1_placar.str.get(1)
dados['placar_casa'] = placar_casa
dados['placar_visitante'] = placar_visitante
dados.drop('Placar', axis=1, inplace=True)

# mudança do tempo
# colocar todos em segundos para facilitar a vida
# primeiro evitar NAN (acredite!!! tem isso no site)
dados.dropna(subset=['Tempo_1'], inplace=True)

dados['Tempo'] = dados['Tempo_1']
dados.drop('Tempo_1', axis=1, inplace=True)

# deixando o DataFrame nessa ordem de colunas
dados = dados[['Quarto', 'Tempo', 'placar_casa', 'placar_visitante', 'Time', 'Indicador', 'Nome']]

########################################################################################################################

r1 = requests.get(jogo)
soup01 = BeautifulSoup(r1.content, 'html.parser')

informacoes_1 = soup01.find_all("div", class_="float-left text-right score_header_left")
informacoes_2 = soup01.find_all("div", class_="float-right text-left score_header_right")

nome_casa_of = informacoes_1[0].find("span", class_="show-for-large").get_text()
nome_fora_of = informacoes_2[0].find("span", class_="show-for-large").get_text()

# acontece erro por conta de nomes com siglas ai eu preciso substituir
nome_casa_of = nome_casa_of.replace('/', ' ')
nome_fora_of = nome_fora_of.replace('/', ' ')

dados.to_csv('Rio Claro_x_Prai Clube.csv')

