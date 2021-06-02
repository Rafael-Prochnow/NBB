from funcoes import *
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

# Chamando arquivos para serem
tabela_geral_acao, lista_cada_temporada_acao, l1_acao, l2_acao = arquivos_acao_df()
lista_funcionando_acao, lista_falha_acao, list_sites_falha_acao, list_sites_funciona_acao = arquivos_acao_lista()
# essa é a ordem das temporadas
temporada = 2020

lista_de_temporadas = [59]

for x in lista_de_temporadas:
    print(f'Temporada {temporada}')
    r = requests.get(f'https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D={x}')
    soup = BeautifulSoup(r.content, 'html.parser')
    list_inoutControl = get_links_from(soup)
    numero_jogo = 1
    for i in list_inoutControl:
        pagina = requests.get(f'{i}')
        erro_na_pagina = BeautifulSoup(pagina.content, 'html.parser')
        if not erro_na_pagina.find_all("b"):
            print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
            lista_falha_acao.append(i)
            numero_jogo += 1
        else:
            erro_na_pagina01 = erro_na_pagina.find_all("b")
            erro_na_pagina02 = erro_na_pagina01[0].get_text()
            # por motivos de erro da página coloquei isso
            if (i == 'https://lnb.com.br/partidas/nbb-20162017-paulistano-x-caxias-do-sul-20122016-1930/') | \
                    (i == 'https://lnb.com.br/noticias/com_personalidade_/') | \
                    (i == 'https://lnb.com.br/noticias/mais-do-que-especial-2/') | \
                    (i == 'https://lnb.com.br/noticias/agora-sim-5/') | \
                    (i == 'https://lnb.com.br/partidas/nbb-2020-2021-corinthians-x-fortaleza-b-c-16122020-2000/') | \
                    (i == 'https://lnb.com.br/partidas/nbb-2020-2021-minas-x-corinthians-14122020-2000/'):
                print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
                lista_falha_acao.append(i)
                numero_jogo += 1
            elif erro_na_pagina02 != 'Fatal error':
                print(f'Jogo {numero_jogo}')
                lista_funcionando_acao.append(i)
                ########################################################################################################
                # pegar o nome dos times
                r1 = requests.get(f'{i}')
                soup01 = BeautifulSoup(r1.content, 'html.parser')
                option = Options()
                option.headless = True
                driver = webdriver.Firefox(options=option)
                driver.get(f'{i}')
                time.sleep(10)
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
                driver.quit()
                numero_jogo += 1
            elif erro_na_pagina02 == 'Fatal error':
                print(f'Essa página {i} não está funcionando')
                lista_falha_acao.append(i)
                numero_jogo += 1
    l1, l2 = salvar_dados_acao(tabela_geral_acao, lista_cada_temporada_acao, temporada, lista_funcionando_acao, l1_acao, l2_acao, lista_falha_acao)
    tabela_geral = pd.DataFrame([])
    list_sites_funciona = []
    list_sites_falha = []
    temporada -= 1

lista_cada_temporada_acao.to_csv('Dados01/Total_de_acao_acao.csv')
l1_acao.to_csv('Dados01/funcionando.csv')
l2_acao.to_csv('Dados01/falha.csv')


