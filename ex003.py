import io
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# teste
url = 'https://lnb.com.br/nbb/tabela-de-jogos'

option = Options()
option.headless = True
driver = webdriver.Firefox()
# options=option

