import streamlit as st
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS COM CONTRASTE MELHORADO ---
st.markdown("""
    <style>
    /* Fundo geral escuro */
    .stApp { background-color: #05070a; color: #ffffff; }
    
    /* Sidebar mais clara para destacar o campo de input */
    [data-testid="stSidebar"] {
        background-color: #161622 !important; 
        border-right: 1px solid #333;
    }
    
    /* Garantir que textos na sidebar fiquem brancos */
    [data-testid="stSidebar"] * { color: #FAFAFA !important; }
    
    /* Estilo do campo de input da API Key */
    div[data-baseweb="input"] {
        background-color: #0e1117 !important;
        border: 1px solid #4a4a5a !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (ÚNICO BLOCO) ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h2 style="margin-top: 10px;">Agente de IA Larymb.v1</h2>
            <div style="color: #60A5FA; font-size: 0.9em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegação com 'key' única para evitar erros
    if st.button("🏠 Início", use_container_width=True, key="nav_home"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="nav_chat"): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True, key="nav_config"): st.session_state.page = "Configurações"
    
    st.markdown("---")
    
    # Campo de API Key com label customizada
    st.markdown("**Coloque aqui sua GROQ API Key e pressione Enter**")
    api_key = st.text_input("", type="password", key="api_key_side", label_visibility="collapsed")
    
    st.markdown("---")
    # Aviso no estilo de caixa informativa
    st.info("Aviso: a IA pode cometer erros. Verifique fatos críticos.", icon="ℹ️")
    
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)
    st.link_button("💬 WhatsApp de Suporte", "https://wa.me/5511994376755", use_container_width=True)

# --- LÓGICA DE PÁGINAS ---
if "page" not in st.session_state: st.session_state.page = "Início"

if st.session_state.page == "Início":
    st.markdown("""
        <div style="text-align: center; margin-top: 100px;">
            <p style="color: #8B5CF6; font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">Bem-vindo!</p>
            <h1 style="color: white; font-size: 3rem; margin-bottom: 10px;">
                Como posso <span style="color: #8B5CF6;">te ajudar</span> hoje?
            </h1>
            <p style="color: #9ca3af; font-size: 1.1rem;">Seu guia inteligente para respostas, explicações e referências.</p>
        </div>
    """, unsafe_allow_html=True)
