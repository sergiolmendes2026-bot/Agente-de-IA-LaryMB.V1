import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- PROMPT DE SISTEMA ---
# Substitua o texto abaixo pelas instruções específicas da imagem
SYSTEM_PROMPT = """
Você é o Agente de IA Larymb.v1. Sua função é atuar como um guia inteligente, 
fornecendo respostas precisas, explicações claras e referências úteis. 
Sempre mantenha um tom profissional, prestativo e neutro. 
Sempre informe que a IA pode cometer erros e que o usuário deve verificar as informações importantes.
"""

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats 
                  (id INTEGER PRIMARY KEY, role TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def salvar_mensagem(role, content):
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute("INSERT INTO chats (role, content, timestamp) VALUES (?, ?, ?)",
              (role, content, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

init_db()

# --- CSS GLOBAL E SIDEBAR ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #4B0082; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Larymb" width="100">
            <h3>Agente de IA Larymb.v1</h3>
            <div style="color: #D8BFD8; font-size: 0.8em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🏠 Início", use_container_width=True): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True): st.session_state.page = "Configurações"
    
    st.markdown("---")
    # Gerenciamento da chave de API no session_state
    if "api_key" not in st.session_state: st.session_state.api_key = ""
    st.session_state.api_key = st.text_input("Insira sua API Key Groq", type="password", value=st.session_state.api_key)
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    URL_WHATSAPP = f"https://wa.me/5511994376755?text=Olá,%20preciso%20de%20ajuda%20com%20o%20Agente%20de%20IA."
    st.sidebar.markdown(f'<a href="{URL_WHATSAPP}" target="_blank" style="color: white; text-decoration: none;">📱 WhatsApp de Suporte</a>', unsafe_allow_html=True)

# --- LÓGICA DE NAVEGAÇÃO ---
if "page" not in st.session_state: st.session_state.page = "Início"

# --- PÁGINA INÍCIO ---
if st.session_state.page == "Início":
    st.markdown('<h1 style="text-align: center; color: white;">Como posso <span style="color: #8B5CF6;">te ajudar</span> hoje?</h1>', unsafe_allow_html=True)
    
    # Exibir histórico do BD
    conn = sqlite3.connect('historico_chat.db')
    mensagens = conn.execute("SELECT role, content FROM chats ORDER BY id ASC").fetchall()
    conn.close()

    for role, content in mensagens:
        with st.chat_message(role):
            st.markdown(content)
            
    if prompt := st.chat_input("Qual sua dúvida?"):
        if not st.session_state.api_key:
            st.error("Insira sua API Key na lateral.")
        else:
            salvar_mensagem("user", prompt)
            
            # Preparar contexto para a API
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for role, content in mensagens:
                messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": prompt})
            
            client = Groq(api_key=st.session_state.api_key)
            response = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile")
            
            resposta = response.choices[0].message.content
            salvar_mensagem("assistant", resposta)
            st.rerun()

elif st.session_state.page == "Conversas":
    st.header("💬 Conversas")
    mensagens = sqlite3.connect('historico_chat.db').execute("SELECT role, content FROM chats ORDER BY id ASC").fetchall()
    for role, content in mensagens:
        with st.chat_message(role): st.markdown(content)

elif st.session_state.page == "Configurações":
    st.header("⚙️ Configurações")
    if st.button("Limpar Histórico de Chat"):
        conn = sqlite3.connect('historico_chat.db')
        conn.execute("DELETE FROM chats")
        conn.commit()
        conn.close()
        st.rerun()
