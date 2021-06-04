import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException


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


def arquivos_tabela_df():
    tabela_geral_tabela = pd.DataFrame([])
    lista_cada_temporada_tabela = pd.DataFrame([])
    l1 = pd.DataFrame([])
    l2 = pd.DataFrame([])
    return tabela_geral_tabela, lista_cada_temporada_tabela, l1, l2


def arquivos_tabela_lista():
    lista_funcionando = []
    lista_falha = []
    list_sites_falha = []
    list_sites_funciona = []
    return lista_funcionando, lista_falha, list_sites_falha, list_sites_funciona


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
    else:
        pass


def tipo_2_tabela(element, driver, i, temporada, Data, Fase, Campeonato):
    html_content = element.get_attribute('outerHTML')
    driver.find_element_by_xpath(
        "//a[@id='team_away_stats-label']").click()
    element_2 = driver.find_element_by_xpath(
        "//table[@class='team_two_table tablesorter tablesorter-default']")
    html_content_2 = element_2.get_attribute('outerHTML')
    # passear o conteúdo em HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')
    soup_2 = BeautifulSoup(html_content_2, 'html.parser')
    table_2 = soup_2.find(name='table')
    r1 = requests.get(f'{i}')
    soup01 = BeautifulSoup(r1.content, 'html.parser')
    informacoes_1 = soup01.find_all("div", class_="float-left text-right")
    informacoes_2 = soup01.find_all("div", class_="float-right text-left")
    nome_casa = informacoes_1[0].find("span", class_="show-for-large").get_text()
    nome_fora = informacoes_2[0].find("span", class_="show-for-large").get_text()
    # acontece erro por conta de nomes com siglas ai eu preciso substituir
    nome_casa = nome_casa.replace('/', ' ')
    # nome_casa = verificacao_nomes(nome_casa)
    nome_fora = nome_fora.replace('/', ' ')
    # nome_fora = verificacao_nomes(nome_fora)
    ###############################################################################################
    time_casa = pd.read_html(str(table))[0]
    linhas = len(time_casa)
    tamanho_casa = [nome_casa for item in range(linhas)]
    tamanho_casa_adversario = [nome_fora for item01 in range(linhas)]
    tamanho01_casa = ['casa' for item02 in range(linhas)]
    ano_casa = [temporada for item03 in range(linhas)]
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
    time_casa['Min'] = time_casa['Min'].astype(str)
    time_casa['Min'] = time_casa['Min'].str.replace(':', '.')
    time_casa['Min'] = time_casa['Min'].astype(float)
    soma1 = round(time_casa['Min'].sum(), 0)
    time_casa.loc[(time_casa['Jogador'] == 'Equipe') | (time_casa['Jogador'] == 'Total'), 'Min'] = soma1
    time_fora = pd.read_html(str(table_2))[0]
    linhas_fora = len(time_fora)
    tamanho_fora = [nome_fora for itens in range(linhas_fora)]
    tamanho01_fora = ['fora' for itens01 in range(linhas_fora)]
    ano_fora = [temporada for itens02 in range(linhas_fora)]
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
    time_fora['Min'] = time_fora['Min'].astype(str)
    time_fora['Min'] = time_fora['Min'].str.replace(':', '.')
    time_fora['Min'] = time_fora['Min'].astype(float)
    soma2 = round(time_fora['Min'].sum(), 0)
    time_fora.loc[(time_fora['Jogador'] == 'Equipe') | (time_fora['Jogador'] == 'Total'), 'Min'] = soma2
    #########################################################################################
    df_full = pd.concat([time_casa, time_fora], axis=0)
    # df_full.drop(index=df_full[df_full['Jogador'] == 'Ações coletivas'].index, inplace=True)
    df_full.drop('JO', axis=1, inplace=True)
    df_full.drop('+/-', axis=1, inplace=True)
    df_full.drop('EF', axis=1, inplace=True)

    # precisa colocar tirar a marcação (T) pois atapalha os nomes e não tem em todas as tabelas
    nome_com_T = df_full['Jogador'].str.translate({ord(c): "," for c in "()"})
    nome_sem_T = nome_com_T.str.replace(' ,T,', '')
    df_full['Jogador'] = nome_sem_T

    # substituir os nomes de Equipes e Total. Deixar padrão.
    df_full['Jogador'] = df_full['Jogador'].str.replace('Total', 'Equipe')
    # substitui os valores nulos por 0
    # df_full.fillna(0, inplace=True)

    ################################################################################################
    # divisão 1 separa da porcentagem
    divisao1 = df_full["Pts"].str.split(" ")
    # separar os convertidos e tentados
    divisao = df_full["Pts"].str.split("/")
    # resultado dos convertidos
    Pts_C = divisao.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo
    # eu separei ele e o resultado separei
    Pts_T1 = divisao.str.get(1)
    divisao3 = Pts_T1.str.split(" ")
    # resultado da separação
    Pts_T = divisao3.str.get(0)
    # add nos dados
    df_full["Pts_C"] = Pts_C
    df_full["Pts_T"] = Pts_T

    # tirei a coluna "Pts C/T %"
    df_full.drop('Pts', axis=1, inplace=True)
    ##############################################################################################
    # divisão 1 separa da porcentagem
    divisao1_3 = df_full["3P%"].str.split(" ")
    # separar os convertidos e tentados
    divisao_3 = df_full["3P%"].str.split("/")
    # resultado dos convertidos
    Pts_C_3 = divisao_3.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo
    # eu separei ele e o resultado separei
    Pts_T1_3 = divisao_3.str.get(1)
    divisao3_3 = Pts_T1_3.str.split(" ")
    # resultado da separação
    Pts_T_3 = divisao3_3.str.get(0)
    # add nos dados
    df_full["Pts_3_C"] = Pts_C_3
    df_full["Pts_3_T"] = Pts_T_3
    # tirei a coluna "Pts C/T %"
    df_full.drop('3P%', axis=1, inplace=True)
    #############################################################################################
    # 2 PONTOS
    # divisão 1 separa da porcentagem
    divisao1_2 = df_full["2P%"].str.split(" ")
    # separar os convertidos e tentados
    divisao_2 = df_full["2P%"].str.split("/")
    # resultado dos convertidos
    Pts_C_2 = divisao_2.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo
    # eu separei ele e o resultado separei
    Pts_T1_2 = divisao_2.str.get(1)
    divisao3_2 = Pts_T1_2.str.split(" ")
    # resultado da separação
    Pts_T_2 = divisao3_2.str.get(0)
    # add nos dados
    df_full["Pts_2_C"] = Pts_C_2
    df_full["Pts_2_T"] = Pts_T_2
    # tirei a coluna "Pts C/T %"
    df_full.drop('2P%', axis=1, inplace=True)
    ############################################################################################
    # LANCE LIVRE
    # divisão 1 separa da porcentagem
    divisao1_LL = df_full["LL%"].str.split(" ")
    # separar os convertidos e tentados
    divisao_LL = df_full["LL%"].str.split("/")
    # resultado dos convertidos
    Pts_C_LL = divisao_LL.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo
    # eu separei ele e o resultado separei
    Pts_T1_LL = divisao_LL.str.get(1)
    divisao3_LL = Pts_T1_LL.str.split(" ")
    # resultado da separação
    Pts_T_LL = divisao3_LL.str.get(0)
    # add nos dados
    df_full["LL_C"] = Pts_C_LL
    df_full["LL_T"] = Pts_T_LL
    # tirei a coluna "Pts C/T %"
    df_full.drop('LL%', axis=1, inplace=True)
    ##################################################################################
    # REBOTES
    # divisão 1 separa da porcentagem
    divisao1_RT = df_full["RD+RO RT"].str.split(" ")
    # resultado da porcentagem
    RT = divisao1_RT.str.get(1)
    # separar os convertidos e tentados
    divisao_RO = df_full["RD+RO RT"].str.split("+")
    # resultado dos convertidos
    RD = divisao_RO.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo
    # eu separei ele e o resultado separei
    RO1 = divisao_RO.str.get(1)
    divisaoRD = RO1.str.split(" ")
    # resultado da separação
    RO = divisaoRD.str.get(0)
    # add nos dados
    df_full["RO"] = RO
    df_full["RD"] = RD
    df_full["RT"] = RT
    # tirei a coluna "Pts C/T %"
    df_full.drop("RD+RO RT", axis=1, inplace=True)
    ####################################################################################################
    return df_full, nome_casa, nome_fora


def tipo_1_tabela(element, driver, i, temporada, Data, Fase, Campeonato):
    html_content = element.get_attribute('outerHTML')
    elementaway = driver.find_element_by_xpath(
        "//div[@class='stats_real_time_table_away table-wrapper float-left']//table")
    html_content_2 = elementaway.get_attribute('outerHTML')
    # passear o conteúdo em HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')
    soup_2 = BeautifulSoup(html_content_2, 'html.parser')
    table_2 = soup_2.find(name='table')
    r1 = requests.get(f'{i}')
    soup01 = BeautifulSoup(r1.content, 'html.parser')
    informacoes_1 = soup01.find_all("div", class_="score_header large-12 small-12 medium-12 columns")
    informacoes_2 = soup01.find_all("div", class_="float-right text-left score_header_right")
    nome_casa = informacoes_1[0].find("span", class_="show-for-large").get_text()
    nome_fora = informacoes_2[0].find("span", class_="show-for-large").get_text()
    # acontece erro por conta de nomes com siglas ai eu preciso substituir
    nome_casa = nome_casa.replace('/', ' ')
    ######################### nome_casa = verificacao_nomes(nome_casa)
    nome_fora = nome_fora.replace('/', ' ')
    ########################## nome_fora = verificacao_nomes(nome_fora)
    ###########################################################################################
    # Estruturar conteúdos em uma Data Frame
    time_casa = pd.read_html(str(table))[0]
    linhas = len(time_casa)
    tamanho_casa = [nome_casa for item in range(linhas)]
    tamanho_casa_adversario = [nome_fora for item01 in range(linhas)]
    tamanho01_casa = ['casa' for item02 in range(linhas)]
    ano_casa = [temporada for item03 in range(linhas)]
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
    time_casa['Min'] = time_casa['Min'].astype(str)
    time_casa['Min'] = time_casa['Min'].str.replace(':', '.')
    time_casa['Min'] = time_casa['Min'].astype(float)
    soma1 = round(time_casa['Min'].sum(), 0)
    time_casa.loc[(time_casa['Jogador'] == 'Equipe') | (time_casa['Jogador'] == 'Total'), 'Min'] = soma1
    time_fora = pd.read_html(str(table_2))[0]
    linhas_fora = len(time_fora)
    tamanho_fora = [nome_fora for itens in range(linhas_fora)]
    tamanho01_fora = ['fora' for itens01 in range(linhas_fora)]
    ano_fora = [temporada for itens02 in range(linhas_fora)]
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
    time_fora['Min'] = time_fora['Min'].astype(str)
    time_fora['Min'] = time_fora['Min'].str.replace(':', '.')
    time_fora['Min'] = time_fora['Min'].astype(float)
    soma2 = round(time_fora['Min'].sum(), 0)
    time_fora.loc[(time_fora['Jogador'] == 'Equipe') | (time_fora['Jogador'] == 'Total'), 'Min'] = soma2
    ###################################################################################################
    df_full = pd.concat([time_casa, time_fora], axis=0)
    df_full.drop('+-', axis=1, inplace=True)
    df_full.drop('EF', axis=1, inplace=True)
    # precisa colocar tirar a marcação (T) pois atapalha os nomes e não tem em todas as tabelas
    nome_com_T = df_full['Jogador'].str.translate({ord(c): "," for c in "()"})
    nome_sem_T = nome_com_T.str.replace(' ,T,', '')
    df_full['Jogador'] = nome_sem_T
    # substituir os nomes de Equipes e Total. Deixar padrão.
    df_full['Jogador'] = df_full['Jogador'].str.replace('Total', 'Equipe')
    # substitui os valores nulos por 0
    # df_full.fillna(0, inplace=True)
    ########################################################################################
    # divisão 1 separa da porcentagem
    divisao1 = df_full["Pts C/T %"].str.split(" ")
    # separar os convertidos e tentados
    divisao = df_full["Pts C/T %"].str.split("/")
    # resultado dos convertidos
    Pts_C = divisao.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo
    # eu separei ele e o resultado separei
    Pts_T1 = divisao.str.get(1)
    divisao3 = Pts_T1.str.split(" ")
    # resultado da separação
    Pts_T = divisao3.str.get(0)
    # add nos dados
    df_full["Pts_C"] = Pts_C
    df_full["Pts_T"] = Pts_T
    # tirei a coluna "Pts C/T %"
    df_full.drop('Pts C/T %', axis=1, inplace=True)
    ####################################################################################
    # divisão 1 separa da porcentagem
    divisao1_3 = df_full["3 P C/T %"].str.split(" ")
    # separar os convertidos e tentados
    divisao_3 = df_full["3 P C/T %"].str.split("/")
    # resultado dos convertidos
    Pts_C_3 = divisao_3.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei
    # ele e o resultado separei
    Pts_T1_3 = divisao_3.str.get(1)
    divisao3_3 = Pts_T1_3.str.split(" ")
    # resultado da separação
    Pts_T_3 = divisao3_3.str.get(0)
    # add nos dados
    df_full["Pts_3_C"] = Pts_C_3
    df_full["Pts_3_T"] = Pts_T_3
    # tirei a coluna "3 P C/T %"
    df_full.drop('3 P C/T %', axis=1, inplace=True)
    #########################################################################################
    # 2 PONTOS
    # divisão 1 separa da porcentagem
    divisao1_2 = df_full["2 P C/T %"].str.split(" ")
    # separar os convertidos e tentados
    divisao_2 = df_full["2 P C/T %"].str.split("/")
    # resultado dos convertidos
    Pts_C_2 = divisao_2.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo
    # eu separei ele e o resultado separei
    Pts_T1_2 = divisao_2.str.get(1)
    divisao3_2 = Pts_T1_2.str.split(" ")
    # resultado da separação
    Pts_T_2 = divisao3_2.str.get(0)
    # add nos dados
    df_full["Pts_2_C"] = Pts_C_2
    df_full["Pts_2_T"] = Pts_T_2
    # tirei a coluna "2 P C/T %"
    df_full.drop('2 P C/T %', axis=1, inplace=True)
    ###########################################################################################
    # LANCE LIVRE
    # divisão 1 separa da porcentagem
    divisao1_LL = df_full["LL C/T %"].str.split(" ")
    # separar os convertidos e tentados
    divisao_LL = df_full["LL C/T %"].str.split("/")
    # resultado dos convertidos
    Pts_C_LL = divisao_LL.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso
    # esse processo eu separei ele e o resultado separei
    Pts_T1_LL = divisao_LL.str.get(1)
    divisao3_LL = Pts_T1_LL.str.split(" ")
    # resultado da separação
    Pts_T_LL = divisao3_LL.str.get(0)
    # add nos dados
    df_full["LL_C"] = Pts_C_LL
    df_full["LL_T"] = Pts_T_LL
    # tirei a coluna "LL C/T %"
    df_full.drop('LL C/T %', axis=1, inplace=True)
    #######################################################################################
    # REBOTES
    # divisão 1 separa da porcentagem
    divisao1_RT = df_full["RO+RD RT"].str.split(" ")
    # resultado da porcentagem
    RT = divisao1_RT.str.get(1)
    # separar os convertidos e tentados
    divisao_RO = df_full["RO+RD RT"].str.split("+")
    # resultado dos convertidos
    RO = divisao_RO.str.get(0)
    # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo
    # eu separei ele e o resultado separei
    RO1 = divisao_RO.str.get(1)
    divisaoRD = RO1.str.split(" ")
    # resultado da separação
    RD = divisaoRD.str.get(0)
    # add nos dados
    df_full["RO"] = RO
    df_full["RD"] = RD
    df_full["RT"] = RT
    # tirei a coluna "RO+RD RT"
    df_full.drop("RO+RD RT", axis=1, inplace=True)
    return df_full, nome_casa, nome_fora


def organizacao_tabelas(df_full, temporada, numero_jogo, nome_casa, nome_fora, tabela_geral):
    df_full.fillna(0, inplace=True)
    df_full = df_full.astype(
        {'RO': 'int64', 'RD': 'int64', 'RT': 'int64', 'AS': 'int64', 'BR': 'int64', 'TO': 'int64',
         'FR': 'int64', 'EN': 'int64', 'Pts_C': 'int64', 'Pts_T': 'int64', 'Pts_3_C': 'int64',
         'Pts_3_T': 'int64', 'Pts_2_C': 'int64', 'Pts_2_T': 'int64', 'LL_C': 'int64',
         'LL_T': 'int64', 'ER': 'int64', 'FC': 'int64'})
    # df_full.to_csv('parte_3.csv')
    #######################################################################################
    dif = list(df_full[df_full['Jogador'] == 'Equipe']['Pts_C'].diff(periods=-1))[0]
    dif = int(dif)
    if dif == 0:
        # encontrar a soma da diferença do placar
        resutado_casa = df_full[df_full['Casa/Fora'] == 'casa']['Pts_C'].sum()
        resutado_fora = df_full[df_full['Casa/Fora'] == 'fora']['Pts_C'].sum()
        #  encontrar os valores da dos times
        casa_pre = list(
            df_full[(df_full['Jogador'] == 'Equipe') & (df_full['Casa/Fora'] == 'casa')].values)
        pre_fora = list(
            df_full[(df_full['Jogador'] == 'Equipe') & (df_full['Casa/Fora'] == 'fora')].values)
        # somar os valores apenas de cada equipe
        sub_casa = list(df_full[df_full['Casa/Fora'] == 'casa'].sum())
        sub_fora = list(df_full[df_full['Casa/Fora'] == 'fora'].sum())
        # substituir valores de informações do jogo
        sub_casa[0:3] = casa_pre[0][0:3]
        sub_fora[0:3] = pre_fora[0][0:3]
        sub_casa[10:17] = casa_pre[0][10:17]
        sub_fora[10:17] = pre_fora[0][10:17]
        # localizar cada time e realizar a substituição dos valores somados anteriormente
        df_full.loc[(df_full['Jogador'] == 'Equipe') & (df_full['Casa/Fora'] == 'casa')] = sub_casa
        df_full.loc[(df_full['Jogador'] == 'Equipe') & (df_full['Casa/Fora'] == 'fora')] = sub_fora
        # valor da diferença do placar
        dif = resutado_casa - resutado_fora
    # valores positivos e negatovos
    resultado_jogo = [
        'vitória' if ((x == 'casa') & (dif >= 0)) | ((x == 'fora') & (dif <= 0)) else 'derrota' for x
        in df_full['Casa/Fora']]

    dif_placar = [
        f'{int(positivo(dif))}' if ((x == 'casa') & (dif >= 0)) | ((x == 'fora') & (dif <= 0)) else
        f'{int(negativo(dif))}' for x in df_full['Casa/Fora']]

    df_full['Vitoria/Derrota'] = resultado_jogo
    df_full['Diferenca_Placar'] = dif_placar
    df_full['Ar_Pts_C'] = df_full['Pts_3_C'] + df_full['Pts_2_C']
    df_full['Ar_Pts_T'] = df_full['Pts_3_T'] + df_full['Pts_2_T']
    df_full['Ar_Pts_C'] = df_full['Ar_Pts_C'].astype(int)
    df_full['Ar_Pts_T'] = df_full['Ar_Pts_T'].astype(int)
    df_full['posse_de_bola'] = round(
        df_full['Ar_Pts_T'] - df_full['RO'] + df_full['ER'] + (0.4 * df_full['LL_T']), 0)
    df_full['posse_de_bola'] = df_full.posse_de_bola.astype(int)

    df_full = df_full[
        ['Temporada', 'Time', 'Oponente', 'Data', 'Semana', 'Classificatoria/Playoffs', 'Casa/Fora',
         'Vitoria/Derrota', 'Diferenca_Placar', 'Jogador', 'Min', 'Pts_C', 'Ar_Pts_C', 'Pts_T',
         'Ar_Pts_T', 'Pts_3_C', 'Pts_3_T', 'Pts_2_C', 'Pts_2_T', 'LL_C', 'LL_T', 'RO',
         'RD', 'RT', 'AS', 'BR', 'TO', 'FC', 'FR', 'ER', 'EN', 'posse_de_bola']]
    df_full.to_csv(
        "Dados/temporada " + f"{temporada}""/" + "tabela_" + f"{numero_jogo}" + "_" + nome_casa + "_x_"
        + nome_fora + ".csv")
    nome_inf_coluna = nome_casa + "_x_" + nome_fora
    print(nome_inf_coluna)
    tabela_geral = pd.concat([df_full, tabela_geral], axis=0)
    return tabela_geral


def salvar_dados_tabela(tabela_geral_tabela, lista_cada_temporada_tabela, temporada, lista_funcionando, l1, l2, lista_falha):
    # retorna uma tabela geral de cada temporada
    lista_cada_temporada_tabela = pd.concat([tabela_geral_tabela, lista_cada_temporada_tabela], axis=0)
    tabela_geral_tabela.to_csv('Dados/temporada ' + f'{temporada}' + '/Total_de_Tabela_' + f'{temporada}' + '.csv')
    # retorna os sites que funcionam de cada temoporada
    list_sites_funciona = pd.DataFrame(lista_funcionando)
    list_sites_funciona.to_csv('Dados/temporada ' + f'{temporada}' + '/funcionando_' + f'{temporada}' + '.csv')
    l1 = pd.concat([list_sites_funciona, l1], axis=0)
    # retorna os sites que NÃO funcionam de cada temoporada
    list_sites_falha = pd.DataFrame(lista_falha)
    list_sites_falha.to_csv('Dados/temporada ' + f'{temporada}' + '/falha_' + f'{temporada}' + '.csv')
    l2 = pd.concat([list_sites_falha, l2], axis=0)
    return l1, l2, lista_cada_temporada_tabela


def localizar_tabela(driver, i, temporada, Data, Fase, Campeonato, tabela_geral, numero_jogo):
    driver.find_element_by_xpath(
        "//div[@class='row tabs_content']//ul//li//a[@id='stats-label']").click()
    try:
        element = driver.find_element_by_xpath(
            "//div[@class='stats_real_time_table_home table-wrapper float-left']//table")
    except NoSuchElementException:
        element = driver.find_element_by_xpath(
            "//table[@class='team_general_table tablesorter tablesorter-default']")
        df_full, nome_casa, nome_fora = tipo_2_tabela(element, driver, i, temporada, Data, Fase, Campeonato)
    else:
        df_full, nome_casa, nome_fora = tipo_1_tabela(element, driver, i, temporada, Data, Fase, Campeonato)
    ###################################################################################################
    # sai do for
    tabela_geral = organizacao_tabelas(df_full, temporada, numero_jogo, nome_casa, nome_fora, tabela_geral)

    return nome_casa, nome_fora, tabela_geral

