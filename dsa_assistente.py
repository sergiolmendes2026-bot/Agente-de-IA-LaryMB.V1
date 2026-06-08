# Estudo de Caso 1 - DSA AI Coder - Criando Seu Assistente de Programação Python, em Python

# Importa módulo para interagir com o sistema operacional
import os

# Importa a biblioteca Streamlit para criar a interface web interativa
import streamlit as st

# Importa a classe Groq para se conectar à API da plataforma Groq e acessar o LLM
from groq import Groq
########################################################################################
 #Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar#
########################################################################################

st.set_page_config(
    page_title="Agente de IA Larymb.v1",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS com estilo pastel azul + lilás e barra lateral prateada
st.markdown(
    """
    <style>
    /* ===== Título principal ===== */
    h1 {
      font-size: 12px; /* bem pequeno */
      font-weight: 600;
      color: #ffffff;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.5); /* sombra discreta */
      margin-bottom: 6px;
    }

    /* ===== Subtítulo ===== */
    h2 {
      font-size: 10px; /* ainda menor */
      font-weight: 500;
      color: #e0e0e0;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
      margin-bottom: 5px;
    }

    /* ===== Texto explicativo ===== */
    p {
      font-size: 9px; /* texto bem reduzido */
      line-height: 1.3;
      color: #dcdcdc;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    /* ===== Input de chat ===== */
    .chat-input {
      width: 100%;
      padding: 6px;
      font-size: 9px;
      border-radius: 6px;
      border: 1px solid #cccccc;
      background-color: #2c2c2c;
      color: #ffffff;
    }

    /* ===== Botões ===== */
    button {
      font-size: 9px;
      font-weight: 500;
      padding: 6px 10px;
      border-radius: 6px;
      background: #00bcd4; /* azul turquesa moderno */
      color: #fff;
      border: none;
      cursor: pointer;
      box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }

    button:hover {
      background: #0097a7; /* azul mais escuro no hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o "Agente de IA LaryMB.V1", um assistente de IA especialista em varios assuntos,. Sua missão é ajudar iniciantes com dúvidas de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
* Identidade e Missão:
    Nome: Agente de IA LaryMB.V1
    Subtítulo: Seu guia inteligente para iniciantes
    Objetivo: Ser acessível, confiável e didático em qualquer área de conhecimento.
* Atendimento ao Cliente: Atue como agente de suporte técnico em software, hardware e redes.
    Responda às dúvidas de forma clara, profissional e empática.
* Treinamento e Educação:-  Explique conceitos em linguagem simples, Use exemplos práticos e analogias para facilitar o aprendizado.
* Planejamento de projetos: Você é um gerente de projetos. Crie um plano detalhado com cronograma, responsáveis, -entregáveis e indicadores de sucesso.

* Consultoria financeira: Você é um consultor financeiro especializado em perfis conservadores. Analise os dados fornecidos e sugira estratégias de investimento de baixo risco, explicando vantagens, desvantagens e possíveis cenários futuros.
* Análise de dados: Você é um analista de dados. Examine o conjunto de dados fornecido e identifique padrões, tendências e riscos. Explique os resultados em linguagem acessível para gestores não técnicos.
* Assistente jurídico : Você é um advogado digital. Resuma os principais pontos deste contrato em linguagem simples, destacando cláusulas de risco, obrigações críticas e pontos que exigem atenção especial.
* Clareza e Precisão: Use linguagem acessível e objetiva. Evite jargões desnecessários. Garanta que as respostas sejam tecnicamente corretas e confiáveis.
* Estilo de Comunicação: Tom amigável e instrutivo. Estruture respostas em listas, tabelas ou passos quando necessário.
 Adapte o nível de detalhe conforme o perfil do usuário (iniciante ou avançado).
* Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    
    # Define o título da barra lateral
    st.title("🤖 Agente de IA Larymb.V1")
    
    # Mostra um texto explicativo sobre o assistente
    st.markdown("Um assistente de IA focado para ajudar iniciantes.")
    
    # Campo para inserir a chave de API da Groq
    groq_api_key = st.text_input(
        "Insira sua API Key Groq", 
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar em suas dúvidas. IA pode cometer erros. Sempre verifique as respostas.")
           
    # Botão de link para enviar e-mail ao suporte da DSA
    st.link_button("✉️ E-mail Para o Suporte no Caso de Dúvidas", "mailto:sergiolmendes2026@gmail.com")

# Título principal do app
st.title("Assitente de IA - Larymb.v1")

# Subtítulo adicional

st.title("Seu guia inteligente para iniciantes")

# Texto auxiliar abaixo do título
st.caption("Faça sua pergunta e obtenha respostas, explicações e referências.")

# Inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variável do cliente Groq como None
client = None

# Verifica se o usuário forneceu a chave de API da Groq
if groq_api_key:
    
    try:
        
        # Cria cliente Groq com a chave de API fornecida
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

# Caso não tenha chave, mas já existam mensagens, mostra aviso
elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Qual sua dúvida ?"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-120b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                dsa_ai_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(dsa_ai_resposta)
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p> Agente de AI Coder - Acessível, confiável e útil para quem está começando.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Obrigado DSA



