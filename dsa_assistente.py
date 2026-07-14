import streamlit as st
from groq import Groq
import sqlite3
import datetime
import textwrap

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

# --- CSS GLOBAL ---
css = textwrap.dedent("""
<style>
.stApp {
    background-color: #05070a;
    background-image: radial-gradient(circle at center bottom, #0d2149 0%, #05070a 70%), radial-gradient(white, rgba(255, 255, 255, 0.15) 2px, transparent 3px), linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background-color: #4B0082 !important;
    border-right: 1px solid #2e303a;
    padding-top: 2rem;
}
[data-testid="stSidebar"] * {
    color: #FAFAFA !important;
}
</style>
""")
st.markdown(css, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats 
                  (id INTEGER PRIMARY KEY, role TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def salvar_mensagem(role, content):
    conn = sqlite3.connect('historico_chat.db')
    c = conn.cursor()
    c.execute("INSERT INTO chats (role, content, timestamp) VALUES (?, ?, ?)",
              (role, content, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

init_db()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h2 style="margin-top: 10px;">Agente de IA Larymb.v1</h2>
            <div class="status-verde" style="font-size: 0.9em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🏠 Início", use_container_width=True, key="nav_inicio"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="nav_conv"): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True, key="nav_conf"): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua chave API Key Groq", type="password", key="api_key_input")
    
    st.markdown("---")
    st.info("Aviso: IA pode gerar respostas imprecisas. incompletas ou erradas. Sempre verifique informações críticas antes de confiar totalmente.", icon="ℹ️")
    
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)
    st.link_button("💬 WhatsApp de Suporte", "https://wa.me/5511994376755", use_container_width=True)

# --- NAVEGAÇÃO ---
if "page" not in st.session_state: st.session_state.page = "Início"

if st.session_state.page == "Início":
    st.markdown('<div style="text-align: center; margin-top: 50px;"><h1>Como posso <span style="color: #8B5CF6;">te ajudar</span> hoje?</h1></div>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('historico_chat.db')
    mensagens = conn.cursor().execute("SELECT role, content FROM chats ORDER BY id ASC").fetchall()
    conn.close()
    
    for role, content in mensagens:
        with st.chat_message(role): st.markdown(content)
            
    if prompt := st.chat_input("Qual sua dúvida?"):
        if not api_key:
            st.error("Insira sua API Key na lateral.")
        else:
            salvar_mensagem("user", prompt)
            client = Groq(api_key=api_key)
            try:
                resposta = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile").choices[0].message.content
                salvar_mensagem("assistant", resposta)
            except Exception as e:
                st.error(f"Erro na API: {e}")
            st.rerun()

elif st.session_state.page == "Conversas":
    st.header("💬 Conversas")
elif st.session_state.page == "Configurações":
    st.header("⚙️ Configurações")
    if st.button("Limpar Histórico", key="btn_limpar"):
        conn = sqlite3.connect('historico_chat.db')
        conn.cursor().execute("DELETE FROM chats")
        conn.commit()
        conn.close()
        st.rerun()
