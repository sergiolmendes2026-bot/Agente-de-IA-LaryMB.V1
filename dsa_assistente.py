import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS Profissional ---
st.markdown("""
    <style>
    .stApp { background-color: #0d0f14; color: #ffffff; font-family: 'Inter', sans-serif; }
    .card { background-color: #161a22; border: 1px solid #374151; border-radius: 16px; padding: 20px; text-align: center; }
    .sidebar-card { background-color: #161a22; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
""", unsafe_allow_html=True)

# --- PROMPT (Estruturado em lista para evitar erros de sintaxe) ---
prompt_list = [
    "Você é o Agente de IA LaryMB.V2, um assistente multifuncional.",
    "Missão: Resolver dúvidas, ensinar conceitos, organizar informações e auxiliar na tomada de decisões.",
    "Prioridade: 1. Segurança, 2. Precisão, 3. Clareza, 4. Organização.",
    "Padrão de resposta: Resumo, Explicação, Passo a Passo, Boas Práticas, Observações.",
    "Formatação: Utilize títulos, listas, tabelas e código formatado."
]
CUSTOM_PROMPT = "\n".join(prompt_list)

# --- ESTADO DA PÁGINA ---
if 'page' not in st.session_state:
    st.session_state.page = "Início"

# --- SIDEBAR (Com botões funcionais) ---
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
    
    st.markdown("<div class='sidebar-card'><h4>Precisa de ajuda?</h4><p>IA pode cometer erros. Sempre verifique as respostas.</p></div>", unsafe_allow_html=True)
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

# --- INTERFACE PRINCIPAL ---
if st.session_state.page == "Início":
    st.markdown("<h1 style='text-align: center;'>Como posso te ajudar hoje?</h1>", unsafe_allow_html=True)
    
    # Grid de Cards
    cols = st.columns(4)
    features = ["Respostas", "Explicações", "Referências", "Rápido"]
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<div class='card'><b>{features[i]}</b></div>", unsafe_allow_html=True)

    # Lógica de Chat na página de início
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Digite sua dúvida aqui..."):
        if not api_key:
            st.error("Insira a API Key na barra lateral.")
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

elif st.session_state.page != "Início":
    st.header(f"Página: {st.session_state.page}")
    st.write("Conteúdo em desenvolvimento...")
