import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException
import io
import re

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=41&wherePlaying=-1&played=-1')
soup = BeautifulSoup(r.content, 'html.parser')


def get_links_from(teste):
    links = []
    for a in teste.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links

#
#

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
                       
'''

lista_de_temporadas = ['https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=41&wherePlaying=-1&played=-1',
                       'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=34']


lista_funcionando = []
lista_falha = []
list_sites_funciona = []
list_sites_falha = []
temporada = 2019
tabela_geral = pd.DataFrame([])

for x in lista_de_temporadas:
    print(f'Temporada {temporada}')
    r = requests.get(x)
    soup = BeautifulSoup(r.content, 'html.parser')
    list_inoutControl = get_links_from(soup)
    del(list_inoutControl[:251])

    numero_jogo = 1
    for i in list_inoutControl:
        pagina = requests.get(f'{i}')
        erro_na_pagina = BeautifulSoup(pagina.content, 'html.parser')
        if not erro_na_pagina.find_all("b"):
            print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
            lista_falha.append(i)
            numero_jogo += 1
        else:
            erro_na_pagina01 = erro_na_pagina.find_all("b")
            erro_na_pagina02 = erro_na_pagina01[0].get_text()
            # por motivos de erro da página coloquei isso
            if i == 'https://lnb.com.br/partidas/nbb-20162017-paulistano-x-caxias-do-sul-20122016-1930/':
                print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
                lista_falha.append(i)
                numero_jogo += 1
            elif erro_na_pagina02 != 'Fatal error':
                print(f'Jogo {numero_jogo}')
                lista_funcionando.append(i)
########################################################################################################################
                # pegar o nome dos times
                r1 = requests.get(f'{i}')
                soup01 = BeautifulSoup(r1.content, 'html.parser')

                option = Options()
                option.headless = True
                driver = webdriver.Firefox()
                # options = option

                driver.get(f'{i}')
                time.sleep(10)

                driver.find_element_by_xpath(
                    "//div[@class='row tabs_content']//ul//li//a[@id='movethemove-label']").click()

                try:
                    element = driver.find_element_by_xpath("//div[@class='move_action_scroll']")
                except NoSuchElementException:
                    element = driver.find_element_by_xpath("//div[@class='move_action_scroll column']")
                    html_content = element.get_attribute('outerHTML')

                    # passear o conteúdo em HTML
                    soup = BeautifulSoup(html_content, 'html.parser')
                    # 3 encontra o time, está separado dos demais
                    items02 = soup.find_all(
                        class_='large-10 small-8 medium-10 columns move_action_content move_action_content_one')
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
                    Indicador02 = dados['Time_01'].str.replace(
                        '                                                                    \n\n', '')

                    Indicador03 = dados['Inf_2'].str.replace(
                        '                                                                    \n\n', '')

                    # esses valores estão invertidos ou seja
                    # Nome; Indicador
                    # Indicador ; Nome
                    # não posso separa-los diretamente então vou fazer uma gambiarra
                    # esses são os valores onde apresentam os nomes
                    b = Indicador02.str.translate({ord(c): "" for c in ".!_+"})

                    b = b.apply(lambda x: re.sub("(Fim de partida|Fim  do quarto quarto|Início do  quarto quarto|"
                                                 "Fim  do terceiro quarto|Início do  terceiro quarto|Fim  do segundo quarto|"
                                                 "Início do  segundo quarto|Fim  do primeiro quarto|Início de partida|"
                                                 "Fim  do período de prorragação|Início do  de período de prorragação)",
                                                 "", x))
                    dados['Time'] = b
                    dados.drop('Time_01', axis=1, inplace=True)
                    c = Indicador03.str.translate({ord(c): "" for c in ".!_+"})

                    c = c.apply(lambda x: re.sub("(Fim  do quarto quarto|Fim  do terceiro quarto|"
                                                 "Fim  do segundo quarto|Fim  do primeiro quarto|"
                                                 "Fim  do período de prorragação)", "1/fim_quarto;", x))

                    c = c.apply(lambda x: re.sub("(Início do  quarto quarto|Início do  terceiro quarto|"
                                                 "Início do  segundo quarto|Início do  de período de prorragação)"
                                                 , "1/inicio_quarto;", x))

                    c = c.str.replace('Fim de partida', '1/fim_partida;')
                    c = c.str.replace('Início de partida', '1/inicio_partida;')
                    # esses são os valores que estão os indicadores
                    c = c.str.replace('É de três ', '')
                    c = c.str.replace(' acerta arremesso de três pontos', '/3_Pts_C;1')
                    c = c.str.replace(' erra tentativa para três pontos', '/3_Pts_T;1')
                    # lance livre
                    c = c.str.replace(' acerta o lance livre', '/LL_Pts_C;1')
                    c = c.str.replace(' erra o lance livre', '/LL_Pts_T;1')
                    # Dois pontos
                    c = c.str.replace(' acerta arremesso de dois pontos', '/2_Pts_C;1')
                    c = c.str.replace(' erra tentativa para dois pontos', '/2_Pts_T;1')
                    # rebotes
                    c = c.str.replace(' pega rebote defensivo', '/RD;1')
                    c = c.str.replace(' pega rebote ofensivo', '/RO;1')
                    # recuperação de bola
                    c = c.str.replace(' recupera a bola', '/BR;1')
                    # assistencia
                    c = c.str.replace('Assistência do ', '/AS;')
                    # faltas recebidas
                    c = c.str.replace(' sofre falta', '/FR;1')
                    # faltas cometidas
                    c = c.str.replace(' comete falta técnica', '/FC_T;1')
                    c = c.str.replace(' comete falta antidesportiva', '/FC_A;1')
                    c = c.str.replace(' comete falta ofensiva', '/FC_O;1')
                    c = c.str.replace(' comete falta', '/FC;1')
                    # substituição
                    c = c.str.replace('Entra ', '/substituicao_entra;')
                    c = c.str.replace('Sai ', '/substituicao_sai;')
                    # tocos
                    c = c.str.replace(' dá um toco', '/TO;1')
                    # tempo técnico
                    c = c.str.replace('Técnico da equipe ', '')
                    c = c.str.replace(' pede tempo', '/tempo_tecnico;')
                    # erros
                    c = c.apply(lambda x: re.sub("( perde posse de bola|Estouro dos 24s| andou com a bola|"
                                                 " comete violação de saída de quadra| comete violação de volta de quadra)",
                                                 "/ER;1", x))
                    # cravada
                    c = c.str.replace('Cravada', '')
                    c = c.str.replace(' acerta enterrada', '/EN;1')

                    # falta técnica para treinador
                    c = c.str.replace('Técnico do ', '')

                    divisao1_placar = dados["Placar"].str.split(" x ")
                    placar_casa = divisao1_placar.str.get(0)
                    placar_visitante = divisao1_placar.str.get(1)
                    dados['placar_casa'] = placar_casa
                    dados['placar_visitante'] = placar_visitante
                    dados.drop('Placar', axis=1, inplace=True)

                    # primeira separação é coloco na ordem dos nomes e depois indicadores
                    # o ; é para fazer a primeira separação: obtem os nomes
                    # 1 é para conter um valor apenas, pois quando separo e junto, caso não tenha um valor,
                    # o resultado retira os valores
                    mudados_00 = c.str.split(';')
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
                    informacoes_1 = soup01.find_all("div", class_="float-left text-right")
                    informacoes_2 = soup01.find_all("div", class_="float-right text-left")

                    nome_casa_of = informacoes_1[0].find("span", class_="show-for-large").get_text()
                    nome_fora_of = informacoes_2[0].find("span", class_="show-for-large").get_text()

                    # acontece erro por conta de nomes com siglas ai eu preciso substituir
                    nome_casa_of = nome_casa_of.replace('/', ' ')
                    nome_fora_of = nome_fora_of.replace('/', ' ')

                else:
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

                    a = re.sub(
                        '(do terceiro quarto|terceiro quarto|do segundo quarto|segundo quarto|do primeiro quarto|'
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
                    a = re.sub(
                        '( erra tentativa para três pontos| acerta arremesso de três pontos| acerta o lance livre|'
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

                    informacoes_1 = soup01.find_all("div", class_="float-left text-right score_header_left")
                    informacoes_2 = soup01.find_all("div", class_="float-right text-left score_header_right")

                    nome_casa_of = informacoes_1[0].find("span", class_="show-for-large").get_text()
                    nome_fora_of = informacoes_2[0].find("span", class_="show-for-large").get_text()

                    # acontece erro por conta de nomes com siglas ai eu preciso substituir
                    nome_casa_of = nome_casa_of.replace('/', ' ')
                    nome_fora_of = nome_fora_of.replace('/', ' ')

                dados.to_csv(
                    "Dados01/temporada " + f"{temporada}""/" + "tabela_" + f"{numero_jogo}" + "_" + nome_casa_of + "_x_" + nome_fora_of + ".csv")
                nome_inf_coluna = nome_casa_of + "_x_" + nome_fora_of
                tabela_geral = pd.concat([dados, tabela_geral], axis=0)
                print(nome_inf_coluna)
                driver.quit()
                numero_jogo += 1
########################################################################################################################
            elif erro_na_pagina02 == 'Fatal error':
                print(f'Essa página {i} não está funcionando')
                lista_falha.append(i)
                numero_jogo += 1
    temporada -= 1
    tabela_geral.to_csv('Dados01/Total_de_acao_acao.csv')
    list_sites_funciona = pd.DataFrame(lista_funcionando)
    list_sites_falha = pd.DataFrame(lista_falha)


print(list_sites_funciona)
print(len(list_sites_funciona))
print(list_sites_falha)
print(len(list_sites_falha))
list_sites_funciona.to_csv('Dados01/funcionado.csv')
list_sites_falha.to_csv('Dados01/falha.csv')
