import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

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
/* Fundo da aplicação */
.stApp { background-color: #050505; color: #ffffff; }

/* Estilização da Sidebar */
[data-testid="stSidebar"] {
    background-color: #4B0082; 
}

/* Ajuste para o texto dentro da sidebar ficar branco */
[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Larymb" width="100">
            <h3>Agente de IA Larymb.v1</h3>
            <div style="color: #D8BFD8; font-size: 0.8em; font-weight: bold;">Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🏠 Início", use_container_width=True, key="btn_i"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="btn_c"): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True, key="btn_co"): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password", key="api_key_input")
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.link_button("✉️ Email para Suporte", "sergiolmendes2026@gmail.com", use_container_width=True)

    # Configuração do Link WhatsApp
    NUMERO_TELEFONE = "5511994376755"
    MENSAGEM_PADRAO = "Olá, preciso de ajuda com o Agente de IA."
    URL_WHATSAPP = f"https://wa.me/{NUMERO_TELEFONE}?text={MENSAGEM_PADRAO.replace(' ', '%20')}"

    st.markdown(
        f"""
        <a href="{URL_WHATSAPP}" target="_blank" style="
            display: flex; align-items: center; justify-content: left;
            background-color: #262730; color: #FAFAFA; padding: 0.5rem 1rem;
            border-radius: 0.5rem; text-decoration: none; border: 1px solid #464e5f;
            width: 100%; box-sizing: border-box;
        ">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20" style="margin-right: 10px;">
        WhatsApp de Suporte
        </a>
        """, unsafe_allow_html=True
    )

# --- LÓGICA DE NAVEGAÇÃO E RESTANTE DO CÓDIGO ---
# (Certifique-se de que o resto do código abaixo também não tenha espaços extras à esquerda)
if "page" not in st.session_state: st.session_state.page = "Início"
# ... continue com o restante da sua lógica ...
