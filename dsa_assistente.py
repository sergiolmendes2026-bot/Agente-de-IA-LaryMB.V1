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
            <div style="font-weight: bold; font-size: 0.8em; color: white;">
                <span style="color: #00FF00; margin-right: 5px;">●</span>
<span>Status: Online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🏠 Início", use_container_width=True, key="btn_i"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="btn_c"): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True, key="btn_co"): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password", key="api_key_input")
    
 # --- Aviso de IA com design azul ---
    st.markdown("""
        <div style="
            background-color: #2C3E50; 
            padding: 15px; 
            border-radius: 10px; 
            color: #5DADE2; 
            font-family: sans-serif; 
            margin-bottom: 20px;
        ">
            <strong>Aviso:</strong> a IA pode gerar respostas imprecisas, incompletas ou erradas. Sempre verifique informações críticas antes de confirmar totalmente. <br>
            
        </div>
    """, unsafe_allow_html=True)
    
    # --- Configuração Link WhatsApp ---
    NUMERO_TELEFONE = "5511994376755"
    MENSAGEM_PADRAO = "Olá, preciso de ajuda com o Agente de IA."
    URL_WHATSAPP = f"https://wa.me/{NUMERO_TELEFONE}?text={MENSAGEM_PADRAO.replace(' ', '%20')}"
    
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

    st.markdown(
        f"""
        <a href="{URL_WHATSAPP}" target="_blank" style="
            display: flex; align-items: center; justify-content: center;
            background-color: #262730; color: #FAFAFA; padding: 0.5rem 1rem;
            border-radius: 0.5rem; text-decoration: none; font-weight: 400;
            border: 1px solid #464e5f; width: 100%; box-sizing: border-box;
        ">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20" style="margin-right: 10px;">
            WhatsApp de Suporte
        </a>
        """, unsafe_allow_html=True
    )

# --- LÓGICA DE NAVEGAÇÃO ---
if "page" not in st.session_state: st.session_state.page = "Início"

# --- PÁGINA INÍCIO ---
if st.session_state.page == "Início":
    st.markdown("""
        <h1 style="text-align: center; color: white;">
            Como posso <span style="color: #8B5CF6;">te ajudar</span> hoje?
        </h1>
        <p style="text-align: center; color: #888; margin-bottom: 30px;">
            Seu guia inteligente para respostas, explicações e referências.
        </p>
    """, unsafe_allow_html=True)
    
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM chats ORDER BY id ASC")
    mensagens = c.fetchall()
    conn.close()

    for role, content in mensagens:
        with st.chat_message(role):
            st.markdown(content)
            
    if prompt := st.chat_input("Qual sua dúvida?"):
        if not api_key:
            st.error("Insira sua API Key na lateral.")
        else:
            salvar_mensagem("user", prompt)
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile"
            )
            resposta = response.choices[0].message.content
            salvar_mensagem("assistant", resposta)
            st.rerun()

elif st.session_state.page == "Conversas":
    st.header("💬 Conversas")
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM chats ORDER BY id ASC")
    mensagens = c.fetchall()
    conn.close()

    if not mensagens:
        st.info("Nenhuma conversa salva ainda.")
    else:
        for role, content in mensagens:
            with st.chat_message(role):
                st.markdown(content)

elif st.session_state.page == "Configurações":
    st.header("⚙️ Configurações")
    if st.button("Limpar Histórico de Chat"):
        conn = sqlite3.connect('historico_chat.db')
        c = conn.cursor()
        c.execute("DELETE FROM chats")
        conn.commit()
        conn.close()
        st.warning("Histórico apagado!")
        st.rerun()
