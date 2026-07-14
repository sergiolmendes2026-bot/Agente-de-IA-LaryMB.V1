import streamlit as st
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS E SIDEBAR DARK ---
st.markdown("""
    <style>
    /* Fundo principal */
    .stApp { background-color: #05070a; color: #ffffff; }
    
    /* Sidebar Dark */
    [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
        border-right: 1px solid #262730;
    }
    
    /* Ajuste de fontes na sidebar */
    [data-testid="stSidebar"] * { color: #FAFAFA !important; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h2 style="margin-top: 10px;">Agente de IA Larymb.v1</h2>
            <div style="color: #60A5FA; font-size: 0.9em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Botões de Navegação com 'key' única para não dar erro
    if st.button("🏠 Início", use_container_width=True, key="btn_home"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="btn_chat"): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True, key="btn_config"): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password", key="api_key_side")
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

# --- LÓGICA DE PÁGINAS ---
if "page" not in st.session_state: st.session_state.page = "Início"

if st.session_state.page == "Início":
    st.markdown("""
        <div style="text-align: center; margin-top: 100px;">
            <p style="color: #8B5CF6; font-size: 1.2rem; font-weight: bold; margin-bottom: 0;">Bem-vindo!</p>
            <h1 style="color: white; font-size: 3rem;">Como posso <span style="color: #8B5CF6;">te ajudar</span> hoje?</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Área de Chat
    if prompt := st.chat_input("Qual sua dúvida?"):
        if not api_key:
            st.error("Por favor, insira sua API Key na barra lateral.")
        else:
            with st.chat_message("user"): st.markdown(prompt)
            # Adicione aqui sua lógica de chamada à API Groq
