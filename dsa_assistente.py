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

# --- SIDEBAR ---
with st.sidebar:
    # Opção Recomendada: Usar o componente nativo do Streamlit para maior estabilidade
    # Ele lida melhor com o redimensionamento e carregamento
    st.image("https://img.freepik.com/vetores-premium/icone-de-robo-tecnologico-moderno_1122-345.jpg", 
             width=150, # Aumentei para 150 para ficar bem grande
             output_format="PNG")
    
    st.markdown("""
        <div style="text-align: center;">
            <h3 style="margin-top: 10px;">Agente de IA Larymb.v1</h3>
            <div style="color: #60A5FA; font-size: 0.9em; font-weight: bold; margin-bottom: 20px;">
                ● Status: Online
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    
    st.markdown("---")
    if st.button("🏠 Início", use_container_width=True): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password")
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

# --- Lógica do WhatsApp ---
URL_WHATSAPP = f"https://wa.me/5511994376755?text=Olá,%20preciso%20de%20ajuda."

st.sidebar.markdown(f"""
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
