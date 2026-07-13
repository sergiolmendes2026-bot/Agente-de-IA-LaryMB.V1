import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS PERSONALIZADO (O segredo do visual) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .sidebar-avatar { text-align: center; padding: 20px 0; }
    .status-online { color: #00ff41; font-size: 0.8em; margin-bottom: 20px; }
    .main-title { font-size: 3em; font-weight: bold; text-align: center; margin-top: 50px; }
    .sub-title { text-align: center; color: #888; margin-bottom: 40px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR COM O VISUAL DESEJADO ---
with st.sidebar:
    # 1. Avatar e Status (Visual Premium)
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Larymb" width="100">
            <h3 style="margin-top: 10px;">Agente de IA Larymb.v1</h3>
            <p style="font-size: 0.8em; color: #888;">v1.0.0</p>
            <div style="color: #00ff41; font-size: 0.8em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 2. Navegação
    if st.button("🏠 Início", use_container_width=True): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True): st.session_state.page = "Conversas"
    if st.button("⭐ Favoritos", use_container_width=True): st.session_state.page = "Favoritos"
    if st.button("🕒 Histórico", use_container_width=True): st.session_state.page = "Histórico"
    if st.button("⚙️ Configurações", use_container_width=True): st.session_state.page = "Configurações"
    
    st.markdown("---")
    
    # 3. Informações de Suporte (Fixas no final da sidebar)
    st.markdown("""
        <div style="font-size: 0.85em; color: #ccc; margin-top: 20px;">
            <p><strong>Desenvolvido para auxiliar em suas dúvidas.</strong><br>
            IA pode cometer erros. Sempre verifique as respostas.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.link_button("✉️ Email para Suporte", "mailto:seuemail@exemplo.com", use_container_width=True)
    
    st.markdown("---")
    
    # Botões de Navegação com ícones
    if st.button("🏠 Início", use_container_width=True): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True): st.session_state.page = "Conversas"
    
    st.markdown("---")
    
    # Histórico (Onde ficam os botões dinâmicos)
    st.subheader("Histórico")
    with st.container(height=300):
        # Aqui entra a lógica de listar conversas do banco (como fizemos antes)
        pass 

# --- ÁREA PRINCIPAL (Visual Bem-vindo) ---
if "page" not in st.session_state: st.session_state.page = "Início"

if st.session_state.page == "Início":
    st.markdown('<div class="main-title">Como posso te ajudar hoje?</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Seu guia inteligente para respostas, explicações e referências.</div>', unsafe_allow_html=True)
    
    # Colunas para os cards de atalho
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.button("Respostas Inteligentes", use_container_width=True)
    with col2: st.button("Explicações Detalhadas", use_container_width=True)
    with col3: st.button("Referências Confiáveis", use_container_width=True)
    with col4: st.button("Rápido e Eficiente", use_container_width=True)
