import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import io
import html5lib


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

# fazer um if caso tenha prorrogação

# df = pd.DataFrame(a9, sep=';')
data = io.StringIO(a9)
df = pd.read_csv(data,sep=';')
# lated = acoes.translate(str.maketrans({' 1º': '\n', ' 2º': '\n', ' 3º': '\n', ' 4º': '\n'}))

# .reset_index
print(df)


