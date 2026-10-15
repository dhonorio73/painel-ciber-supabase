import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Enterprise Threat Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DADOS ESTÁTICOS ---
dados = [
    {"id": 1, "nome_operador": "Ana Silva", "registro_funcionario": "101", "data_nascimento": "12/03/1992", "termo_pesquisado": "Análise de vulnerabilidades CVE-2026", "data_hora": "2026-10-01 09:15:22", "departamento": "Segurança da Informação"},
    {"id": 2, "nome_operador": "Carlos Mendes", "registro_funcionario": "102", "data_nascimento": "22/07/1988", "termo_pesquisado": "Configuração de Firewall corporativo", "data_hora": "2026-10-02 11:30:45", "departamento": "Infraestrutura e Redes"},
    {"id": 3, "nome_operador": "Beatriz Costa", "registro_funcionario": "103", "data_nascimento": "05/11/1995", "termo_pesquisado": "Auditoria de conformidade LGPD", "data_hora": "2026-10-03 14:10:00", "departamento": "Compliance"},
    {"id": 4, "nome_operador": "Marcos Oliveira", "registro_funcionario": "104", "data_nascimento": "14/02/1990", "termo_pesquisado": "Python Flask API endpoints security", "data_hora": "2026-10-04 16:20:11", "departamento": "Desenvolvimento / TI"},
    {"id": 5, "nome_operador": "Ana Silva", "registro_funcionario": "101", "data_nascimento": "12/03/1992", "termo_pesquisado": "Mitigação de ataques DDoS", "data_hora": "2026-10-05 08:45:33", "departamento": "Segurança da Informação"},
    {"id": 6, "nome_operador": "Juliana Rocha", "registro_funcionario": "105", "data_nascimento": "30/09/1993", "termo_pesquisado": "Gestão de acessos IAM Supabase", "data_hora": "2026-10-06 10:05:50", "departamento": "Governança de Dados"},
    {"id": 7, "nome_operador": "Carlos Mendes", "registro_funcionario": "102", "data_nascimento": "22/07/1988", "termo_pesquisado": "Relatório de incidentes críticos", "data_hora": "2026-10-07 13:22:19", "departamento": "Infraestrutura e Redes"},
    {"id": 8, "nome_operador": "Lucas Pereira", "registro_funcionario": "106", "data_nascimento": "18/12/1991", "termo_pesquisado": "Centro de Operações (SOC)", "data_hora": "2026-10-08 17:50:02", "departamento": "Centro de Operações (SOC)"},
    {"id": 9, "nome_operador": "Beatriz Costa", "registro_funcionario": "103", "data_nascimento": "05/11/1995", "termo_pesquisado": "Termos de uso e privacidade", "data_hora": "2026-10-09 09:33:40", "departamento": "Compliance"},
    {"id": 10, "nome_operador": "Marcos Oliveira", "registro_funcionario": "104", "data_nascimento": "14/02/1990", "termo_pesquisado": "Criptografia Fernet e SHA-256", "data_hora": "2026-10-10 11:12:04", "departamento": "Desenvolvimento / TI"}
]

df_dados = pd.DataFrame(dados)

# --- CABEÇALHO ---
st.markdown("### ⚡ Supabase Observability & Threat Telemetry")
st.markdown("Painel de controlo corporativo em tempo real integrado ao cluster de produção.")
st.sidebar.markdown("---")

# --- FILTROS NA BARRA LATERAL ---
st.sidebar.subheader("⚙️ Filtros de Fleet")

operadores = ["Todos"] + list(df_dados["nome_operador"].dropna().unique())
op_sel = st.sidebar.selectbox("Filtrar por Operador:", operadores)

deptos = ["Todos"] + list(df_dados["departamento"].dropna().unique())
dept_sel = st.sidebar.selectbox("Filtrar por Departamento:", deptos)

if op_sel != "Todos":
    df_dados = df_dados[df_dados["nome_operador"] == op_sel]

if dept_sel != "Todos":
    df_dados = df_dados[df_dados["departamento"] == dept_sel]

# --- MÉTRICAS ---
total_reg = len(df_dados)
ops_unicos = df_dados["nome_operador"].nunique()
ultima = df_dados["data_hora"].max() if not df_dados.empty else "N/A"

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(label="TOTAL QUERIES", value=total_reg)

with c2:
    st.metric(label="ÚLTIMO EVENTO", value=ultima)

with c3:
    st.metric(label="ACTIVE OPERATORS", value=ops_unicos)

with c4:
    st.metric(label="DATABASE STATUS", value="🟢 Online")

st.markdown("---")

# --- TABELA ---
st.subheader("📋 Registo de Atividades e Pesquisas")
st.dataframe(df_dados, use_container_width=True)
