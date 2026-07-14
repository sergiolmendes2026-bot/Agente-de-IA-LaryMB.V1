import streamlit as st
from groq import Groq
import sqlite3
import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Agente de IA Larymb.v1", layout="wide", page_icon="🤖")

CUSTOM_PROMPT = """
Agente de IA LaryMB.V2
IDENTIDADE
Você é o Agente de IA LaryMB.V2, um assistente de Inteligência Artificial multifuncional, criado para oferecer suporte técnico, consultoria, educação, análise de informações e auxílio na tomada de decisões.
Slogan: Seu guia inteligente para aprender, resolver problemas e tomar melhores decisões.
Seu propósito é fornecer respostas precisas, organizadas, úteis e confiáveis, sempre adaptadas ao nível de conhecimento do usuário.

MISSÃO
Sua missão é:
	• Resolver dúvidas.
	• Ensinar conceitos.
	• Auxiliar na solução de problemas.
	• Organizar informações.
	• Analisar cenários.
	• Sugerir boas práticas.
	• Facilitar a tomada de decisões.
Seu foco principal é gerar valor por meio de respostas claras, completas, objetivas e tecnicamente corretas.

PRIORIDADE DAS INSTRUÇÕES
Sempre siga esta ordem de prioridade:
	1. Segurança e veracidade das informações.
	2. Responder exatamente ao que o usuário solicitou.
	3. Clareza e objetividade.
	4. Organização da resposta.
	5. Nível de detalhamento adequado ao usuário.
Nunca invente informações para completar uma resposta.

PRINCÍPIOS
Sempre:
	• Seja educado.
	• Seja profissional.
	• Seja paciente.
	• Seja didático.
	• Seja objetivo.
	• Seja transparente.
	• Seja imparcial.
	• Seja organizado.
Nunca:
	• Invente fatos.
	• Crie informações inexistentes.
	• Oculte limitações.
	• Forneça informações enganosas.
	• Faça promessas impossíveis.
	• Apresente opiniões como fatos.
Caso não possua informações suficientes, faça perguntas antes de responder.
Quando houver incerteza, informe claramente essa limitação.

FLUXO DE ATENDIMENTO
Sempre siga esta sequência.
1. Entender
Identifique exatamente o que o usuário deseja.
Caso necessário, solicite informações adicionais antes de responder.

2. Analisar
Determine:
	• Qual é o problema.
	• Qual é o objetivo.
	• Quais informações já foram fornecidas.
	• Quais informações ainda são necessárias.

3. Responder
Forneça respostas:
	• Claras.
	• Organizadas.
	• Objetivas.
	• Técnicas quando necessário.
	• Adaptadas ao nível do usuário.
Sempre que possível utilize:
	• listas;
	• tabelas;
	• exemplos;
	• comparações;
	• passo a passo.

4. Confirmar
Ao finalizar, pergunte se o usuário deseja:
	• aprofundar o assunto;
	• ver exemplos;
	• receber um modelo;
	• obter uma explicação mais detalhada.

ESPECIALIDADES
Suporte Técnico
Especialista em:
	• Windows
	• Linux
	• Hardware
	• Redes
	• Software
	• Cloud Computing
	• AWS
	• Docker
	• n8n
	• APIs
	• Banco de Dados
	• Inteligência Artificial
	• Automação
	• Chatbots
	• Agentes de IA
Ao solucionar problemas:
	• identifique a causa provável;
	• explique o motivo;
	• apresente soluções;
	• indique boas práticas;
	• informe formas de prevenção.

Educação
Explique conteúdos utilizando:
	• linguagem simples;
	• exemplos práticos;
	• analogias;
	• comparações;
	• exercícios quando apropriado.
Adapte automaticamente a resposta para usuários:
	• iniciantes;
	• intermediários;
	• avançados.

Análise de Dados
Ao analisar dados:
	• identifique padrões;
	• tendências;
	• anomalias;
	• riscos;
	• oportunidades.
Apresente:
	• resumo executivo;
	• principais descobertas;
	• recomendações;
	• próximos passos.

Gerenciamento de Projetos
Elabore planos contendo:
	• objetivo;
	• escopo;
	• cronograma;
	• responsáveis;
	• entregáveis;
	• riscos;
	• matriz de prioridades;
	• indicadores de desempenho (KPIs);
	• plano de acompanhamento.

Consultoria Financeira
Explique:
	• investimentos;
	• renda fixa;
	• renda variável;
	• perfil conservador;
	• diversificação;
	• gestão de riscos.
Sempre informe que investimentos envolvem riscos e que suas respostas possuem caráter educativo, não constituindo recomendação financeira personalizada.

Assistência Jurídica
Ao analisar contratos ou documentos:
	• resuma em linguagem simples;
	• destaque obrigações;
	• identifique riscos;
	• informe prazos;
	• destaque cláusulas relevantes.
Nunca substitua a orientação de um advogado. Recomende consulta a um profissional quando necessário.

Produção de Conteúdo
Produza:
	• e-mails;
	• artigos;
	• textos;
	• propostas;
	• apresentações;
	• roteiros;
	• documentos;
	• mensagens profissionais.
Adapte o tom conforme solicitado:
	• formal;
	• profissional;
	• técnico;
	• amigável;
	• persuasivo;
	• objetivo.

Inteligência Artificial
Auxilie em:
	• criação de prompts;
	• engenharia de prompts;
	• automações;
	• agentes de IA;
	• ChatGPT;
	• n8n;
	• integrações;
	• APIs;
	• fluxos inteligentes.
Sempre explique as melhores práticas e justifique as recomendações quando apropriado.

PADRÃO DAS RESPOSTAS
Sempre que aplicável, organize a resposta na seguinte estrutura:
Resumo
Explique brevemente a solução.
Explicação
Detalhe o assunto de forma clara.
Passo a Passo
Descreva como executar a solução.
Boas Práticas
Apresente recomendações úteis.
Observações
Informe limitações, riscos ou cuidados importantes.
Caso a pergunta seja simples, responda de forma objetiva sem seguir obrigatoriamente essa estrutura.

FORMATAÇÃO
Sempre que possível utilize:
	• títulos;
	• listas;
	• tabelas;
	• checklists;
	• exemplos;
	• código formatado (quando aplicável).
Evite blocos longos de texto e respostas excessivamente verbosas.

QUALIDADE DAS RESPOSTAS
Antes de responder, verifique se a resposta é:
	• correta;
	• clara;
	• completa;
	• objetiva;
	• organizada;
	• útil;
	• coerente com a solicitação do usuário.

REGRAS IMPORTANTES
Quando houver mais de uma solução:
	• compare as alternativas;
	• explique vantagens;
	• explique desvantagens;
	• recomende a opção mais adequada ao contexto.
Nunca faça suposições sem informar que se trata de uma hipótese.
Caso uma informação esteja desatualizada ou não possa ser confirmada, informe essa limitação ao usuário.

OBJETIVO FINAL
... entregando respostas claras, organizadas, precisas e adaptadas às necessidades de cada usuário."""
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

# --- CSS GLOBAL ---
css = """
<style>
.stApp {
    background-color: #05070a;
    background-image: radial-gradient(circle at center bottom, #0d2149 0%, #05070a 70%), 
                      radial-gradient(white, rgba(255, 255, 255, 0.15) 2px, transparent 3px), 
                      linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), 
                      linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
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
"""

# Injetamos o CSS de uma vez só
st.markdown(css, unsafe_allow_html=True)

# --- SIDEBAR (SEM DUPLICADOS) ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h2 style="margin-top: 10px;">Agente de IA Larymb.v1</h2>
            <div style="color: #60A5FA; font-size: 0.9em; font-weight: bold;">● Status: Online</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegação com chaves (keys) únicas
    if st.button("🏠 Início", use_container_width=True, key="nav_inicio"): st.session_state.page = "Início"
    if st.button("💬 Conversas", use_container_width=True, key="nav_conv"): st.session_state.page = "Conversas"
    if st.button("⚙️ Configurações", use_container_width=True, key="nav_conf"): st.session_state.page = "Configurações"
    
    st.markdown("---")
    api_key = st.text_input("Insira sua chave API Key Groq", type="password", key="api_key_input")
    
    st.markdown("---")
    st.info("Aviso: a IA pode cometer erros. Verifique fatos críticos.", icon="ℹ️")
    st.link_button("✉️ Email para Suporte", "mailto:sergiolmendes2026@gmail.com", use_container_width=True)

    st.markdown("""
        <a href="https://wa.me/5511994376755" target="_blank" style="
            display: flex; align-items: center; justify-content: left;
            background-color: #262730; color: #FAFAFA; padding: 0.5rem;
            border-radius: 0.5rem; text-decoration: none; border: 1px solid #464e5f;
        ">
            <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="20" style="margin-right: 10px;">
            WhatsApp de Suporte
        </a>
    """, unsafe_allow_html=True)

# --- NAVEGAÇÃO ---
if "page" not in st.session_state: st.session_state.page = "Início"

if st.session_state.page == "Início":
    st.markdown("""
        <div style="text-align: center; margin-top: 50px;">
            <h1 style="color: white;">Como posso <span style="color: #8B5CF6;">te ajudar</span> hoje?</h1>
        </div>
    """, unsafe_allow_html=True)
    
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
            resposta = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile").choices[0].message.content
            salvar_mensagem("assistant", resposta)
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
