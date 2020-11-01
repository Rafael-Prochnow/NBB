import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import io
import re
import html5lib

'''
lista_de_temporadas = ['https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=54&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=47',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=41&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=34',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=27&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=15',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=8&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=4',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=3&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=2',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=1&wherePlaying=-1&played=-1']
t = 19

for x in lista_de_temporadas:
    r = requests.get(x)
    f'soup{t}' = BeautifulSoup(r.content, 'html.parser')
    t = t-1
'''

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=54&wherePlaying=-1&played=-1')
soup = BeautifulSoup(r.content, 'html.parser')

def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links

list_inoutControl = get_links_from(soup)

#######################################################################################################################
option = Options()
option.headless = True
driver = webdriver.Firefox()
# options=option
driver.get(list_inoutControl[1])
time.sleep(10)


driver.find_element_by_xpath(
    "//div[@class='row tabs_content']//ul//li//a[@id='movethemove-label']").click()


element = driver.find_element_by_xpath("//div[@class='move_action_scroll']")
# move_action_scroll column
html_content = element.get_attribute('outerHTML')

# passear o conteúdo em HTML
soup = BeautifulSoup(html_content, 'html.parser')

acoes = soup.get_text()

acoes = soup.get_text()
b = acoes.replace(' 1º', '\n1')
b = b.replace(' 2º', '\n2')
b = b.replace(' 3º', '\n3')
b = b.replace(' 4º', '\n4')
b = re.sub('(.			 |      |  |    |			 |			 |			)', ';', b)

data = io.StringIO(b)

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
divisao1 = dados["inf_3"]

divisao1_retirado = divisao1.str.translate({ord(c): " " for c in "!_+"})

a = re.sub('(INÍCIO DE QUARTO Início do quarto quarto|INÍCIO DE QUARTO Início do terceiro quarto|'
       'INÍCIO DE QUARTO Início do segundo quarto)', 'inicio_quarto;', str(divisao1_retirado))


'''
a = a.replace('FIM DE PARTIDA Fim de partida', 'fim_partida;')
a = a.replace('INÍCIO DE QUARTO Início de partida', 'inicio_partida;')

a = re.sub('(FIM DE QUARTO Fim do quarto quarto|FIM DE QUARTO Fim do terceiro quarto|'
            'FIM DE QUARTO Fim do segundo quarto|FIM DE QUARTO Fim do primeiro quarto)', 'fim_quarto;', a)
# três pontos

a = a.replace("Tentativa para três pontos ", "3_Pts_T;")
a = a.replace('É DE TRÊS  É de três  ', '3_Pts_C;')
# lance livre
a = a.replace(' 1 PONTO ', 'LL_Pts_C;')
a = a.replace('Lance Livre Errado ', 'LL_Pts_T;')
# dois pontos
a = a.replace('Tentativa para dois pontos ', '2_Pts_T;')
a = a.replace(' 2 PONTOS ', '2_Pts_C;')
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
a = a.replace('TOCO  ', 'TO;')
# tempo técnico
a = a.replace(' TEMPO TÉCNICO Técnico da equipe ', 'tempo_tecnico;')
# Erros
a = re.sub('( Violação Estouro dos 24s|Violação |Erro )', 'ER;', a)
# enterrada
a = a.replace('CRAVADA  Cravada ', 'EN;')
# retiradas de informações inúteis
a = re.sub('( erra tentativa para três pontos| acerta arremesso de três pontos| acerta o lance livre|'
           ' erra tentativa para dois pontos| acerta arremesso de dois pontos| pega rebote ofensivo|'
           ' erra o lance livre| pega rebote defensivo| recupera a bola| sofre falta| comete falta ofensiva|'
           ' antidesportiva| perde posse de bola| comete violação de saída de quadra|nan| dá um toco|'
           ' pede tempo| acerta enterrada | comete falta técnica| comete falta)', '', a)

'''
dados['mudados'] = a
dados.drop('inf_3', axis=1, inplace=True)

'''
separar_01 = dados['mudados'].str.split(";")
Indicador = separar_01.str.get(0)
dados['Indicador'] = Indicador
inf_02 = separar_01.str.get(1)


teste = inf_02.str.translate({ord(c): "," for c in "("})

teste2 = teste.str.split(',')
teste3 = teste2.str.get(0)
dados['Nomes'] = teste3
dados.drop('mudados', axis=1, inplace=True)

'''
dados.to_csv('parte_3.csv')
# fora revisados os dados na primeira planilha. eu sei que está certo uma olhada pq
# os dados apresentam padrão na escrita

# dados.drop('inf_3', axis=1, inplace=True)
