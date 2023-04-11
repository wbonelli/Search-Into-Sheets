import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Define as informações da planilha
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)
client = gspread.authorize(creds)

# Define a função que faz a busca na planilha


def buscar_valor(planilha_link, valor_busca):
    # Abre a planilha
    planilha = client.open_by_url(planilha_link)

    # Percorre todas as abas da planilha
    for aba in planilha.worksheets():
        # Busca pelo valor na aba atual
        try:
            celula = aba.find(valor_busca)
            # Retorna o resultado da busca
            return {"valor": valor_busca, "celula": celula.address, "aba": aba.title}
        except:
            # Se o valor não foi encontrado na aba atual, passa para a próxima
            pass

    # Se o valor não foi encontrado em nenhuma das abas, retorna uma mensagem de erro
    return {"valor": valor_busca, "celula": "Não encontrado", "aba": "Não encontrado"}


# Define a interface do usuário
st.title("Busca Dados na Planilha")
planilha_link = st.text_input("Cole o link da planilha aqui")
valor_busca = st.text_input("Digite o valor que deseja buscar")

# Faz a busca na planilha ao clicar no botão
if st.button("Buscar"):
    resultado = buscar_valor(planilha_link, valor_busca)
    st.table(resultado)
