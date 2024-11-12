import os
import json

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')
edge_service = Service(edge_driver_path)
edge_options = Options()
edge_options.add_argument(f'user-agent={user_agent}')

browser = webdriver.Edge(service=edge_service, options=edge_options)

# Função para aguardar até que o elemento esteja clicável
def element_click(browser, by, locator, timeout=10):
    return WebDriverWait(browser, timeout).until(
        EC.element_to_be_clickable((by, locator))
    )

# Função para aguardar até que o elemento esteja presente no DOM
def element_present(browser, by, locator, timeout=10):
    return WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((by, locator))
    )

# Função para fazer scroll até o elemento e clicar nele via JS
def scroll_element(browser, element):
    browser.execute_script("arguments[0].scrollIntoView(true);", element)  # Faz scroll até o elemento
    browser.execute_script("arguments[0].click();", element)  # Clica no elemento usando JS

# Funções para Web Scraping
def ArachnoTrAC(lista):
    browser.get("https://sites.google.com/view/arachnotrac/neotropical-spiders?authuser=0")
    browser.maximize_window()
    
    # Procura uma família específica
    familia = 'linyphiidae'
    abrir_familia = element_click(browser, By.XPATH, f"//span[contains(text(), '{familia.upper()}')]")
    scroll_element(browser, abrir_familia)

    # Acessa a lista de gêneros de uma dada família e a coloca em um txt local
    with open('familias_xpath.json', 'r') as file:
        familias_xpath = json.load(file)

    if familia.upper() in familias_xpath:
        lista_path = familias_xpath[familia.upper()]
        lista_generos = browser.find_element(By.XPATH, lista_path)
        
    with open('generos_ArachnoTrAC.txt', 'w', encoding='utf-8') as file:
        file.write(lista_generos.text)

    # Organiza a lista de gêneros para mostrar apenas os gêneros e em ordem alfabética, evitando repetições
    with open('generos_ArachnoTrAC.txt', 'r', encoding='utf-8') as file:
        for line in file:
            primeira_palavra = line.strip().split()[0]  # Pega a primeira palavra
            lista.append(primeira_palavra)

    return lista

def iNaturalist(lista):
    browser.get("https://www.inaturalist.org/taxa/495875-Erigoninae#taxonomy-tab")
    browser.maximize_window()

    lista_path = '//*[@id="taxonomy-tab"]/div/div[1]/div/div/div[1]/div/ul/li/ul/li/ul/li/ul/li/ul/li/ul/li/ul/li/ul/li/ul/li/ul/li/ul/li/ul'
    lista_generos = element_present(browser, By.XPATH, lista_path)

    with open('generos_iNaturalist.txt', 'w') as file:
            file.write(lista_generos.text)

    with open('generos_iNaturalist.txt', 'r') as file:
        for line in file:
            segunda_palavra = line.strip().split()[1]
            lista.append(segunda_palavra)

    return lista

lista_ArachnoTrAC = []
lista_iNat = []

# Preenchimento das listas
ArachnoTrAC(lista_ArachnoTrAC)
iNaturalist(lista_iNat)

# Análise de itens em comum (Nesse commit, entre os **linifídeos da América do Sul** e os **erigoníneos do mundo todo**)
lista_intersecao = set(lista_ArachnoTrAC).intersection(set(lista_iNat))
print(sorted(lista_intersecao))