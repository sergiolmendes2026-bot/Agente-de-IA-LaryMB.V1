import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats 
                 (id INTEGER PRIMARY KEY, chat_nome TEXT, role TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def salvar_mensagem(chat_nome, role, content):
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute("INSERT INTO chats (chat_nome, role, content, timestamp) VALUES (?, ?, ?, ?)",
              (chat_nome, role, content, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

init_db()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- SIDEBAR COM GERENCIAMENTO DE CHATS ---
with st.sidebar:
    st.markdown("## 🤖 Agente de IA Larymb.v1")
    
    if st.button("➕ Nova Conversa", use_container_width=True):
        st.session_state.chat_atual = f"Conversa {datetime.datetime.now().strftime('%H:%M:%S')}"
        st.rerun()

    st.markdown("---")
    # Busca nomes únicos de chats no banco
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT chat_nome FROM chats")
    chats = [row[0] for row in c.fetchall()]
    conn.close()

    for nome in chats:
        if st.button(nome, use_container_width=True):
            st.session_state.chat_atual = nome
            st.rerun()

# --- LÓGICA DO CHAT ---
if "chat_atual" not in st.session_state:
    st.session_state.chat_atual = "Conversa 1"

st.header(f"Visualizando: {st.session_state.chat_atual}")

# Carregar mensagens do banco para a conversa atual
conn = sqlite3.connect('historico_chat.db')
c = conn.cursor()
c.execute("SELECT role, content FROM chats WHERE chat_nome = ? ORDER BY id ASC", (st.session_state.chat_atual,))
mensagens = c.fetchall()
conn.close()

for role, content in mensagens:
    with st.chat_message(role):
        st.markdown(content)

# Input
if prompt := st.chat_input("Digite sua dúvida..."):
    # Salva usuário
    salvar_mensagem(st.session_state.chat_atual, "user", prompt)
    
    # Simula chamada da IA (Groq)
    # response = client.chat.completions.create(...) 
    resposta_ia = "Resposta simulada para: " + prompt 
    
    # Salva IA
    salvar_mensagem(st.session_state.chat_atual, "assistant", resposta_ia)
    st.rerun()
