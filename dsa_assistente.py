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

# --- CSS GLOBAL ---
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
    if st.button("🏠 Início", use_container_width=True, key="btn_i"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="btn_c"): st.session_state.page = "Conversas"
    if st.button("🕒 Histórico", use_container_width=True, key="btn_h"): st.session_state.page = "Histórico"
    if st.button("⚙️ Configurações", use_container_width=True, key="btn_co"): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password", key="api_key_input")
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.link_button("✉️ Email para Suporte", "mailto:seuemail@exemplo.com", use_container_width=True)

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
    
    # Exibir histórico
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM chats ORDER BY id ASC")
    mensagens = c.fetchall()
    conn.close()

    for role, content in mensagens:
        with st.chat_message(role):
            st.markdown(content)
            
    # Entrada do Usuário
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
    st.write("Aqui você verá seu histórico completo.")

elif st.session_state.page == "Configurações":
    st.header("⚙️ Configurações")
    st.write("Personalize o comportamento do seu agente.")
    
    # Exemplo de configuração: Modo Tradutor
    modo_tradutor = st.checkbox("Ativar Modo Tradutor", help="Se ativado, o agente focará em traduções.")
    
    if modo_tradutor:
        st.success("Modo Tradutor Ativado!")
    else:
        st.info("Modo Assistente Padrão Ativo.")
        
    st.write("---")
    if st.button("Limpar Histórico de Chat"):
        conn = sqlite3.connect('historico_chat.db')
        c = conn.cursor()
        c.execute("DELETE FROM chats")
        conn.commit()
        conn.close()
        st.warning("Histórico apagado com sucesso!")
        st.rerun()

else:
    st.header(f"Página: {st.session_state.page}")
    st.write("Conteúdo em desenvolvimento...")
