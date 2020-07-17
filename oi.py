import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=34')
soup = BeautifulSoup(r.content, 'html.parser')


def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


list_inoutControl = get_links_from(soup)
ano = 16
# jogo do pinheiros_x_vitória não aparece as estatísticas do jogo
del(list_inoutControl[1])
# jogo do mogi_x_vitoria não aparece as estatísticas do jogo 246
del(list_inoutControl[246])

#######################################################################################################################
tabela_geral = pd.DataFrame([])

for i in list_inoutControl:

    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)

    driver.get(f'{i}')
    time.sleep(10)

    driver.find_element_by_xpath(
        "//div[@class='row tabs_content']//ul//li//a[@id='stats-label']").click()

    try:
        element = driver.find_element_by_xpath(
            "//div[@class='stats_real_time_table_home table-wrapper float-left']//table")
    except NoSuchElementException:
        element = driver.find_element_by_xpath("//table[@class='team_general_table tablesorter tablesorter-default']")
        html_content = element.get_attribute('outerHTML')

        driver.find_element_by_xpath(
            "//a[@id='team_away_stats-label']").click()

        element_2 = driver.find_element_by_xpath("//table[@class='team_two_table tablesorter tablesorter-default']")
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

        time_casa = pd.read_html(str(table))[0]
        linhas = len(time_casa)
        tamanho_casa = [nome_casa for item in range(linhas)]
        tamanho_casa_adversario = [nome_fora for item01 in range(linhas)]
        tamanho01_casa = [1 for item02 in range(linhas)]
        ano_casa = [ano for item03 in range(linhas)]

        time_casa['time'] = tamanho_casa
        time_casa['casa/fora'] = tamanho01_casa
        time_casa['adversário'] = tamanho_casa_adversario
        time_casa['Temporada'] = ano_casa

        time_fora = pd.read_html(str(table_2))[0]
        linhas_fora = len(time_fora)
        tamanho_fora = [nome_fora for itens in range(linhas_fora)]
        tamanho01_fora = [2 for itens01 in range(linhas_fora)]
        ano_fora = [ano for itens02 in range(linhas_fora)]
        tamanho_fora_adversario = [nome_casa for itens03 in range(linhas_fora)]

        time_fora['time'] = tamanho_fora
        time_fora['casa/fora'] = tamanho01_fora
        time_fora['adversário'] = tamanho_fora_adversario
        time_fora['Temporada'] = ano_fora

        df_full = pd.concat([time_casa, time_fora], axis=0)

        df_full.drop('JO', axis=1, inplace=True)
        df_full.drop('+/-', axis=1, inplace=True)
        df_full.drop('EF', axis=1, inplace=True)
        # divisão 1 separa da porcentagem
        divisao1 = df_full["Pts"].str.split(" ")
        # separar os convertidos e tentados
        divisao = df_full["Pts"].str.split("/")
        # resultado dos convertidos
        Pts_C = divisao.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        Pts_T1 = divisao.str.get(1)
        divisao3 = Pts_T1.str.split(" ")
        # resultado da separação
        Pts_T = divisao3.str.get(0)
        # add nos dados
        df_full["Pts_C"] = Pts_C
        df_full["Pts_T"] = Pts_T
        # tirei a coluna "Pts C/T %"
        df_full.drop('Pts', axis=1, inplace=True)
        ################################################################################################################
        # divisão 1 separa da porcentagem
        divisao1_3 = df_full["3P%"].str.split(" ")
        # separar os convertidos e tentados
        divisao_3 = df_full["3P%"].str.split("/")
        # resultado dos convertidos
        Pts_C_3 = divisao_3.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        Pts_T1_3 = divisao_3.str.get(1)
        divisao3_3 = Pts_T1_3.str.split(" ")
        # resultado da separação
        Pts_T_3 = divisao3_3.str.get(0)
        # add nos dados
        df_full["3_Pts_C"] = Pts_C_3
        df_full["3_Pts_T"] = Pts_T_3
        # tirei a coluna "Pts C/T %"
        df_full.drop('3P%', axis=1, inplace=True)
        ################################################################################################################
        # 2 PONTOS
        # divisão 1 separa da porcentagem
        divisao1_2 = df_full["2P%"].str.split(" ")
        # separar os convertidos e tentados
        divisao_2 = df_full["2P%"].str.split("/")
        # resultado dos convertidos
        Pts_C_2 = divisao_2.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        Pts_T1_2 = divisao_2.str.get(1)
        divisao3_2 = Pts_T1_2.str.split(" ")
        # resultado da separação
        Pts_T_2 = divisao3_2.str.get(0)
        # add nos dados
        df_full["2_Pts_C"] = Pts_C_2
        df_full["2_Pts_T"] = Pts_T_2
        # tirei a coluna "Pts C/T %"
        df_full.drop('2P%', axis=1, inplace=True)
        ################################################################################################################
        # LANCE LIVRE
        # divisão 1 separa da porcentagem
        divisao1_LL = df_full["LL%"].str.split(" ")
        # separar os convertidos e tentados
        divisao_LL = df_full["LL%"].str.split("/")
        # resultado dos convertidos
        Pts_C_LL = divisao_LL.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        Pts_T1_LL = divisao_LL.str.get(1)
        divisao3_LL = Pts_T1_LL.str.split(" ")
        # resultado da separação
        Pts_T_LL = divisao3_LL.str.get(0)
        # add nos dados
        df_full["LL_Pts_C"] = Pts_C_LL
        df_full["LL_Pts_T"] = Pts_T_LL
        # tirei a coluna "Pts C/T %"
        df_full.drop('LL%', axis=1, inplace=True)
        ################################################################################################################
        # REBOTES
        # divisão 1 separa da porcentagem
        divisao1_RT = df_full["RD+RO RT"].str.split(" ")
        # resultado da porcentagem
        RT = divisao1_RT.str.get(1)
        # separar os convertidos e tentados
        divisao_RO = df_full["RD+RO RT"].str.split("+")
        # resultado dos convertidos
        RO = divisao_RO.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        RO1 = divisao_RO.str.get(1)
        divisaoRD = RO1.str.split(" ")
        # resultado da separação
        RD = divisaoRD.str.get(0)
        # add nos dados
        df_full["RO"] = RO
        df_full["RD"] = RD
        df_full["RT"] = RT
        # tirei a coluna "Pts C/T %"
        df_full.drop("RD+RO RT", axis=1, inplace=True)
    else:
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

        # Estruturar conteúdos em uma Data Frame
        time_casa = pd.read_html(str(table))[0]
        linhas = len(time_casa)
        tamanho_casa = [nome_casa for item in range(linhas)]
        tamanho_casa_adversario = [nome_fora for item01 in range(linhas)]
        tamanho01_casa = [1 for item02 in range(linhas)]
        ano_casa = [ano for item03 in range(linhas)]

        time_casa['time'] = tamanho_casa
        time_casa['casa/fora'] = tamanho01_casa
        time_casa['adversário'] = tamanho_casa_adversario
        time_casa['Temporada'] = ano_casa

        time_fora = pd.read_html(str(table_2))[0]
        linhas_fora = len(time_fora)
        tamanho_fora = [nome_fora for itens in range(linhas_fora)]
        tamanho01_fora = [2 for itens01 in range(linhas_fora)]
        ano_fora = [ano for itens02 in range(linhas_fora)]
        tamanho_fora_adversario = [nome_casa for itens03 in range(linhas_fora)]

        time_fora['time'] = tamanho_fora
        time_fora['casa/fora'] = tamanho01_fora
        time_fora['adversário'] = tamanho_fora_adversario
        time_fora['Temporada'] = ano_fora

        df_full = pd.concat([time_casa, time_fora], axis=0)

        df_full.drop('+-', axis=1, inplace=True)
        df_full.drop('EF', axis=1, inplace=True)
        df_full['Min'] = df_full['Min'].str.replace(':', '.')
        ################################################################################################################
        # divisão 1 separa da porcentagem
        divisao1 = df_full["Pts C/T %"].str.split(" ")
        # separar os convertidos e tentados
        divisao = df_full["Pts C/T %"].str.split("/")
        # resultado dos convertidos
        Pts_C = divisao.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        Pts_T1 = divisao.str.get(1)
        divisao3 = Pts_T1.str.split(" ")
        # resultado da separação
        Pts_T = divisao3.str.get(0)
        # add nos dados
        df_full["Pts_C"] = Pts_C
        df_full["Pts_T"] = Pts_T
        # tirei a coluna "Pts C/T %"
        df_full.drop('Pts C/T %', axis=1, inplace=True)
        ################################################################################################################
        # divisão 1 separa da porcentagem
        divisao1_3 = df_full["3 P C/T %"].str.split(" ")
        # separar os convertidos e tentados
        divisao_3 = df_full["3 P C/T %"].str.split("/")
        # resultado dos convertidos
        Pts_C_3 = divisao_3.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        Pts_T1_3 = divisao_3.str.get(1)
        divisao3_3 = Pts_T1_3.str.split(" ")
        # resultado da separação
        Pts_T_3 = divisao3_3.str.get(0)
        # add nos dados
        df_full["3_Pts_C"] = Pts_C_3
        df_full["3_Pts_T"] = Pts_T_3
        # tirei a coluna "3 P C/T %"
        df_full.drop('3 P C/T %', axis=1, inplace=True)
        ################################################################################################################
        # 2 PONTOS
        # divisão 1 separa da porcentagem
        divisao1_2 = df_full["2 P C/T %"].str.split(" ")
        # separar os convertidos e tentados
        divisao_2 = df_full["2 P C/T %"].str.split("/")
        # resultado dos convertidos
        Pts_C_2 = divisao_2.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        Pts_T1_2 = divisao_2.str.get(1)
        divisao3_2 = Pts_T1_2.str.split(" ")
        # resultado da separação
        Pts_T_2 = divisao3_2.str.get(0)
        # add nos dados
        df_full["2_Pts_C"] = Pts_C_2
        df_full["2_Pts_T"] = Pts_T_2
        # tirei a coluna "2 P C/T %"
        df_full.drop('2 P C/T %', axis=1, inplace=True)
        ################################################################################################################
        # LANCE LIVRE
        # divisão 1 separa da porcentagem
        divisao1_LL = df_full["LL C/T %"].str.split(" ")
        # separar os convertidos e tentados
        divisao_LL = df_full["LL C/T %"].str.split("/")
        # resultado dos convertidos
        Pts_C_LL = divisao_LL.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
        Pts_T1_LL = divisao_LL.str.get(1)
        divisao3_LL = Pts_T1_LL.str.split(" ")
        # resultado da separação
        Pts_T_LL = divisao3_LL.str.get(0)
        # add nos dados
        df_full["LL_Pts_C"] = Pts_C_LL
        df_full["LL_Pts_T"] = Pts_T_LL
        # tirei a coluna "LL C/T %"
        df_full.drop('LL C/T %', axis=1, inplace=True)
        ################################################################################################################
        # REBOTES
        # divisão 1 separa da porcentagem
        divisao1_RT = df_full["RO+RD RT"].str.split(" ")
        # resultado da porcentagem
        RT = divisao1_RT.str.get(1)
        # separar os convertidos e tentados
        divisao_RO = df_full["RO+RD RT"].str.split("+")
        # resultado dos convertidos
        RO = divisao_RO.str.get(0)
        # como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei
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

    df_full = df_full[['Temporada', 'time', 'adversário', 'casa/fora', 'Jogador', 'Min', 'Pts_C', 'Pts_T', '3_Pts_C',
                       '3_Pts_T', '2_Pts_C', '2_Pts_T', 'LL_Pts_C', 'LL_Pts_T', 'RO', 'RD', 'RT', 'AS', 'BR', 'TO',
                       'FC', 'FR', 'ER', 'EN']]
    df_full.to_csv("./temporada 2016/" + nome_casa + "_x_" + nome_fora + ".csv", index=None)

    nome_inf_coluna = nome_casa + "_x_" + nome_fora
    print(nome_inf_coluna)
    tabela_geral = pd.concat([df_full, tabela_geral], axis=0)
    driver.quit()


tabela_geral.to_csv("./temporada 2016/Tabela geral.csv")
