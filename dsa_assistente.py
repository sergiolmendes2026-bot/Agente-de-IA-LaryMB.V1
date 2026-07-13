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

# --- PROMPT ---
# Mantendo o prompt em variável limpa para evitar erro de sintaxe
CUSTOM_PROMPT = "Você é o Agente de IA LaryMB.V2, um assistente multifuncional focado em suporte técnico, educação e análise. Seja objetivo, organizado e use sempre a estrutura: Resumo, Explicação, Passo a Passo e Observações."

# --- SIDEBAR COM NAVEGAÇÃO ---
with st.sidebar:
    # Nome que faltava
    st.markdown("## 🤖 Agente de IA Larymb.v1")
    st.caption("v1.0.0")
    st.markdown("---")
    
    # Lógica de Navegação
    if st.button("🏠 Início", use_container_width=True):
        st.session_state.pagina = "inicio"
    if st.button("💬 Conversas", use_container_width=True):
        st.session_state.pagina = "conversas"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password")
    
    st.markdown("<div class='sidebar-card'><h4>Precisa de ajuda?</h4><p>IA pode cometer erros. Verifique os dados.</p></div>", unsafe_allow_html=True)

# --- LÓGICA DE NAVEGAÇÃO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# --- INTERFACE PRINCIPAL ---
if st.session_state.pagina == "inicio":
    st.markdown("<h1 style='text-align: center;'>Bem-vindo ao Larymb.v1</h1>", unsafe_allow_html=True)
    # Aqui vai o seu grid de cards original
elif st.session_state.pagina == "conversas":
    st.header("Suas Conversas")
    # Aqui vai a lógica de histórico

# --- LÓGICA DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico apenas se não estiver em "conversas" (ou conforme preferir)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua dúvida aqui..."):
    if not api_key:
        st.error("Insira a API Key na barra lateral.")
        st.stop()
        
    client = Groq(api_key=api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": CUSTOM_PROMPT}] + st.session_state.messages,
            model="llama-3.3-70b-versatile"
        )
        ans = response.choices[0].message.content
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
