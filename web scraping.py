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
    '''# informações para a tabela tabela
    table_inf = soup.find(name='table')
    # estruturar conteúdo em uma Data Frame - Pandas
    informacoes = pd.read_html(str(table_inf))[0]
    ii = 0'''
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
                # ação ação
                lista_falha_acao.append(i)
                '''# Tabela 
                lista_falha.append(i)'''
                numero_jogo += 1
            elif erro_na_pagina02 != 'Fatal error':
                print(f'Jogo {numero_jogo}')
                # ação ação
                lista_funcionando_acao.append(i)
                '''# Tabela
                lista_funcionando.append(i)'''
                ########################################################################################################
                # pegar o nome dos times
                r1 = requests.get(f'{i}')
                soup01 = BeautifulSoup(r1.content, 'html.parser')
                option = Options()
                option.headless = True
                driver = webdriver.Firefox(options=option)
                driver.get(f'{i}')
                time.sleep(10)
                '''# Pegar os dados Tabela Tabela
                Data = informacoes['DATA'][ii]
                Fase = informacoes['FASE'][ii]
                Campeonato = informacoes['CAMPEONATO'][ii]'''

                # Pegar os dados Jogada Jogada
                tabela_geral = localizar_acao(driver, i, temporada, numero_jogo, tabela_geral_acao)
                driver.quit()
                numero_jogo += 1
            elif erro_na_pagina02 == 'Fatal error':
                print(f'Essa página {i} não está funcionando')
                lista_falha_acao.append(i)
                numero_jogo += 1
    l1_acao, l2_acao = salvar_dados_acao(tabela_geral_acao, lista_cada_temporada_acao, temporada, lista_funcionando_acao, l1_acao, l2_acao, lista_falha_acao)
    tabela_geral = pd.DataFrame([])
    list_sites_funciona = []
    list_sites_falha = []
    temporada -= 1

lista_cada_temporada_acao.to_csv('Dados01/Total_de_acao_acao.csv')
l1_acao.to_csv('Dados01/funcionando.csv')
l2_acao.to_csv('Dados01/falha.csv')


