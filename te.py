import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import io
import re
import html5lib


r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=34')
soup = BeautifulSoup(r.content, 'html.parser')

def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links

list_inoutControl = get_links_from(soup)
del(list_inoutControl[:254])
print(list_inoutControl)


#######################################################################################################################
option = Options()
option.headless = True
driver = webdriver.Firefox()
# options=option
driver.get(list_inoutControl[1])
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

# realizar a limpeza dos dados obtidos
a = acoes.replace(' 1º', '\n1')
a = a.replace(' 2º', '\n2')
a = a.replace(' 3º', '\n3')
a = a.replace(' 4º', '\n4')
# precisa separar espaços criados no html e utilizar ; para juntar
a = re.sub('(			 |			 |			 )', ';', a)
a = a.replace('    ', ';')
# alguns nomes não são colocados por causa do scouter, ai causa uma lacuna. Para resolver fiz isso
a = a.replace('  ', ';')
a = a.replace(';;', ';')

a = a.translate({ord(c): "" for c in ".!_+"})

# depois de ajustar os espaços eu substititui os indicadores por nomes padronizados

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

# convertendo em um StringIO
data = io.StringIO(a)
# depois para DataFrame
dados = pd.read_csv(data, sep=';', index_col=False,
                 usecols=[0, 1, 2, 3, 4, 5], header=None)
dados.columns = ['Quarto', 'Tempo', 'Placar', 'Time', 'Indicador', 'Nome']

# separando o placar em duas colunas (casa/visitante)
divisao1_placar = dados["Placar"].str.split(" x ")
placar_casa = divisao1_placar.str.get(0)
placar_visitante = divisao1_placar.str.get(1)
dados['placar_casa'] = placar_casa
dados['placar_visitante'] = placar_visitante
dados.drop('Placar', axis=1, inplace=True)
# deixando o DataFrame nessa ordem de colunas
dados = dados[['Quarto', 'Tempo', 'placar_casa', 'placar_visitante', 'Time', 'Indicador', 'Nome']]

r1 = requests.get(list_inoutControl[1])
soup01 = BeautifulSoup(r1.content, 'html.parser')

informacoes_1 = soup01.find_all("div", class_="float-left text-right score_header_left")
informacoes_2 = soup01.find_all("div", class_="float-right text-left score_header_right")

nome_casa_of = informacoes_1[0].find("span", class_="show-for-large").get_text()
nome_fora_of = informacoes_2[0].find("span", class_="show-for-large").get_text()

# acontece erro por conta de nomes com siglas ai eu preciso substituir
nome_casa_of = nome_casa_of.replace('/', ' ')
nome_fora_of = nome_fora_of.replace('/', ' ')

# realizar algumas modificações para as análises
dados.to_csv('parte_3.csv')
