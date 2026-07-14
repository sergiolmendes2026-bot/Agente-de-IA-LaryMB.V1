import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# Variáveis globais de imagem
URL_ROBO = "https://img.freepik.com/vetores-premium/icone-de-robo-tecnologico-moderno_1122-345.jpg"

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
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #05070a;
        background-image: 
            radial-gradient(circle at center bottom, #0d2149 0%, #05070a 70%),
            radial-gradient(white, rgba(255, 255, 255, 0.15) 2px, transparent 3px),
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), 
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-position: center bottom, center center, 50px 50px, 50px 50px;
        background-size: auto, 100px 100px, 50px 50px, 50px 50px;
        background-repeat: no-repeat, repeat, repeat, repeat;
        color: #ffffff;
        height: 100vh; 
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(22, 23, 31, 0.9); 
        border-right: 1px solid #2e303a; 
        padding-top: 2rem;
    }}
    [data-testid="stSidebar"] * {{ color: #FAFAFA !important; }}
    div.stButton > button {{
        background-color: #262730 !important;
        border: 1px solid #464e5f !important;
        color: #FAFAFA !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR COMPLETO ---
with st.sidebar:
    # 1. Definição da string em um bloco contínuo
    CODIGO_BASE64 = """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=="""

    st.markdown(f"""
        <div style="text-align: center; padding-bottom: 20px;">
            <img src="data:image/png;base64,{CODIGO_BASE64}" width="100" style="border-radius: 50%; border: 2px solid #60A5FA;">
            <h3 style="margin-top: 10px;">Agente de IA Larymb.v1</h3>
            <div style="color: #60A5FA; font-size: 0.9em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    # Botões alinhados dentro do 'with'
    if st.button("🏠 Início", use_container_width=True): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password")
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

    # Botão WhatsApp dentro do 'with'
    URL_WHATSAPP = f"https://wa.me/5511994376755?text=Olá,%20preciso%20de%20ajuda."
    st.markdown(f"""
        <a href="{URL_WHATSAPP}" target="_blank" style="
            display: flex; align-items: center; justify-content: left;
            background-color: #262730; color: #FAFAFA; padding: 0.5rem;
            border-radius: 0.5rem; text-decoration: none; border: 1px solid #464e5f;
        ">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20" style="margin-right: 10px;">
            WhatsApp de Suporte
        </a>
    """, unsafe_allow_html=True)

# --- NAVEGAÇÃO ---
if "page" not in st.session_state: st.session_state.page = "Início"

if st.session_state.page == "Início":
    st.markdown("""
        <div style="text-align: center; margin-top: 50px;">
            <p style="color: #6366f1; font-weight: bold;">Bem-vindo!</p>
            <h1 style="color: white;">Como posso <span style="color: #8B5CF6;">te ajudar</span> hoje?</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Exibir histórico
    conn = sqlite3.connect('historico_chat.db')
    mensagens = conn.cursor().execute("SELECT role, content FROM chats ORDER BY id ASC").fetchall()
    conn.close()
    for role, content in mensagens:
        with st.chat_message(role): st.markdown(content)
            
    if prompt := st.chat_input("Qual sua dúvida?"):
        if not api_key:
            st.error("Insira sua API Key na lateral.")
        else:
            salvar_mensagem("user", prompt)
            client = Groq(api_key=api_key)
            resposta = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile").choices[0].message.content
            salvar_mensagem("assistant", resposta)
            st.rerun()

elif st.session_state.page == "Conversas":
    st.header("💬 Conversas")
    # ... (restante do código de conversas)

elif st.session_state.page == "Configurações":
    st.header("⚙️ Configurações")
    if st.button("Limpar Histórico"):
        conn = sqlite3.connect('historico_chat.db')
        conn.cursor().execute("DELETE FROM chats")
        conn.commit()
        conn.close()
        st.rerun()
