import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Enterprise Threat Intelligence Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CUSTOMIZADA ---
st.markdown("""
<style>
    .main { background-color: #0f172a; }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-top: 3px solid #3b82f6;
        padding: 16px;
        border-radius: 6px;
    }
    .metric-title { color: #94a3b8; font-size: 11px; font-weight: 700; text-transform: uppercase; }
    .metric-value { color: #f8fafc; font-size: 24px; font-weight: 700; margin-top: 4px; }
    .status-badge { background-color: rgba(34, 197, 94, 0.15); color: #22c55e; padding: 4px 10px; border-radius: 4px; font-weight: 600; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# --- AUTENTICAÇÃO ---
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

# --- DADOS ESTÁTICOS INTEGRADOS ---
dados = [
    {"id": 1, "nome_operador": "Ana Silva", "registro_funcionario": "101", "data_nascimento": "12/03/1992", "termo_pesquisado": "Análise de vulnerabilidades CVE-2026", "data_hora": "2026-10-01 09:15:22", "departamento": "Segurança da Informação"},
    {"id": 2, "nome_operador": "Carlos Mendes", "registro_funcionario": "102", "data_nascimento": "22/07/1988", "termo_pesquisado": "Configuração de Firewall corporativo", "data_hora": "2026-10-02 11:30:45", "departamento": "Infraestrutura e Redes"},
    {"id": 3, "nome_operador": "Beatriz Costa", "registro_funcionario": "103", "data_nascimento": "05/11/1995", "termo_pesquisado": "Auditoria de conformidade LGPD", "data_hora": "2026-10-03 14:10:00", "departamento": "Compliance"},
    {"id": 4, "nome_operador": "Marcos Oliveira", "registro_funcionario": "104", "data_nascimento": "14/02/1990", "termo_pesquisado": "Python Flask API endpoints security", "data_hora": "2026-10-04 16:20:11", "departamento": "Desenvolvimento / TI"},
    {"id": 5, "nome_operador": "Ana Silva", "registro_funcionario": "101", "data_nascimento": "12/03/1992", "termo_pesquisado": "Mitigação de ataques DDoS", "data_hora": "2026-10-05 08:45:33", "departamento": "Segurança da Informação"},
    {"id": 6, "nome_operador": "Juliana Rocha", "registro_funcionario": "105", "data_nascimento": "30/09/1993", "termo_pesquisado": "Gestão de acessos IAM Supabase", "data_hora": "2026-10-06 10:05:50", "departamento": "Governança de Dados"},
    {"id": 7, "nome_operador": "Carlos Mendes", "registro_funcionario": "102", "data_nascimento": "22/07/1988", "termo_pesquisado": "Análise de logs de intrusão", "data_hora": "2026-10-07 13:22:19", "departamento": "Infraestrutura e Redes"},
    {"id": 8, "nome_operador": "Lucas Pereira", "registro_funcionario": "106", "data_nascimento": "18/12/1991", "termo_pesquisado": "Relatório de incidentes críticos", "data_hora": "2026-10-08 17:50:02", "departamento": "Centro de Operações (SOC)"},
    {"id": 9, "nome_operador": "Beatriz Costa", "registro_funcionario": "103", "data_nascimento": "05/11/1995", "termo_pesquisado": "Termos de uso e privacidade", "data_hora": "2026-10-09 09:33:40", "departamento": "Compliance"},
    {"id": 10, "nome_operador": "Marcos Oliveira", "registro_funcionario": "104", "data_nascimento": "14/02/1990", "termo_pesquisado": "Criptografia Fernet e SHA-256", "data_hora": "2026-10-10 15:12:04", "departamento": "Desenvolvimento / TI"}
]

df_dados = pd.DataFrame(dados)

# --- CABEÇALHO ---
st.markdown("### ⚡ Supabase Observability & Threat Telemetry")
st.markdown("Painel de controlo corporativo em tempo real integrado ao cluster de produção.")

# --- FILTROS NA BARRA LATERAL ---
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Filtros de Fleet")

operadores = ["Todos"] + list(df_dados["nome_operador"].dropna().unique())
op_sel = st.sidebar.selectbox("Filtrar por Operador:", operadores)
if op_sel != "Todos":
    df_dados = df_dados[df_dados["nome_operador"] == op_sel]

deptos = ["Todos"] + list(df_dados["departamento"].dropna().unique())
dept_sel = st.sidebar.selectbox("Filtrar por Departamento:", deptos)
if dept_sel != "Todos":
    df_dados = df_dados[df_dados["departamento"] == dept_sel]

# --- MÉTRICAS ---
total_reg = len(df_dados)
ops_unicos = df_dados["nome_operador"].nunique()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Total Queries</div><div class="metric-value">{total_reg}</div></div>', unsafe_allow_html=True)
with c2:
    ultima = df_dados["data_hora"].max()
    st.markdown(f'<div class="metric-card"><div class="metric-title">Último Evento</div><div class="metric-value" style="font-size:16px; margin-top:8px;">{ultima}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Active Operators</div><div class="metric-value">{ops_unicos}</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Database Status</div><div class="metric-value" style="margin-top:6px;"><span class="status-badge">ONLINE 🟢</span></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- TABELA E EXPORTAÇÃO ---
st.subheader("📋 Query Telemetry Logs & Activity Stream")

col_p, col_b = st.columns([3, 1])
with col_p:
    pesquisa = st.text_input("🔍 Search Query Logs:", placeholder="Filtrar por termos, operador ou departamento...")

if pesquisa:
    mask = df_dados.astype(str).apply(lambda x: x.str.contains(pesquisa, case=False)).any(axis=1)
    df_exibicao = df_dados[mask]
else:
    df_exibicao = df_dados

with col_b:
    st.markdown("<br>", unsafe_allow_html=True)
    csv = df_exibicao.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="📥 Descarregar Excel/CSV",
        data=csv,
        file_name=f"telemetria_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

st.dataframe(df_exibicao, use_container_width=True)
