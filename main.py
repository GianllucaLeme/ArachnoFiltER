import os
import time
import datetime

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')
edge_service = Service(edge_driver_path)
edge_options = Options()
edge_options.add_argument(f'user-agent={user_agent}')

browser = webdriver.Edge(service=edge_service, options=edge_options)
browser.get("https://sites.google.com/view/arachnotrac/neotropical-spiders?authuser=0")
browser.maximize_window()

time.sleep(2)

# Procura uma família específica
familia = 'LINYPHIIDAE'
abrir_familia = browser.find_element(By.XPATH,f"//span[contains(text(), '{familia}')]")
abrir_familia.click()

time.sleep(2)

# Abre a lista de gêneros de uma família e a coloca em um txt local

lista = '//*[@id="h.148f5de7d885156b_250"]/div/div/ul'
lista_genero = browser.find_element(By.XPATH, lista)

with open('generos.txt', 'w') as file:
    file.write(lista_genero.text)

# Organiza a lista de gêneros para mostrar apenas os gêneros e em ordem alfabética, evitando repetições

lista_genero_final = []
with open('generos.txt', 'r') as file:
    for line in file:
        first_word = line.strip().split()[0]  # Pega a primeira palavra
        lista_genero_final.append(first_word)

#print(set(lista_genero_final))
#print("\n")
print(sorted(set(lista_genero_final)))

time.sleep(8)