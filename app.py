import streamlit as st
import pandas as pd
import requests
import datetime

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
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
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

# --- CORPO PRINCIPAL DO DASHBOARD ---
st.title("🛡️ Enterprise Threat Intelligence Dashboard")
st.markdown("Painel avançado de telemetria, monitoramento e registo integrado ao Supabase.")

# Carregar os dados
df_dados = carregar_dados()

if not df_dados.empty:
    # --- BARRA LATERAL DE FILTROS AVANÇADOS ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Filtros de Telemetria")
    
    operadores_disponiveis = ["Todos"] + list(df_dados["nome_operador"].dropna().unique()) if "nome_operador" in df_dados.columns else ["Todos"]
    operador_selecionado = st.sidebar.selectbox("Filtrar por Operador:", operadores_disponiveis)
    
    if operador_selecionado != "Todos":
        df_dados = df_dados[df_dados["nome_operador"] == operador_selecionado]

    # --- MÉTRICAS DE RESUMO EXECUTIVO ---
    total_registros = len(df_dados)
    operadores_unicos = df_dados["nome_operador"].nunique() if "nome_operador" in df_dados.columns else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total de Registros</div>
                <div class="metric-value">{total_registros}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        ultima_data = "N/A"
        if "data_hora" in df_dados.columns and not df_dados["data_hora"].isna().all():
            ultima_data = df_dados["data_hora"].max().strftime("%d/%m/%Y %H:%M")
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Última Atividade</div>
                <div class="metric-value">{ultima_data}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Operadores Ativos</div>
                <div class="metric-value">{operadores_unicos}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Estado do Sistema</div>
                <div class="metric-value" style="color: #22c55e; font-size: 24px;">Operacional 🟢</div>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- GRÁFICO DE ATIVIDADE TEMPORAL ---
    if "data_hora" in df_dados.columns and not df_dados["data_hora"].isna().all():
        st.subheader("📈 Telemetria de Atividade por Período")
        df_chart = df_dados.copy()
        df_chart["data_dia"] = df_chart["data_hora"].dt.date
        counts_por_dia = df_chart.groupby("data_dia").size().reset_index(name="quantidade")
        st.bar_chart(counts_por_dia.set_index("data_dia"), color="#3b82f6")

    # --- TABELA DE DADOS DETALHADA COM BUSCA ---
    st.subheader("📋 Histórico Detalhado de Consultas")
    filtro_pesquisa = st.text_input("🔍 Pesquisa Global nos Registos:", placeholder="Digite para filtrar termos, operadores ou datas...")
    
    if filtro_pesquisa:
        mask = df_dados.astype(str).apply(lambda x: x.str.contains(filtro_pesquisa, case=False)).any(axis=1)
        df_exibicao = df_dados[mask]
    else:
        df_exibicao = df_dados

    st.dataframe(df_exibicao, use_container_width=True)
else:
    st.info("ℹ️ Nenhum dado encontrado na tabela `historico_pesquisas` do Supabase ou aguardando conexão.")
