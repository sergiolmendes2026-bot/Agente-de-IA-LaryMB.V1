import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- BANCO DE DADOS (Persistência do Histórico) ---
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

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Larymb" width="100">
            <h3>Agente de IA Larymb.v1</h3>
            <div style="color: #00ff41; font-size: 0.8em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegação
    if st.button("🏠 Início", use_container_width=True, key="btn_i"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="btn_c"): st.session_state.page = "Conversas"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password", key="api_key_input")
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.link_button("✉️ Email para Suporte", "mailto:seuemail@exemplo.com", use_container_width=True)

# --- LÓGICA DE NAVEGAÇÃO ---
if "page" not in st.session_state: st.session_state.page = "Início"

# --- PÁGINA INÍCIO (CHAT) ---
if st.session_state.page == "Início":
    st.markdown('<h1 style="text-align:center;">Como posso te ajudar hoje?</h1>', unsafe_allow_html=True)
    
    # Carregar mensagens do banco de dados
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM chats ORDER BY id ASC")
    mensagens = c.fetchall()
    conn.close()

    # Exibir histórico
    for role, content in mensagens:
        with st.chat_message(role):
            st.markdown(content)
            
    # Entrada do Usuário
    if prompt := st.chat_input("Qual sua dúvida?"):
        if not api_key:
            st.error("Insira sua API Key na lateral.")
        else:
            # Salvar usuário no banco
            salvar_mensagem("user", prompt)
            
            # Chamar Groq
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            resposta = response.choices[0].message.content
            
            # Salvar IA no banco
            salvar_mensagem("assistant", resposta)
            st.rerun()

# --- PÁGINA CONVERSAS ---
elif st.session_state.page == "Conversas":
    st.header("💬 Conversas")
    st.write("Aqui ficará o seu histórico consolidado.")
    # Você pode copiar a mesma lógica de consulta do banco aqui para exibir tudo
