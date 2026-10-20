# 1. IMPORTAÇÃO DE BIBLIOTECAS
import streamlit as st  # Importa a biblioteca visual

# 2. CONFIGURAÇÃO DA PÁGINA
st.title("A minha Primeira Aplicação")

# 3. INTERAÇÃO COM O UTILIZADOR (ENTRADA DE DADOS)
nome = st.text_input("Qual é o teu nome?")

# 4. LÓGICA E SAÍDA DE DADOS
if nome:
    st.write(f"Olá, {nome}! O teu ficheiro app.py está a funcionar perfeitamente.")