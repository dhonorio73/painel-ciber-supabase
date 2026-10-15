import streamlit as st
import pandas as pd
import requests
import datetime
import io
import time

# --- CONFIGURAÇÃO PREMIUM DA PÁGINA ---
st.set_page_config(
    page_title="Enterprise Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS PREMIUM) ---
st.markdown("""
<style>
    /* Customização de Cards de Métricas */
    .metric-card {
        background-color: #1e293b;
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 10px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 28px;
        font-weight: 700;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- CREDENCIAIS SEGURAS DO SUPABASE ---
# Configurado para buscar no st.secrets (garanta que o secrets.toml esteja configurado)
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    # Fallback de segurança ou aviso caso o secrets não esteja configurado localmente
    SUPABASE_URL = ""
    SUPABASE_KEY = ""

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- SISTEMA DE AUTENTICAÇÃO CORPORATIVA ---
def verificar_autenticacao():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
        
    if not st.session_state.autenticado:
        st.sidebar.markdown("### 🔒 Acesso Restrito")
        senha_input = st.sidebar.text_input("Palavra-passe corporativa:", type="password")
        
        if st.sidebar.button("🔓 Autenticar", use_container_width=True):
            if senha_input == "ciber2026":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.sidebar.error("❌ Palavra-passe incorreta.")
        return False
    return True

if not verificar_autenticacao():
    st.title("🛡️ Enterprise Threat Intelligence Dashboard")
    st.warning("⚠️ Autenticação necessária. Introduza a chave corporativa de acesso na barra lateral (`ciber2026`).")
    st.stop()

# --- INTEGRAÇÃO ROBUSTA COM SUPABASE ---
@st.cache_data(ttl=5)
def carregar_dados():
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("⚠️ As credenciais do Supabase não foram encontradas nas configurações de segredos.")
        return pd.DataFrame()
        
    endpoint = f"{SUPABASE_URL}/rest/v1/historico_pesquisas?select=*&order=id.desc"
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                if "data_hora" in df.columns:
                    df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
                return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao conectar com o Supabase: {e}")
        return pd.DataFrame()
