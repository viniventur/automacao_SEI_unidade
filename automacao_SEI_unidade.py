import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values
env = dotenv_values('.env')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pyautogui
import requests
from bs4 import BeautifulSoup


import time

# Abrindo o SEI
driver = webdriver.Chrome()
driver.get(env['SITE_SEI'])


# Login e seleção da unidade

usuario_sei = env['CPF_SEI']
senha_sei = env['SENHA_SEI']

driver.find_element("xpath", '//*[@id="txtUsuario"]').send_keys(usuario_sei)
driver.find_element("xpath", '//*[@id="pwdSenha"]').send_keys(senha_sei)
driver.find_element("xpath", '//*[@id="selOrgao"]').send_keys('CGE')
driver.find_element("xpath", '//*[@id="sbmLogin"]').click()

# Selecionar unidade
unidade_usuario = driver.find_element("xpath", '//*[@id="selInfraUnidades"]')
Select(unidade_usuario).select_by_visible_text(env['UNIDADE'])

# Consultar processos

processo = 'E:35032.0000003108/2024'

time.sleep(1)
driver.find_element("xpath", '//*[@id="txtPesquisaRapida"]').send_keys(processo)
driver.find_element("xpath", '//*[@id="txtPesquisaRapida"]').send_keys(Keys.ENTER)
unidade_usuario = driver.find_element("xpath", '//*[@id="selInfraUnidades"]')
Select(unidade_usuario).select_by_visible_text(env['UNIDADE'])

# Alternar para o iframe 'ifrArvore'
iframe_arvore = driver.find_element('name', "ifrArvore")
driver.switch_to.frame(iframe_arvore)

driver.find_element("xpath", '//*[@id="divConsultarAndamento"]/a/span').click() # consultar andamento

# Alternar para o iframe 'ifrVisualizacao'
driver.switch_to.default_content()
iframe_visualizacao = driver.find_element('name', "ifrVisualizacao")
driver.switch_to.frame(iframe_visualizacao)

# Looping de raspagem

df = pd.read_excel('lista_processos.xlsx')

for processo in df['Processo Mãe']:

    time.sleep(1.5)
    driver.find_element("xpath", '//*[@id="txtPesquisaRapida"]').send_keys(processo)
    driver.find_element("xpath", '//*[@id="txtPesquisaRapida"]').send_keys(Keys.ENTER)

    # Alternar para o iframe 'ifrArvore'
    iframe_arvore = driver.find_element('name', "ifrArvore")
    driver.switch_to.frame(iframe_arvore)

    driver.find_element("xpath", '//*[@id="divConsultarAndamento"]/a/span').click() # consultar andamento
        
    # Alternar para o iframe 'ifrVisualizacao'
    driver.switch_to.default_content()
    iframe_visualizacao = driver.find_element('name', "ifrVisualizacao")
    driver.switch_to.frame(iframe_visualizacao)

    # Extrai os dados da primeira linha da tabela
    data_hora = driver.find_element(By.XPATH, '//*[@id="tblHistorico"]/tbody/tr[2]/td[1]').text  # Coluna 1: Data/Horário
    unidade = driver.find_element(By.XPATH, '//*[@id="tblHistorico"]/tbody/tr[2]/td[2]').text    # Coluna 2: Unidade
    usuario = driver.find_element(By.XPATH, '//*[@id="tblHistorico"]/tbody/tr[2]/td[3]').text    # Coluna 3: Usuário
    descricao = driver.find_element(By.XPATH, '//*[@id="tblHistorico"]/tbody/tr[2]/td[4]').text  # Coluna 4: Descrição

    # Cria um dicionário para organizar os dados extraídos
    dados = {
        "Data Horário": data_hora,
        "Unidade Atual": unidade,
        "Usuário CPF": usuario,
        "Descrição": descricao
    }

    # Atualiza o DataFrame de forma mais eficiente
    df.loc[df['Processo Mãe'] == processo, ['Data Horário', 'Unidade Atual', 'Usuário CPF', 'Descrição']] = [
        dados["Data Horário"], dados["Unidade Atual"], dados["Usuário CPF"], dados["Descrição"]
    ]

    # Voltar ao contexto principal
    driver.switch_to.default_content()


time.sleep(2000)

driver.quit()