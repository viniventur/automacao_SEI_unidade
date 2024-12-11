import pandas as pd
import os
import streamlit as st
from dotenv import load_dotenv, dotenv_values
env = dotenv_values('.env')

from login import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pyautogui
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
import base64
import time

st.set_page_config(layout="wide", page_title='Extrator de dados - SEI - OGP/CGE', page_icon='src/assets/Identidades visual/OGP/LOGO-OGP - icon.jpg')

def main():

    # VER VER VER O DARK MODE PADRAO
    # Criar um contêiner fixo no topo da página
    header = st.container()

    def get_image_as_base64(file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")

    logo_path_CGE = 'src/assets/Identidades visual/Logo CGE Governo/LOGO GOV-branco.png'
    logo_path_OGP = 'src/assets/Identidades visual/OGP/APRESENTAÇÃO_LOGO_-_OBSERVATÓRIO_DA_GESTÃO_PÚBLICA_BRANCO_TRANSP.png'
    logo_base64_CGE = get_image_as_base64(logo_path_CGE)
    logo_base64_OGP = get_image_as_base64(logo_path_OGP)

    with st.container():
        # Centralizando as imagens lado a lado
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 150px;">
                <img src="data:image/png;base64,{logo_base64_CGE}" style="margin-right: 20px; width: 300px;">
                <img src="data:image/png;base64,{logo_base64_OGP}" style="width: 250px;">
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.container():
        # Centralizando o texto no meio da tela
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100px; text-align: center;">
                <h1 style="font-size: 35px; margin: 0;">Extrator de Dados de Andamento de Processos do SEI</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

### Olá! Bem vindo extrator de dados do SEI

    with st.container():

        st.write('''
                 
                 # 

                 Obs.: Os dados de logins fornecidos não são armazenados, servindo apenas para o sistema logar no SEI e carregar as informações.                 
                 
                 ''')

    # Input para o usuário
    usuario = st.text_input('Usuário SEI:', placeholder="Digite seu nome de usuário do SEI.")

    # Input para a senha (caracteres ocultos)
    senha = st.text_input('Senha SEI:', type='password', placeholder="Digite sua senha do SEI.")

    # Lista de orgaos login
    with st.spinner('Obtendo órgãos disponíveis no SEI...'):
        lista_orgaos = lista_orgaos_login()
        orgao = st.selectbox("Órgão:", lista_orgaos)

    # Login
    if st.button("Login"):
        login_sei(usuario, senha, orgao)



    '''

    # adicionar input para a unidade (lista de seleção)
    unidade = st.selectbox('Selecione a Unidade', lista_unidades)
    '''


if __name__ == "__main__":
    main()