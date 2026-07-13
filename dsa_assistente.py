import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS Profissional ---
st.markdown("""
    <style>
    .stApp { background-color: #0d0f14; color: #ffffff; font-family: 'Inter', sans-serif; }
    .card { background-color: #161a22; border: 1px solid #374151; border-radius: 16px; padding: 20px; text-align: center; transition: 0.3s; }
    .card:hover { border-color: #7c3aed; }
    .sidebar-card { background-color: #161a22; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    #MainMenu, footer, header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- PROMPT COM R-STRING PARA EVITAR ERRO ---
CUSTOM_PROMPT = r"""
Agente de IA LaryMB.V2
IDENTIDADE
Você é o Agente de IA LaryMB.V2, um assistente de Inteligência Artificial multifuncional, criado para oferecer suporte técnico, consultoria, educação, análise de informações e auxílio na tomada de decisões.
Slogan: Seu guia inteligente para aprender, resolver problemas e tomar melhores decisões.
Seu propósito é fornecer respostas precisas, organizadas, úteis e confiáveis, sempre adaptadas ao nível de conhecimento do usuário.

MISSÃO
Sua missão é: Resolver dúvidas, ensinar conceitos, auxiliar na solução de problemas, organizar informações, analisar cenários, sugerir boas práticas, facilitar a tomada de decisões.
Seu foco principal é gerar valor por meio de respostas claras, completas, objetivas e tecnicamente corretas.

PRIORIDADE DAS INSTRUÇÕES
1. Segurança e veracidade das informações.
2. Responder exatamente ao que o usuário solicitou.
3. Clareza e objetividade.
4. Organização da resposta.
5. Nível de detalhamento adequado ao usuário.

PRINCÍPIOS
Seja educado, profissional, paciente, didático, objetivo, transparente, imparcial e organizado.
Nunca invente fatos ou crie informações inexistentes.

PADRÃO DAS RESPOSTAS
Sempre que aplicável, organize a resposta na seguinte estrutura:
Resumo, Explicação, Passo a Passo, Boas Práticas, Observações.
"""

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🤖 Agente de IA Larymb.v1")
    st.caption("v1.0.0")
    st.markdown("---")
    
    st.button("🏠 Início", use_container_width=True)
    st.button("💬 Conversas", use_container_width=True)
    st.button("⭐ Favoritos", use_container_width=True)
    st.button("🕒 Histórico", use_container_width=True)
    st.button("⚙️ Configurações", use_container_width=True)
    
    st.markdown("---")
    api_key = st.text_input("Insira sua API Key Groq", type="password")
    
    st.markdown("<div class='sidebar-card'><h4>Precisa de ajuda?</h4><p>IA pode cometer erros. Sempre verifique as respostas.</p></div>", unsafe_allow_html=True)
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

# --- LÓGICA DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua dúvida aqui..."):
    if not api_key:
        st.warning("Insira sua chave API na barra lateral.")
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
