import streamlit as st
import pandas as pd
import requests
import datetime

# --- CONFIGURAÇÃO DA PÁGINA (ESTILO MONITORAMENTO) ---
st.set_page_config(
    page_title="Enterprise Threat Intelligence Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CUSTOMIZADA (TEMA DARK / DATADOG STYLE) ---
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-top: 3px solid #3b82f6;
        padding: 16px;
        border-radius: 6px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 700;
        margin-top: 4px;
    }
    .status-badge {
        background-color: rgba(34, 197, 94, 0.15);
        color: #22c55e;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 13px;
        border: 1px solid rgba(34, 197, 94, 0.3);
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
        st.sidebar.markdown("### 🔒 Secure Gateway")
        senha_input = st.sidebar.text_input("Palavra-passe corporativa:", type="password")
        if st.sidebar.button("🔓 Autenticar Acesso", use_container_width=True):
            if senha_input == "ciber2026":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.sidebar.error("❌ Credencial inválida.")
        return False
    return True

if not verificar_autenticacao():
    st.title("⚡ Enterprise Threat Intelligence")
    st.warning("⚠️ Acesso restrito. Introduza a chave corporativa de autenticação na barra lateral (`ciber2026`).")
    st.stop()

# --- CARREGAR DADOS DO SUPABASE ---
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
        st.error(f"Erro de conexão com o banco de dados: {e}")
        return pd.DataFrame()

# --- CABEÇALHO DO PAINEL ---
st.markdown("### ⚡ Supabase Observability & Threat Telemetry")
st.markdown("Painel de controlo corporativo em tempo real integrado ao cluster de produção.")

df_dados = carregar_dados()

if not df_dados.empty:
    # --- BARRA LATERAL DE FILTROS E EXPORTAÇÃO ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Filtros de Fleet")
    
    # Filtro por Operador
    operadores_disponiveis = ["Todos"] + list(df_dados["nome_operador"].dropna().unique()) if "nome_operador" in df_dados.columns else ["Todos"]
    operador_selecionado = st.sidebar.selectbox("Filtrar por Operador:", operadores_disponiveis)
    if operador_selecionado != "Todos":
        df_dados = df_dados[df_dados["nome_operador"] == operador_selecionado]

    # Filtro por Departamento (caso a coluna exista na tabela)
    if "departamento" in df_dados.columns:
        departamentos_disponiveis = ["Todos"] + list(df_dados["departamento"].dropna().unique())
        departamento_selecionado = st.sidebar.selectbox("Filtrar por Departamento:", departamentos_disponiveis)
        if departamento_selecionado != "Todos":
            df_dados = df_dados[df_dados["departamento"] == departamento_selecionado]

    # --- MÉTRICAS EXECUTIVAS (CARDS) ---
    total_registros = len(df_dados)
    operadores_unicos = df_dados["nome_operador"].nunique() if "nome_operador" in df_dados.columns else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Queries (Fleet)</div>
                <div class="metric-value">{total_registros}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        ultima_data = "N/A"
        if "data_hora" in df_dados.columns and not df_dados["data_hora"].isna().all():
            ultima_data = df_dados["data_hora"].max().strftime("%d/%m/%Y %H:%M")
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Último Evento Registado</div>
                <div class="metric-value" style="font-size: 18px; margin-top: 8px;">{ultima_data}</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Active Operators</div>
                <div class="metric-value">{operadores_unicos}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Database Status</div>
                <div class="metric-value" style="margin-top: 6px;"><span class="status-badge">ONLINE 🟢</span></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- GRÁFICO DE TELEMETRIA TEMPORAL ---
    if "data_hora" in df_dados.columns and not df_dados["data_hora"].isna().all():
        st.subheader("📊 Query Throughput by Timeline")
        df_chart = df_dados.copy()
        df_chart["data_dia"] = df_chart["data_hora"].dt.date
        counts_por_dia = df_chart.groupby("data_dia").size().reset_index(name="quantidade")
        st.bar_chart(counts_por_dia.set_index("data_dia"), color="#3b82f6")

    st.divider()

    # --- TABELA DE LOGS DETALHADA E EXPORTAÇÃO ---
    st.subheader("📋 Query Telemetry Logs & Activity Stream")
    
    col_pesq, col_btn = st.columns([3, 1])
    with col_pesq:
        filtro_pesquisa = st.text_input("🔍 Search Query Logs:", placeholder="Filtrar por termos, operador, departamento ou carimbo temporal...")
    
    if filtro_pesquisa:
        mask = df_dados.astype(str).apply(lambda x: x.str.contains(filtro_pesquisa, case=False)).any(axis=1)
        df_exibicao = df_dados[mask]
    else:
        df_exibicao = df_dados

    # Botão de Download Organizado em Excel / CSV
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_data = df_exibicao.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 Descarregar Excel/CSV",
            data=csv_data,
            file_name=f"relatorio_telemetria_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.dataframe(df_exibicao, use_container_width=True)
else:
    st.info("ℹ️ A aguardar fluxo de dados na base de dados Supabase...")
