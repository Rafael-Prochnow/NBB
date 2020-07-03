import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.common.exceptions import NoSuchElementException
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
ii = 0


for i in list_inoutControl:

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
             'Tempo': tempo,
             'Time_01': time_site,
             'Placar': placar,
             'Inf_2': acao_pessoa02
             })

        # erro de espaços vindo de cima
        Indicador01 = dados['Time_01'].str.replace(
            '.                                                                    \n\n', '')
        # limpeza dos dados tirando Fim de partida e dos quartos

        erro02 = Indicador01.str.replace('Fim de partida', 'NaN')
        erro03 = erro02.str.replace('Fim  do quarto quarto', 'NaN')
        erro04 = erro03.str.replace('Início do  quarto quarto', 'NaN')
        erro05 = erro04.str.replace('Fim  do terceiro quarto', 'NaN')
        erro06 = erro05.str.replace('Início do  terceiro quarto', 'NaN')
        erro07 = erro06.str.replace('Fim  do segundo quarto', 'NaN')
        erro08 = erro07.str.replace('Início do  segundo quarto', 'NaN')
        erro09 = erro08.str.replace('Fim  do primeiro quarto', 'NaN')
        erro10 = erro09.str.replace('Início do  primeiro quarto', 'NaN')
        Indicador_consertado = erro10.str.replace('Início de partida', 'NaN')
        # deve ter prorrogação!!!!

        dados['Time'] = Indicador_consertado
        dados.drop('Time_01', axis=1, inplace=True)
        # erro de espaços vinda de cima
        Indicador02 = dados['Inf_2'].str.replace(
            '                                                                    \n\n', '')

        divisao1_retirado = Indicador02.str.translate({ord(c): " " for c in ".!_+"})
        dados['Indicador_01'] = divisao1_retirado
        dados.drop('Inf_2', axis=1, inplace=True)
        ################################################################################################################
        divisao1_placar = dados["Placar"].str.split(" x ")
        placar_casa = divisao1_placar.str.get(0)
        placar_visitante = divisao1_placar.str.get(1)
        dados['placar_casa'] = placar_casa
        dados['placar_visitante'] = placar_visitante
        dados.drop('Placar', axis=1, inplace=True)

        # esses valores estão invertidos ou seja
        # Nome; Indicador
        # Indicador ; Nome
        # não posso separa-los diretamente então vou fazer uma gambiarra
        # esses são os valores onde apresentam os nomes
        divisao1 = dados["Indicador_01"]

        a1 = divisao1.str.replace('Fim de partida', '1/fim_partida;')
        a2 = a1.str.replace('Início de partida', '1/inicio_partida;')
        a3 = a2.str.replace('Início do  primeiro quarto', '1/inicio_quarto;')
        a4 = a3.str.replace('Início do  segundo quarto', '1/inicio_quarto;')
        a5 = a4.str.replace('Início do  terceiro quarto', '1/inicio_quarto;')
        a6 = a5.str.replace('Início do  quarto quarto', '1/inicio_quarto;')
        a7 = a6.str.replace('Fim  do quarto quarto', '/fim_quarto;')
        a8 = a7.str.replace('Fim  do terceiro quarto', '1/fim_quarto;')
        a9 = a8.str.replace('Fim  do segundo quarto', '1/fim_quarto;')
        a10 = a9.str.replace('Fim  do primeiro quarto', '1/fim_quarto;')

        ####################################################################################################
        # esses são os valores que estão os indicadores
        a11 = a10.str.replace('É de três  ', '')
        a12 = a11.str.replace(' acerta arremesso de três pontos', '/3_Pts_C;1')
        a13 = a12.str.replace(' erra tentativa para três pontos', '/3_Pts_T;1')
        # lance livre
        a14 = a13.str.replace(' acerta o lance livre', '/LL_Pts_C;1')
        a15 = a14.str.replace(' erra o lance livre', '/LL_Pts_T;1')
        # Dois pontos
        a16 = a15.str.replace(' acerta arremesso de dois pontos', '/2_Pts_C;1')
        a17 = a16.str.replace(' erra tentativa para dois pontos', '/2_Pts_T;1')
        # rebotes
        a18 = a17.str.replace(' pega rebote defensivo', '/RD;1')
        a19 = a18.str.replace(' pega rebote ofensivo', '/RO;1')
        # recuperação de bola
        a20 = a19.str.replace(' recupera a bola', '/BR;1')
        # assistencia
        a21 = a20.str.replace('Assistência do ', '/AS;')
        # faltas recebidas
        a22 = a21.str.replace(' sofre falta', '/FR;1')
        # faltas cometidas
        a23 = a22.str.replace(' comete falta técnica', '/FC_T;1')
        a24 = a23.str.replace(' comete falta antidesportiva', '/FC_A;1')
        a25 = a24.str.replace(' comete falta ofensiva', '/FC_O;1')
        a26 = a25.str.replace(' comete falta', '/FC;1')
        # substituição
        a27 = a26.str.replace('Entra ', '/substituicao_entra;')
        a28 = a27.str.replace('Sai ', '/substituicao_sai;')
        # erros
        a29 = a28.str.replace(' perde posse de bola', '/ER;1')
        a30 = a29.str.replace('Estouro dos 24s', '/ER;1')
        a31 = a30.str.replace(' andou com a bola', '/ER;1')
        a32 = a31.str.replace(' comete violação de saída de quadra', '/ER;1')
        # tocos
        a33 = a32.str.replace(' dá um toco', '/TO;1')
        # tempo técnico
        a34 = a33.str.replace('Técnico da equipe ', '')
        a35 = a34.str.replace(' pede tempo ', '/tempo_tecnico;')
        # cravada
        a36 = a35.str.replace('Cravada ', '')
        a37 = a36.str.replace(' acerta enterrada', '/EN;1')

        # primeira separação é coloco na ordem dos nomes e depois indicadores
        # o ; é para fazer a primeira separação
        # 1 é para conter um valor apenas, pois quando separo e junto, caso não tenha um valor, o resultado retira os valores
        mudados_00 = a37.str.split(';')
        mudados_01 = mudados_00.str.get(1)
        mudados_02 = mudados_00.str.get(0)

        alinhados = mudados_01 + mudados_02
        # agora que juntou e alinhou os nomes
        # organizar novamente
        alinhados_01 = alinhados.str.split('/')
        alinhados_02 = alinhados_01.str.get(0)
        alinhados_03 = alinhados_01.str.get(1)

        # depois de separado vamos organizar por nomes e retirar os valores que ajudaram na primeira separação, como 1 e espaço

        alinhados_04 = alinhados_02.str.replace('1 ', '')
        alinhados_05 = alinhados_04.str.replace(' 1', '')

        dados["Indicador"] = alinhados_03
        dados["Nomes"] = alinhados_05
        dados.drop('Indicador_01', axis=1, inplace=True)
    else:
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
        a1 = divisao1_retirado.str.replace('FIM DE PARTIDA Fim de partida', 'fim_partida;')
        a2 = a1.str.replace('INÍCIO DE QUARTO Início de partida', 'inicio_partida;')
        a3 = a2.str.replace('INÍCIO DE QUARTO Início do quarto quarto', 'inicio_quarto;')
        a4 = a3.str.replace('INÍCIO DE QUARTO Início do terceiro quarto', 'inicio_quarto;')
        a5 = a4.str.replace('INÍCIO DE QUARTO Início do segundo quarto', 'inicio_quarto;')
        a6 = a5.str.replace('FIM DE QUARTO Fim do quarto quarto', 'fim_quarto;')
        a7 = a6.str.replace('FIM DE QUARTO Fim do terceiro quarto', 'fim_quarto;')
        a8 = a7.str.replace('FIM DE QUARTO Fim do segundo quarto', 'fim_quarto;')
        a9 = a8.str.replace('FIM DE QUARTO Fim do primeiro quarto', 'fim_quarto;')

        # fora revisados os dados na primeira planilha. eu sei que está certo uma olhada pq
        # os dados apresentam padrão na escrita
        ########################################################################################################################
        # três pontos
        a10 = a9.str.replace("Tentativa para três pontos ", "3_Pts_T;")
        a11 = a10.str.replace('É DE TRÊS  É de três  ', '3_Pts_C;')
        a12 = a11.str.replace(' erra tentativa para três pontos', '')
        a13 = a12.str.replace(' acerta arremesso de três pontos', '')
        # lance livre
        a14 = a13.str.replace(' 1 PONTO ', 'LL_Pts_C;')
        a15 = a14.str.replace('Lance Livre Errado ', 'LL_Pts_T;')
        a16 = a15.str.replace(' acerta o lance livre', '')
        a17 = a16.str.replace(' erra o lance livre', '')
        # dois pontos
        a18 = a17.str.replace('Tentativa para dois pontos ', '2_Pts_T;')
        a19 = a18.str.replace(' 2 PONTOS ', '2_Pts_C;')
        a20 = a19.str.replace(' erra tentativa para dois pontos', '')
        a21 = a20.str.replace(' acerta arremesso de dois pontos', '')
        # rebotes
        a22 = a21.str.replace('REBOTE DEFENSIVO ', 'RD;')
        a23 = a22.str.replace('REBOTE OFENSIVO ', 'RO;')
        a24 = a23.str.replace(' pega rebote ofensivo', '')
        a25 = a24.str.replace(' pega rebote defensivo', '')
        # recuperação da bola
        a26 = a25.str.replace('Bola recuperada ', 'BR;')
        a27 = a26.str.replace(' recupera a bola', '')
        # assistência
        a28 = a27.str.replace('ASSISTÊNCIA Assistência do ', 'AS;')
        # faltas recebidas
        a29 = a28.str.replace('Falta sofrida ', 'FR;')
        a30 = a29.str.replace(' sofre falta', '')
        # faltas cometidas
        a31 = a30.str.replace('FALTA OFENSIVA', 'FC_O;')
        a32 = a31.str.replace(' comete falta ofensiva', '')
        a34 = a32.str.replace('FALTA ANTIDESPORTIVA ', 'FC_A;')
        a35 = a34.str.replace(' antidesportiva', '')
        # substituições
        a36 = a35.str.replace('Substituição Entra ', 'substituicao_entra;')
        a37 = a36.str.replace('Substituição Sai ', 'substituicao_sai;')
        # Erros
        a38 = a37.str.replace(' Violação Estouro dos 24s', 'ER;')
        a39 = a38.str.replace('Violação ', 'ER;')
        a40 = a39.str.replace('Erro ', 'ER;')
        a41 = a40.str.replace(' perde posse de bola', '')
        a42 = a41.str.replace(' comete violação de saída de quadra', '')
        a43 = a42.str.replace('nan', '')
        # tocos
        a44 = a43.str.replace('TOCO  ', 'TO;')
        a45 = a44.str.replace(' dá um toco', '')
        # tempo técnico
        a46 = a45.str.replace(' TEMPO TÉCNICO Técnico da equipe ', 'tempo_tecnico;')
        a47 = a46.str.replace(' pede tempo', '')
        # enterrada
        a48 = a47.str.replace('CRAVADA  Cravada ', 'EN;')
        a49 = a48.str.replace(' acerta enterrada ', '')
        #########################################################################################################
        # outra revisão
        a50 = a49.str.replace('FALTA TÉCNICA ', 'FC_T;')
        a51 = a50.str.replace(' comete falta técnica', '')
        a52 = a51.str.replace('FALTA ', 'FC;')
        a53 = a52.str.replace(' comete falta', '')
        # a = a.str.replace(' andou com a bola', '/ER;1')

        # adicionar e tirar os dados
        dados['mudados'] = a53
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

    dados.to_csv(f"./Dados01/tabela_{ii}.csv", index=None)

    ii = ii + 1
    driver.quit()
