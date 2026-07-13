import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .sidebar-avatar { text-align: center; padding: 20px 0; }
    .status-online { color: #00ff41; font-size: 0.8em; margin-bottom: 20px; }
    .main-title { font-size: 3em; font-weight: bold; text-align: center; margin-top: 50px; }
    .sub-title { text-align: center; color: #888; margin-bottom: 40px; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (LIMPA E CORRIGIDA) ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Larymb" width="100">
            <h3 style="margin-top: 10px;">Agente de IA Larymb.v1</h3>
            <div style="color: #00ff41; font-size: 0.8em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegação ÚNICA
    if st.button("🏠 Início", use_container_width=True, key="btn_inicio"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="btn_conv"): st.session_state.page = "Conversas"
    if st.button("⭐ Favoritos", use_container_width=True, key="btn_fav"): st.session_state.page = "Favoritos"
    if st.button("🕒 Histórico", use_container_width=True, key="btn_hist"): st.session_state.page = "Histórico"
    if st.button("⚙️ Configurações", use_container_width=True, key="btn_conf"): st.session_state.page = "Configurações"
    
    st.markdown("---")
    
    # Histórico de Conversas (Área de scroll)
    st.subheader("Histórico")
    with st.container(height=300):
        st.write("Suas conversas salvas aparecerão aqui.")
    
    st.markdown("---")
    
    # Rodapé de Suporte
    st.markdown("""
        <div style="font-size: 0.85em; color: #ccc;">
            <p><strong>Desenvolvido para auxiliar.</strong><br>
            IA pode cometer erros. Sempre verifique as respostas.</p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("✉️ Email para Suporte", "mailto:seuemail@exemplo.com", use_container_width=True)

# --- ÁREA PRINCIPAL ---
if "page" not in st.session_state: st.session_state.page = "Início"

if st.session_state.page == "Início":
    st.markdown('<div class="main-title">Como posso te ajudar hoje?</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Seu guia inteligente para respostas, explicações e referências.</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.button("Respostas Inteligentes", use_container_width=True, key="a1")
    with col2: st.button("Explicações Detalhadas", use_container_width=True, key="a2")
    with col3: st.button("Referências Confiáveis", use_container_width=True, key="a3")
    with col4: st.button("Rápido e Eficiente", use_container_width=True, key="a4")
