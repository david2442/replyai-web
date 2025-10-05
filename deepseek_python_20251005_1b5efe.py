import streamlit as st
import openai
import random
import time

# Configuração da página
st.set_page_config(
    page_title="ReplyAI - Seu Assistente",
    page_icon="🤖",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .chat-user {
        background: #E3F2FD;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1E88E5;
    }
    .chat-ai {
        background: #F5F5F5;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-title">🤖 ReplyAI Online</h1>', unsafe_allow_html=True)
st.markdown("### 💬 Converse com sua IA pessoal na nuvem!")

# Sidebar com configurações
with st.sidebar:
    st.title("⚙️ Configurações")
    
    # Input da API Key
    api_key = st.text_input(
        "🔑 Sua OpenAI API Key:",
        type="password",
        placeholder="sk-...",
        help="Obtenha em: https://platform.openai.com/api-keys"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Status do Sistema")
    st.success("✅ Online na nuvem")
    st.info("🌐 Acessível globalmente")
    
    st.markdown("---")
    st.markdown("### 💡 Como usar:")
    st.write("1. Cole sua API Key")
    st.write("2. Digite sua mensagem")
    st.write("3. Clique Enter")
    st.write("4. Compartilhe o link!")

# Sistema de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar histórico
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-user"><strong>👤 Você:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-ai"><strong>🤖 ReplyAI:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Input do usuário
user_input = st.chat_input("Digite sua mensagem aqui...")

if user_input:
    # Adicionar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Verificar se tem API key
    if not api_key:
        st.error("❌ Por favor, cole sua OpenAI API Key na sidebar")
        st.stop()
    
    try:
        openai.api_key = api_key
        
        with st.spinner("🤖 ReplyAI está pensando..."):
            # Gerar resposta
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é a ReplyAI, um assistente útil e amigável. Responda no mesmo idioma do usuário."}
                ] + [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages],
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            
        # Adicionar resposta da IA
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Recarregar para mostrar nova mensagem
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")

# Botão para limpar chat
if st.button("🧹 Limpar Conversa", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🚀 <strong>ReplyAI Cloud</strong> - Disponível 24/7 na nuvem</p>
    <p>📧 Compartilhe este link com amigos e familiares!</p>
</div>
""", unsafe_allow_html=True)