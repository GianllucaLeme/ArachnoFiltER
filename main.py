import os
import json
import re

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Função para abrir a janela do navegador somente APÓS o input do usuário
def janela_hold():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
    edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')
    edge_service = Service(edge_driver_path)
    edge_options = Options()
    edge_options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Edge(service=edge_service, options=edge_options)
    return browser

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
def ArachnoTrAC(lista, familia):
    browser = janela_hold()
    browser.get('https://sites.google.com/view/arachnotrac/neotropical-spiders?authuser=0')
    browser.maximize_window()
    
    # Procura uma família específica
    abrir_familia = element_click(browser, By.XPATH, f"//span[normalize-space(text())='{familia.upper()}']")
    scroll_element(browser, abrir_familia)

    # Acessa a lista de espécies de uma dada família e a coloca em um txt local
    with open('familias_xpath.json', 'r') as file:
        familias_xpath = json.load(file)

    if familia.upper() in familias_xpath:
        lista_path = familias_xpath[familia.upper()]
        lista_generos = browser.find_element(By.XPATH, lista_path)
        
    with open('generos_ArachnoTrAC.txt', 'w', encoding='utf-8') as file:
        file.write(lista_generos.text)

    # Organiza a lista de espécies para mostrar apenas os gêneros
    with open('generos_ArachnoTrAC.txt', 'r', encoding='utf-8') as file:
        for line in file:
            primeira_palavra = line.strip().split()[0]  # Pega a primeira palavra
            lista.append(primeira_palavra)

    return lista

def iNaturalist(lista, taxon):
    browser = janela_hold()
    browser.get('https://www.inaturalist.org')
    browser.maximize_window()

    # Acessar a página do táxon informado
    search_button = element_present(browser, By.XPATH, '//*[@id="headersearch"]/button[1]')
    search_button.click()

    search_box = element_present(browser, By.XPATH, '//*[@id="headersearch"]/div/div/input')
    search_box.send_keys(taxon)

    taxon_link = element_click(browser, By.XPATH, "//li[contains(@class, 'ac-result')]//a[contains(@class, 'about')]")
    taxon_link.click()

    taxonomy_tab = element_click(browser, By.XPATH, '//*[@id="main-tabs"]/li[4]/a')
    scroll_element(browser, taxonomy_tab)

    lista_taxon = element_present(browser, By.XPATH, "//ul[@class='plain taxonomy']//li[contains(@class, 'all-shown tabular')]")
    
    # Escrevendo apenas as linhas do texto de 'lista_taxon' que possui números
    with open('generos_iNaturalist.txt', 'w', encoding='utf-8') as file:
        for line in lista_taxon.text.splitlines():
            if re.search(r'\d', line):
                file.write(line + '\n')  # Escrita de apenas linhas com números

    # Leitura de apenas o nome do táxon
    with open('generos_iNaturalist.txt', 'r', encoding='utf-8') as file:
        for line in file:
            segunda_palavra = line.strip().split()[1]  # Pega a segunda palavra de cada linha
            lista.append(segunda_palavra)  # Adiciona na lista

    return lista

# Função principal que aborda todo o projeto
def main():
    # Preenchimento das listas
    familia = input('\nDigite o nome da família: ').strip().upper()
    if familia:
        lista_ArachnoTrAC = []
        ArachnoTrAC(lista_ArachnoTrAC, familia)  # Preenche a lista com dados da família

    taxon = input('\nDigite o nome do táxon: ').strip()
    if taxon:
        lista_iNat = []
        iNaturalist(lista_iNat, taxon)  # Preenche a lista com dados do táxon

    # Análise de itens em comum
    if familia and taxon:
        lista_intersecao = set(lista_ArachnoTrAC).intersection(set(lista_iNat))
        print('\nItens em comum:', sorted(lista_intersecao) + '\n')

if __name__ == '__main__':
    main()