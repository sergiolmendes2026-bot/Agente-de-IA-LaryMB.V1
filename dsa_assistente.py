import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS PARA DARK THEME E LAYOUT ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { font-size: 2.5em; font-weight: bold; text-align: center; margin-top: 20px; }
    .sub-title { text-align: center; color: #888; margin-bottom: 30px; }
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
    
    # CAMPO DA API KEY (AQUI!)
    st.caption("Configurações")
    api_key = st.text_input("Insira sua API Key Groq", type="password", key="api_key_input")
    
    st.markdown("---")
    st.markdown("IA pode cometer erros. Sempre verifique as respostas.")
    st.link_button("✉️ Email para Suporte", "mailto:seuemail@exemplo.com", use_container_width=True)

# --- LÓGICA DE NAVEGAÇÃO ---
if "page" not in st.session_state: st.session_state.page = "Início"

# --- PÁGINA DE INÍCIO (COM CHAT) ---
if st.session_state.page == "Início":
    st.markdown('<div class="main-title">Como posso te ajudar hoje?</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Seu guia inteligente para respostas e referências.</div>', unsafe_allow_html=True)
    
    # Inicializa chat
    if "messages" not in st.session_state: st.session_state.messages = []
    
    # Exibe histórico
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # CAMPO PARA DIGITAR PERGUNTAS (AQUI!)
    if prompt := st.chat_input("Qual sua dúvida?"):
        if not api_key:
            st.error("Por favor, insira sua API Key na barra lateral.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama-3.3-70b-versatile"
                )
                resposta = response.choices[0].message.content
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})

# --- OUTRAS PÁGINAS ---
elif st.session_state.page == "Conversas":
    st.header("💬 Conversas")
    st.write("Histórico de conversas em desenvolvimento.")
