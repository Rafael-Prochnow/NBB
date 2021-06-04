from bs4 import BeautifulSoup
import pandas as pd
import requests
import io
import re
from selenium.common.exceptions import NoSuchElementException


def arquivos_acao_df():
    tabela_geral_acao = pd.DataFrame([])
    lista_cada_temporada_acao = pd.DataFrame([])
    l1_acao = pd.DataFrame([])
    l2_acao = pd.DataFrame([])
    return tabela_geral_acao, lista_cada_temporada_acao, l1_acao, l2_acao


def arquivos_acao_lista():
    lista_funcionando_acao = []
    lista_falha_acao = []
    list_sites_falha_acao = []
    list_sites_funciona_acao = []
    return lista_funcionando_acao, lista_falha_acao, list_sites_falha_acao, list_sites_funciona_acao


def verificacao_nomes(nome_time):
    if nome_time == 'L. Sorocabana':
        nome_time = 'Liga Sorocabana'
        return nome_time

    elif nome_time == 'Mogi':
        nome_time = 'Mogi das Cruzes'
        return nome_time

    elif nome_time == 'Fortaleza B. C.':
        nome_time = 'Fortaleza Basquete'
        return nome_time
    elif nome_time == 'BRB Brasília':
        nome_time = 'Brasília'
        return nome_time


def get_links_from(teste):
    links = []
    for a in teste.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


def tabela_tipo_1(i, element):
    # Tabela tipo um apresenta uma estrutura de dados em que os times apresentam abas um do lado do outro
    # atribuir os dados do site em html
    html_content = element.get_attribute('outerHTML')
    # passear o conteúdo em HTML e pegar o texto
    soup = BeautifulSoup(html_content, 'html.parser')
    acoes = soup.get_text()

    # realizar a limpeza dos dados obtidos
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
               " comete violação de condução)", ">ER;1", c)

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
    dados['Tempo'] = separar_03
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
    dados = dados[['Quarto', 'Tempo', 'placar_casa', 'placar_visitante', 'Time', 'Indicador', 'Nome']]
    ####################################################################################################
    # descobrir nome do time
    r1 = requests.get(f'{i}')
    soup01 = BeautifulSoup(r1.content, 'html.parser')

    informacoes_1 = soup01.find_all("div", class_="float-left text-right score_header_left")
    informacoes_2 = soup01.find_all("div", class_="float-right text-left score_header_right")

    nome_casa_of = informacoes_1[0].find("span", class_="show-for-large").get_text()
    nome_fora_of = informacoes_2[0].find("span", class_="show-for-large").get_text()

    # acontece erro por conta de nomes com siglas ai eu preciso substituir
    nome_casa_of = nome_casa_of.replace('/', ' ')
    nome_casa_of = verificacao_nomes(nome_casa_of)
    nome_fora_of = nome_fora_of.replace('/', ' ')
    nome_fora_of = verificacao_nomes(nome_fora_of)

    return dados, nome_casa_of, nome_fora_of


def tabela_tipo_2(i, element):
    # Tabela tipo dois apresenta uma estrutura de dados em que os times estão em sequência (Tabela 1 em cima da 2)
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
    acao_pessoa02 = [nome_acao_pessoa02.find("p", class_='').get_text() for nome_acao_pessoa02 in
                     items01]

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
                                 "Fim  do período de prorragação)", "1>fim_quarto;", x))

    c = c.apply(lambda x: re.sub("(Início do  quarto quarto|Início do  terceiro quarto|"
                                 "Início do  segundo quarto|Início do  de período de prorragação)"
                                 , "1>inicio_quarto;", x))

    c = c.apply(lambda x: re.sub("(Fim  do quarto quarto|Fim  do terceiro quarto|"
                                 "Fim  do segundo quarto|Fim  do primeiro quarto|"
                                 "Fim  do período de prorragação)", "1>fim_quarto;", x))

    c = c.apply(lambda x: re.sub("(Início do  quarto quarto|Início do  terceiro quarto|"
                                 "Início do  segundo quarto|Início do  de período de prorragação)"
                                 , "1>inicio_quarto;", x))

    lista_dois = ['Fim de partida', 'Início de partida', 'É de três ', ' acerta arremesso de três pontos',
                  ' erra tentativa para três pontos', ' acerta o lance livre', ' erra o lance livre',
                  ' acerta arremesso de dois pontos', ' erra tentativa para dois pontos', ' pega rebote defensivo',
                  ' pega rebote ofensivo', ' recupera a bola', ' recupera posse de bola', 'Assistência do ',
                  ' sofre falta', ' comete falta técnica', ' comete falta antidesportiva', ' comete falta ofensiva',
                  ' comete falta desqualificante', ' comete falta', 'Entra ', 'Sai ', ' dá um toco',
                  'Técnico da equipe ',
                  ' pede tempo', 'Cravada', ' acerta enterrada', ' erra tentativa de enterrada', 'Técnico do ', '(']

    lista_dois_ver = ['1>fim_partida;', '1>inicio_partida;', '', '>3_Pts_C;1', '>3_Pts_T;1', '>LL_Pts_C;1',
                      '>LL_Pts_T;1',
                      '>2_Pts_C;1', '>2_Pts_T;1', '>RD;1', '>RO;1', '>BR;1', '>BR;1', '>AS;', '>FR;1', '>FC_T;1',
                      '>FC_A;1', '>FC_O;1', '>FC_D;1', '>FC;1', '>substituicao_entra;', '>substituicao_sai;', '>TO;1',
                      '', '>tempo_tecnico;', '', '>EN;1', '>2_Pts_T;1', '', ';']

    for n in range(len(lista_dois)):
        c = c.str.replace(lista_dois[n], lista_dois_ver[n])

    # erros
    c = c.apply(lambda x: re.sub("( perde posse de bola|Estouro dos 24s| andou com a bola|"
                                 " comete violação de saída de quadra| comete violação de volta de quadra|"
                                 " comete violação de condução| comete violação de 3s no garrafão)", ">ER;1", x))

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
    alinhados_01 = alinhados.str.split('>')
    alinhados_02 = alinhados_01.str.get(0)
    alinhados_03 = alinhados_01.str.get(1)

    # depois de separado vamos organizar por nomes e retirar os valores que ajudaram na separação,
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
    dados = dados[['Quarto', 'Tempo', 'placar_casa', 'placar_visitante', 'Time', 'Indicador', 'Nome']]
    ####################################################################################################
    # descobrir nome do time
    r1 = requests.get(f'{i}')
    soup01 = BeautifulSoup(r1.content, 'html.parser')
    informacoes_1 = soup01.find_all("div", class_="float-left text-right")
    informacoes_2 = soup01.find_all("div", class_="float-right text-left")
    nome_casa_of = informacoes_1[0].find("span", class_="show-for-large").get_text()
    nome_fora_of = informacoes_2[0].find("span", class_="show-for-large").get_text()

    # acontece erro por conta de nomes com siglas ai eu preciso substituir
    nome_casa_of = nome_casa_of.replace('/', ' ')
    nome_casa_of = verificacao_nomes(nome_casa_of)
    nome_fora_of = nome_fora_of.replace('/', ' ')
    nome_fora_of = verificacao_nomes(nome_fora_of)

    return dados, nome_casa_of, nome_fora_of


def salvar_dados_acao(tabela_geral, lista_cada_temporada, temporada, lista_funcionando, l1, l2, lista_falha):
    # retorna uma tabela geral de cada temporada
    lista_cada_temporada = pd.concat([tabela_geral, lista_cada_temporada], axis=0)
    tabela_geral.to_csv('Dados01/temporada ' + f'{temporada}' + '/Total_de_acao_acao_' + f'{temporada}' + '.csv')
    # retorna os sites que funcionam de cada temoporada
    list_sites_funciona = pd.DataFrame(lista_funcionando)
    list_sites_funciona.to_csv('Dados01/temporada ' + f'{temporada}' + '/funcionando_' + f'{temporada}' + '.csv')
    l1 = pd.concat([list_sites_funciona, l1], axis=0)
    # retorna os sites que NÃO funcionam de cada temoporada
    list_sites_falha = pd.DataFrame(lista_falha)
    list_sites_falha.to_csv('Dados01/temporada ' + f'{temporada}' + '/falha_' + f'{temporada}' + '.csv')
    l2 = pd.concat([list_sites_falha, l2], axis=0)
    # zera informações das temporadas
    return l1, l2, lista_cada_temporada


def localizar_acao(driver, i, temporada, numero_jogo, tabela_geral_acao):
    driver.find_element_by_xpath(
        "//div[@class='row tabs_content']//ul//li//a[@id='movethemove-label']").click()
    try:
        element = driver.find_element_by_xpath("//div[@class='move_action_scroll']")
    except NoSuchElementException:
        element = driver.find_element_by_xpath("//div[@class='move_action_scroll column']")
        dados, nome_casa_of, nome_fora_of = tabela_tipo_2(i, element)
    else:
        dados, nome_casa_of, nome_fora_of = tabela_tipo_1(i, element)

    dados.to_csv(
        "Dados01/temporada " + f"{temporada}""/" + "tabela_" + f"{numero_jogo}" + "_" + nome_casa_of + "_x_" + nome_fora_of + ".csv")
    nome_inf_coluna = nome_casa_of + "_x_" + nome_fora_of
    print(nome_inf_coluna)
    tabela_geral = pd.concat([dados, tabela_geral_acao], axis=0)

    return tabela_geral

