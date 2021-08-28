from funcoes import *
from funcoes_tabela import *
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Chamando arquivos das ações
tabela_geral_acao, lista_cada_temporada_acao, l1_acao, l2_acao = arquivos_acao_df()
lista_funcionando_acao, lista_falha_acao, list_sites_falha_acao, list_sites_funciona_acao = arquivos_acao_lista()

# Chamando arquivos das tabelas
lista_funcionando, lista_falha, list_sites_falha, list_sites_funciona = arquivos_tabela_lista()
tabela_geral_tabela, lista_cada_temporada_tabela, l1, l2 = arquivos_tabela_df()

# essa é a ordem das temporadas
temporada = 2021

print(f'Temporada {temporada}')
r = requests.get('https://lnb.com.br/ldb/tabela-de-jogos/?season%5B%5D=64&wherePlaying=-1&played=-1')
soup = BeautifulSoup(r.content, 'html.parser')
list_inoutControl = get_links_from(soup)
list_inoutControl = list_inoutControl[14:16]
# del (list_inoutControl[:314])
print(list_inoutControl)

numero_jogo = 1
# informações para a tabela tabela
table_inf = soup.find(name='table')
# estruturar conteúdo em uma Data Frame - Pandas
informacoes = pd.read_html(str(table_inf))[0]
ii = 0
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
                (i == 'https://lnb.com.br/partidas/nbb-2020-2021-minas-x-corinthians-14122020-2000/') | \
                (i == 'https://lnb.com.br/noticias/de-virada/') | \
                (i == 'https://lnb.com.br/noticias/feito-expressivo/') | \
                (i == 'https://lnb.com.br/noticias/so-vitorias/') | \
                (i == 'https://lnb.com.br/noticias/com-a-mao-direita/') | \
                (i == 'https://lnb.com.br/noticias/triunfo/') | \
                (i == 'https://lnb.com.br/noticias/na-raca-3/') | \
                (i == 'https://lnb.com.br/noticias/tartarugao-invicto/') | \
                (i == 'https://lnb.com.br/noticias/la-em-cima-2/') | \
                (i == 'https://lnb.com.br/noticias/so-no-tempo-extra/') | \
                (i == 'https://lnb.com.br/noticias/o-dono-do-jogo-2/') | \
                (i == 'https://lnb.com.br/noticias/faixa-carimbada/') | \
                (i == 'https://lnb.com.br/noticias/6-em-6/') | \
                (i == 'https://lnb.com.br/noticias/sem-sufoco/') | \
                (i == 'https://lnb.com.br/noticias/reaprendendo-a-vencer/') | \
                (i == 'https://lnb.com.br/noticias/no-topo-da-tabela/') | \
                (i == 'https://lnb.com.br/noticias/inicio-arrasador/') | \
                (i == 'https://lnb.com.br/noticias/causaram/') | \
                (i == 'https://lnb.com.br/noticias/no-coracao/') | \
                (i == 'https://lnb.com.br/noticias/reabilitado/') | \
                (i == 'https://lnb.com.br/noticias/resta-um/') | \
                (i == 'https://lnb.com.br/noticias/reagiu/') | \
                (i == 'https://lnb.com.br/noticias/dramatico/') | \
                (i == 'https://lnb.com.br/noticias/the-man/') | \
                (i == 'https://lnb.com.br/noticias/lider-isolado-e-100/') | \
                (i == 'https://lnb.com.br/noticias/noite-de-gala/') | \
                (i == 'https://lnb.com.br/noticias/boa-estreia/'):
            print(f'SEM DADOS KKKKKKKKKKKKKK {i}')
            # ação ação
            lista_falha_acao.append(i)
            # Tabela
            lista_falha.append(i)
            numero_jogo += 1
        elif erro_na_pagina02 != 'Fatal error':
            print(f'Jogo {numero_jogo}')
            # ação ação
            lista_funcionando_acao.append(i)
            # Tabela
            lista_funcionando.append(i)
            ########################################################################################################
            # pegar o nome dos times
            r1 = requests.get(f'{i}')
            soup01 = BeautifulSoup(r1.content, 'html.parser')
            option = Options()
            option.headless = True
            driver = webdriver.Firefox(options=option)
            driver.get(f'{i}')
            time.sleep(5)
            # Pegar os dados Tabela Tabela
            Data = informacoes['DATA'][ii]
            Fase = informacoes['FASE'][ii]
            Campeonato = informacoes['CAMPEONATO'][ii]
            # Pegar os dados Tabelas
            nome_casa, nome_fora, tabela_geral_tabela = localizar_tabela(driver, i, temporada, Data, Fase,
                                                                         Campeonato, tabela_geral_tabela,
                                                                         numero_jogo)
            if temporada >= 2013:
                # Pegar os dados Jogada Jogada
                tabela_geral_acao = localizar_acao(driver, temporada, numero_jogo, tabela_geral_acao, nome_casa,
                                                   nome_fora)
            else:
                print('não')
                pass
            driver.quit()
            numero_jogo += 1
        elif erro_na_pagina02 == 'Fatal error':
            print(f'Essa página {i} não está funcionando')
            lista_falha_acao.append(i)
            numero_jogo += 1
        ii += 1
if temporada >= 2013:
    # Salvar os dados Tabelas
    l1, l2, lista_cada_temporada_tabela = salvar_dados_tabela(tabela_geral_tabela, lista_cada_temporada_tabela,
                                                              temporada, lista_funcionando, l1, l2, lista_falha)
    # Salvar os dados  Jogada Jogada
    l1_acao, l2_acao, lista_cada_temporada_acao = salvar_dados_acao(tabela_geral_acao, lista_cada_temporada_acao,
                                                                    temporada, lista_funcionando_acao, l1_acao,
                                                                    l2_acao, lista_falha_acao)
else:
    # Salvar os dados Tabelas
    l1, l2, lista_cada_temporada_tabela = salvar_dados_tabela(tabela_geral_tabela, lista_cada_temporada_tabela,
                                                              temporada, lista_funcionando, l1, l2, lista_falha)
tabela_geral = pd.DataFrame([])
tabela_geral_tabela = pd.DataFrame([])
list_sites_funciona = []
list_sites_falha = []






