import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException
import io
import re
import datetime as dt

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=54&wherePlaying=-1&played=-1')
soup = BeautifulSoup(r.content, 'html.parser')


def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


list_inoutControl = get_links_from(soup)

#######################################################################################################################
temporada = 2019
tabela_geral = pd.DataFrame([])
jj = 1

for j in list_inoutControl:

    ####################################################################################################################

    option = Options()
    option.headless = True
    driver = webdriver.Firefox()
    # options = option

    driver.get(f'{j}')
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
             'Tempo_1': tempo,
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
                                     "Fim  do período de prorragação|Início do  de período de prorragação)", "", x))
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
        c = c.str.replace(' comete falta desqualificante', '/FC_D;1')
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
                                     " comete violação de saída de quadra| comete violação de volta de quadra|"
                                     " comete violação de condução)", "/ER;1", x))
        # cravada
        c = c.str.replace('Cravada', '')
        c = c.str.replace(' acerta enterrada', '/EN;1')

        # falta técnica para treinador
        c = c.str.replace('Técnico do ', '')

        # tirar os parenteses
        c = c.str.replace('(', ';')

        # primeira separação é coloco na ordem dos nomes e depois indicadores
        # o ; é para fazer a primeira separação: obtem os nomes
        # 1 é para conter um valor apenas, pois quando separo e junto, caso não tenha um valor, o resultado retira os valores
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
        alinhados_05 = alinhados_05.str.strip()

        dados["Indicador"] = alinhados_03
        dados["Nome"] = alinhados_05

        dados.drop('Inf_2', axis=1, inplace=True)

        divisao1_placar = dados["Placar"].str.split(" x ")
        placar_casa = divisao1_placar.str.get(0)
        placar_visitante = divisao1_placar.str.get(1)
        dados['placar_casa'] = placar_casa
        dados['placar_visitante'] = placar_visitante
        dados.drop('Placar', axis=1, inplace=True)
        #############################################################################################################
        # descobrir nome do time
        r1 = requests.get(f'{j}')
        soup01 = BeautifulSoup(r1.content, 'html.parser')

        informacoes_1 = soup01.find_all("div", class_="float-left text-right")
        informacoes_2 = soup01.find_all("div", class_="float-right text-left")

        nome_casa_of = informacoes_1[0].find("span", class_="show-for-large").get_text()
        nome_fora_of = informacoes_2[0].find("span", class_="show-for-large").get_text()

        # acontece erro por conta de nomes com siglas ai eu preciso substituir
        nome_casa_of = nome_casa_of.replace('/', ' ')
        nome_fora_of = nome_fora_of.replace('/', ' ')

    else:
        # atribuir os dados do site em html
        html_content = element.get_attribute('outerHTML')
        # passear o conteúdo em HTML e pegar o texto
        soup = BeautifulSoup(html_content, 'html.parser')
        acoes = soup.get_text()

        # realizar a limpeza dos dados obtidos
        c = acoes.replace(' 1º', '\n1')
        c = c.replace(' 2º', '\n2')
        c = c.replace(' 3º', '\n3')
        c = c.replace(' 4º', '\n4')
        c = c.replace(' 5º', '\n5')
        c = c.replace(' 6º', '\n6')
        c = c.replace(' 7º', '\n7')
        c = re.sub('(			 |			 |			 )', ';', c)
        c = c.replace('    ', ';')
        c = c.translate({ord(c): "" for c in ".!_+"})

        # depois de ajustar os espaços eu substititui os indicadores por nomes padronizados
        c = re.sub("(Fim  do quarto quarto|Fim  do terceiro quarto|"
                   "Fim  do segundo quarto|Fim  do primeiro quarto|"
                   "Fim  do período de prorragação)", ";1/fim_quarto;", c)

        c = re.sub("(Início do  quarto quarto|Início do  terceiro quarto|"
                   "Início do  segundo quarto|Início do  de período de prorragação)", ";1/inicio_quarto;", c)

        c = c.replace('Fim de partida', ';1/fim_partida;')
        c = c.replace('Início de partida', ';1/inicio_partida;')

        # esses são os valores que estão os indicadores
        c = c.replace('acerta arremesso de três pontos', '/3_Pts_C;1')
        c = c.replace('erra tentativa para três pontos', '/3_Pts_T;1')
        # lance livre
        c = c.replace('acerta o lance livre', '/LL_Pts_C;1')
        c = c.replace('erra o lance livre', '/LL_Pts_T;1')
        # Dois pontos
        c = c.replace('acerta arremesso de dois pontos', '/2_Pts_C;1')
        c = c.replace('erra tentativa para dois pontos', '/2_Pts_T;1')
        # rebotes
        c = c.replace('pega rebote defensivo', '/RD;1')
        c = c.replace('pega rebote ofensivo', '/RO;1')
        # recuperação de bola
        c = c.replace('recupera a bola', '/BR;1')
        # assistencia
        c = c.replace('Assistência do ', '/AS;')
        # faltas recebidas
        c = c.replace('sofre falta', '/FR;1')

        # faltas cometidas
        c = c.replace('comete falta técnica', '/FC_T;1')
        c = c.replace('comete falta antidesportiva', '/FC_A;1')
        c = c.replace('comete falta ofensiva', '/FC_O;1')
        c = c.replace('comete falta desqualificante', '/FC_D;1')
        c = c.replace('comete falta', '/FC;1')
        # substituição
        c = c.replace('Entra ', '1/substituicao_entra;')
        c = c.replace('Sai ', '1/substituicao_sai;')
        # tocos
        c = c.replace('dá um toco', '/TO;1')
        # tempo técnico
        c = c.replace('pede tempo', '/tempo_tecnico;')
        # erros
        c = re.sub("( perde posse de bola|Estouro dos 24s| andou com a bola|"
                   " comete violação de saída de quadra| comete violação de volta de quadra|  comete violação de condução)",
                   "/ER;1", c)
        # cravada
        c = c.replace('acerta enterrada', '1/EN;1')

        # tirar os parenteses
        c = c.replace(' (', ';')

        # retiradas de informações inúteis
        c = re.sub('(INÍCIO DE QUARTO |FIM DE QUARTO |FIM DE PARTIDA |'
                   'Tentativa para três pontos |É DE TRÊS |1 PONTO |Lance Livre Errado |Tentativa para dois pontos |'
                   '2 PONTOS |REBOTE DEFENSIVO |REBOTE OFENSIVO |Bola recuperada |ASSISTÊNCIA |'
                   'Falta sofrida |FALTA OFENSIVA|FALTA ANTIDESPORTIVA |FALTA TÉCNICA |FALTA DESQUALIFICANTE |FALTA |'
                   'Substituição |Substituição Sai |TOCO |TEMPO TÉCNICO Técnico da equipe |'
                   ' Violação Estouro dos 24s|Violação |Erro |CRAVADA |TEMPO TÉCNICO |É de três |'
                   'Técnico da equipe |Cravada|Técnico do )', '', c)

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
        alinhados_01 = alinhados.str.split('/')
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
        #############################################################################################################
        # descobrir nome do time
        r1 = requests.get(f'{j}')
        soup01 = BeautifulSoup(r1.content, 'html.parser')

        informacoes_1 = soup01.find_all("div", class_="float-left text-right score_header_left")
        informacoes_2 = soup01.find_all("div", class_="float-right text-left score_header_right")

        nome_casa_of = informacoes_1[0].find("span", class_="show-for-large").get_text()
        nome_fora_of = informacoes_2[0].find("span", class_="show-for-large").get_text()

        # acontece erro por conta de nomes com siglas ai eu preciso substituir
        nome_casa_of = nome_casa_of.replace('/', ' ')
        nome_fora_of = nome_fora_of.replace('/', ' ')

    # mudança do tempo
    # colocar todos em segundos para facilitar a vida
    # primeiro evitar NAN (acredite!!! tem isso no site)
    dados.dropna(subset=['Tempo_1'], inplace=True)

    # tem jogos que o site apresenta numeros inteiros (1, 12, 134, 1000)
    # para isso localizei o valores errados e concertei
    mudar_hora = []
    for x in dados['Tempo_1']:
        if re.findall(r'..:..', x):
            mudar_hora.append(x)
        else:
            if re.findall(r'....', x):
                x = x[0:2] + ':' + x[2:4]
                mudar_hora.append(x)
            elif re.findall(r'...', x):
                x = '0' + x[0] + ':' + x[1:3]
                mudar_hora.append(x)
            elif re.findall(r'..', x):
                x = '00:' + x
                mudar_hora.append(x)
            elif re.findall(r'.', x):
                x = '00:0' + x
                mudar_hora.append(x)

    dados['Tempo_2'] = mudar_hora
    dados.drop('Tempo_1', axis=1, inplace=True)

    # transformado tudo em segundo
    dados['Tempo_2'] = dados['Tempo_2'].apply(lambda q: dt.datetime.strptime(q, '%M:%S'))
    dados['Tempo_2'] = dados['Tempo_2'].apply(lambda w: dt.time(w.hour, w.minute, w.second))
    dados['Tempo_2'] = dados['Tempo_2'].apply(lambda e: (e.hour * 60 + e.minute) * 60 + e.second)

    # transforma os dados para números inteiros
    dados['Quarto'] = dados['Quarto'].apply(lambda l: int(l))
    # modificar o tempo decrescente para crescente (* -1)
    # acrescentar o tempo de cada quarto (primeiro quarto termina em 600s, o segundo quarto 2*600 = 1200 ...)
    tempo_novo = []
    for x, y in zip(dados['Quarto'], dados['Tempo_2']):
        if x == 1:
            a = (y - (600 * 1)) * -1
            tempo_novo.append(a)
        elif x == 2:
            a = (y - (600 * 2)) * -1
            tempo_novo.append(a)
        elif x == 3:
            a = (y - (600 * 3)) * -1
            tempo_novo.append(a)
        elif x == 4:
            a = (y - (600 * 4)) * -1
            tempo_novo.append(a)
        elif x == 5:
            a = (y - (600 * 5)) * -1
            tempo_novo.append(a)
        elif x == 6:
            a = (y - (600 * 6)) * -1
            tempo_novo.append(a)
        elif x == 7:
            a = (y - (600 * 7)) * -1
            tempo_novo.append(a)

    dados['Tempo'] = tempo_novo
    dados.drop('Tempo_2', axis=1, inplace=True)

    # deixando o DataFrame nessa ordem de colunas
    dados = dados[['Quarto', 'Tempo', 'placar_casa', 'placar_visitante', 'Time', 'Indicador', 'Nome']]
    dados.to_csv("Dados01/temporada " + f"{temporada}""/" + "tabela_" + f"{jj}" + "_" + nome_casa_of + "_x_" + nome_fora_of + ".csv")
    nome_inf_coluna = nome_casa_of + "_x_" + nome_fora_of
    tabela_geral = pd.concat([dados, tabela_geral], axis=0)
    print(nome_inf_coluna)

    jj += 1
    driver.quit()
