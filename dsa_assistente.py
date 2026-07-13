import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS PARA ESTILIZAÇÃO DARK ---
st.markdown("""
    <style>
    .stApp { background-color: #0d0f14; color: #ffffff; font-family: 'Inter', sans-serif; }
    .sidebar-card { background-color: #161a22; padding: 15px; border-radius: 10px; border: 1px solid #374151; margin-top: 20px; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- PROMPT DE SISTEMA ---
CUSTOM_PROMPT = "Você é o Agente de IA LaryMB.V2, um assistente especializado em suporte técnico e educação. Seja organizado, use tabelas e listas."

# --- ESTADO DE NAVEGAÇÃO ---
if 'page' not in st.session_state:
    st.session_state.page = "Início"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🤖 Agente de IA Larymb.v1")
    st.caption("v1.0.0")
    st.markdown("---")
    
    if st.button("🏠 Início", use_container_width=True): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True): st.session_state.page = "Conversas"
    if st.button("⭐ Favoritos", use_container_width=True): st.session_state.page = "Favoritos"
    if st.button("🕒 Histórico", use_container_width=True): st.session_state.page = "Histórico"
    if st.button("⚙️ Configurações", use_container_width=True): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password")
    
    st.markdown("""
    <div class='sidebar-card'>
        <h4 style='color: white; margin-top: 0;'>Precisa de ajuda?</h4>
        <p style='font-size: 0.85em; color: #9ca3af;'>IA pode cometer erros. Sempre verifique as informações.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

# --- RENDERIZAÇÃO DA PÁGINA ---
if st.session_state.page == "Início":
    st.markdown("<h1 style='text-align: center;'>Como posso te ajudar hoje?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9ca3af;'>Seu guia inteligente para respostas, explicações e referências.</p>", unsafe_allow_html=True)
    
    # Lógica de Chat
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Digite sua dúvida aqui..."):
        if not api_key:
            st.error("Por favor, insira sua API Key na lateral.")
            st.stop()
        
        client = Groq(api_key=api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": CUSTOM_PROMPT}] + st.session_state.messages,
                model="llama-3.3-70b-versatile"
            )
            ans = response.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

else:
    st.header(f"Página: {st.session_state.page}")
    st.write("Esta área de navegação está pronta para receber seus dados.")
