import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import pandas as pd

r = requests.get('https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D=34')
soup = BeautifulSoup(r.content, 'html.parser')

def get_links_from(soup):
    links = []
    for a in soup.findAll('a', attrs={'class': 'small-4 medium-12 large-12 float-left match_score_relatorio'}):
        links.append((a.get('href')))
    return links


list_inoutControl = get_links_from(soup)
del(list_inoutControl[:241])
print(list_inoutControl)

#print(list_inoutControl)

#######################################################################################################################
option = Options()
option.headless = True
driver = webdriver.Firefox()
# options=option

driver.get(list_inoutControl[1])
time.sleep(10)
########################################################################################################################
# função

driver.find_element_by_xpath(
    "//div[@class='row tabs_content']//ul//li//a[@id='stats-label']").click()

# ai precisa fazer uma separação de conteúdos
# primeiro para uma tabelas

element = driver.find_element_by_xpath("//div[@class='stats_real_time_table_home table-wrapper float-left']//table")
html_content = element.get_attribute('outerHTML')

elementaway = driver.find_element_by_xpath("//div[@class='stats_real_time_table_away table-wrapper float-left']//table")
html_content_2 = elementaway.get_attribute('outerHTML')

# passear o conteúdo em HTML
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

soup_2 = BeautifulSoup(html_content_2, 'html.parser')
table_2 = soup_2.find(name='table')

# Estruturar conteúdos em uma Data Frame
time_casa = pd.read_html(str(table))[0]
time_fora = pd.read_html(str(table_2))[0]

df_full = pd.concat([time_casa, time_fora], axis=0)


df_full.drop('+-', axis=1, inplace=True)
df_full.drop('EF', axis=1, inplace=True)

df_full['Min'] = df_full['Min'].str.replace(':', '.')

print(df_full)

# divisão 1 separa da porcentagem
divisao1 = df_full["Pts C/T %"].str.split(" ")
# separar os convertidos e tentados
divisao = df_full["Pts C/T %"].str.split("/")
# resultado dos convertidos
Pts_C = divisao.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1 = divisao.str.get(1)
divisao3 = Pts_T1.str.split(" ")
# resultado da separação
Pts_T = divisao3.str.get(0)
# add nos dados
df_full["Pts_C"] = Pts_C
df_full["Pts_T"] = Pts_T
# tirei a coluna "Pts C/T %"
df_full.drop('Pts C/T %', axis=1, inplace=True)
########################################################################################################################
# divisão 1 separa da porcentagem
divisao1_3 = df_full["3 P C/T %"].str.split(" ")
# separar os convertidos e tentados
divisao_3 = df_full["3 P C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_3 = divisao_3.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_3 = divisao_3.str.get(1)
divisao3_3 = Pts_T1_3.str.split(" ")
# resultado da separação
Pts_T_3 = divisao3_3.str.get(0)
# add nos dados
df_full["3_Pts_C"] = Pts_C_3
df_full["3_Pts_T"] = Pts_T_3
# tirei a coluna "3 P C/T %"
df_full.drop('3 P C/T %', axis=1, inplace=True)
########################################################################################################################
# 2 PONTOS
# divisão 1 separa da porcentagem
divisao1_2 = df_full["2 P C/T %"].str.split(" ")
# separar os convertidos e tentados
divisao_2 = df_full["2 P C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_2 = divisao_2.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_2 = divisao_2.str.get(1)
divisao3_2 = Pts_T1_2.str.split(" ")
# resultado da separação
Pts_T_2 = divisao3_2.str.get(0)
# add nos dados
df_full["2_Pts_C"] = Pts_C_2
df_full["2_Pts_T"] = Pts_T_2
# tirei a coluna "2 P C/T %"
df_full.drop('2 P C/T %', axis=1, inplace=True)
########################################################################################################################
# LANCE LIVRE
# divisão 1 separa da porcentagem
divisao1_LL = df_full["LL C/T %"].str.split(" ")
# separar os convertidos e tentados
divisao_LL = df_full["LL C/T %"].str.split("/")
# resultado dos convertidos
Pts_C_LL = divisao_LL.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
Pts_T1_LL = divisao_LL.str.get(1)
divisao3_LL = Pts_T1_LL.str.split(" ")
# resultado da separação
Pts_T_LL = divisao3_LL.str.get(0)
# add nos dados
df_full["LL_Pts_C"] = Pts_C_LL
df_full["LL_Pts_T"] = Pts_T_LL
# tirei a coluna "LL C/T %"
df_full.drop('LL C/T %', axis=1, inplace=True)
########################################################################################################################
# REBOTES
# divisão 1 separa da porcentagem
divisao1_RT = df_full["RO+RD RT"].str.split(" ")
# resultado da porcentagem
RT = divisao1_RT.str.get(1)
# separar os convertidos e tentados
divisao_RO = df_full["RO+RD RT"].str.split("+")
# resultado dos convertidos
RO = divisao_RO.str.get(0)
# como os tentados ta no meio e eu não sei pegar ele sem toso esse processo eu separei ele e o resultado separei de novo
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
########################################################################################################################
# drive de saída
df_full.to_csv("tabela_noiss.csv", index=None)
# precisa colocar a mudança de nomes
