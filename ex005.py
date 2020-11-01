import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import io


r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos')
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

divisao1 = dados["inf_3"]

divisao1_retirado = divisao1.str.translate({ord(c): " " for c in "!_+"})

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
a42 = a41.str.replace(' recupera a bola', 'BR;')
a43 = a42.str.replace('Erro ', 'ER;')
########################################################################################################################
# alguns que faltaram olhando a tabela 1
a44 = a43.str.replace('Violação ', 'ER;')
a45 = a44.str.replace('TOCO  ', 'TO;')
a46 = a45.str.replace(' dá um toco', '')
a47 = a46.str.replace('FIM DE QUARTO Fim', 'fim_quarto;')
a48 = a47.str.replace(' TEMPO TÉCNICO Técnico da equipe ', 'tempo_tecnico;')
a49 = a48.str.replace(' pede tempo', '')
a50 = a49.str.replace('do quarto quarto', '')
a51 = a50.str.replace('CRAVADA  Cravada ', 'EN;')
a52 = a51.str.replace(' acerta enterrada ', '')
# Deu B.o ai tive que olha novamente a tabela 2 e encontrar o problema
a53 = a52.str.replace('ANTIDESPORTIVA ', 'FC;')
a54 = a53.str.replace(' antidesportiva', '')
# ANTIDESPORTIVA Pastor antidesportiva

# 4,03:08,RCB,94,78,FC,ANTIDESPORTIVA
# D. Nunes comete falta ofensiva
# Técnico da equipe Rio Claro pede tempo.

# adicionar e tirar os dados
dados['mudados'] = a54
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

dados.to_csv("teste_06.csv", index=None)
driver.quit()


# str coloca para identificação de uma string assim não acontece erro na procura
# tem nomes separados JOSE HENRIQUE ai da b.o na separação. Então eu estou identificando isso e juntando os nomes
# tirar_lixo é os dados que estão (.........) aleatorio só é para chamar ter algo para chamar depois no ()
# o for coloquei iii para variavel percorrer no Nome (range do Nome que está em cima)
# ele percorre iii e se algo começar com '(' ele para e coloca NaN
# se não começar com '(' ele para e pega a informação de iii
# e no finla retorna nova_tabela
# no print eu
