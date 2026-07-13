import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v2", layout="wide", page_icon="🤖")

# --- PROMPT DEFINIDO ---
SYSTEM_PROMPT = """
Agente de IA LaryMB.V2
IDENTIDADE
Você é o Agente de IA LaryMB.V2, um assistente de Inteligência Artificial multifuncional... 
(O restante do seu texto continua aqui...)
OBJETIVO FINAL
... entregando respostas claras, organizadas, precisas e adaptadas às necessidades de cada usuário.
"""

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

# --- SIDEBAR E API KEY (Com Session State para não perder o valor) ---
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

with st.sidebar:
    st.markdown("### 🤖 Agente de IA Larymb.v2")
    st.session_state.api_key = st.text_input("Insira sua API Key Groq", type="password", value=st.session_state.api_key)
    st.markdown("---")
    if st.button("🏠 Início"): st.session_state.page = "Início"
    if st.button("💬 Conversas"): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações"): st.session_state.page = "Configurações"

# --- LÓGICA DE NAVEGAÇÃO ---
if "page" not in st.session_state: st.session_state.page = "Início"

if st.session_state.page == "Início":
    st.title("Como posso te ajudar hoje?")
    
    # Exibir histórico
    conn = sqlite3.connect('historico_chat.db')
    mensagens = conn.execute("SELECT role, content FROM chats ORDER BY id ASC").fetchall()
    conn.close()

    for role, content in mensagens:
        with st.chat_message(role):
            st.markdown(content)
            
    if prompt := st.chat_input("Qual sua dúvida?"):
        if not st.session_state.api_key:
            st.error("Insira sua API Key na lateral.")
        else:
            salvar_mensagem("user", prompt)
            
            # Construir contexto: Sistema + Histórico + Novo Prompt
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for role, content in mensagens:
                messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": prompt})
            
            # Chamada da API
            try:
                client = Groq(api_key=st.session_state.api_key)
                response = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile"
                )
                resposta = response.choices[0].message.content
                salvar_mensagem("assistant", resposta)
                st.rerun()
            except Exception as e:
                st.error(f"Erro na API: {e}")

elif st.session_state.page == "Configurações":
    st.header("⚙️ Configurações")
    if st.button("Limpar Histórico de Chat"):
        conn = sqlite3.connect('historico_chat.db')
        conn.execute("DELETE FROM chats")
        conn.commit()
        conn.close()
        st.rerun()
