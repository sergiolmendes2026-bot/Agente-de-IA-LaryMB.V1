import streamlit as st
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- SIDEBAR ESTRUTURADO ---
with st.sidebar:
    # Cabeçalho da Sidebar
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h2 style="margin-top: 10px;">Agente de IA Larymb.v1</h2>
            <div style="color: #60A5FA; font-size: 0.9em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegação com 'key' única para evitar erros de duplicidade
    if st.button("🏠 Início", use_container_width=True, key="btn_inicio_sidebar"): 
        st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="btn_conversas_sidebar"): 
        st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True, key="btn_config_sidebar"): 
        st.session_state.page = "Configurações"
    
    st.markdown("---")
    
    # Campo de API Key com chave única
    api_key = st.text_input("Insira sua API Key Groq", type="password", key="api_key_input")
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

    # Botão WhatsApp
    URL_WHATSAPP = "https://wa.me/5511994376755?text=Olá,%20preciso%20de%20ajuda."
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

# --- NAVEGAÇÃO LÓGICA ---
if "page" not in st.session_state: 
    st.session_state.page = "Início"

# Aqui entra o restante da sua lógica de exibição de cada página (Início, Conversas, etc.)
