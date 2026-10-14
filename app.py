# === CÓDIGO RAIZ - app.py ===
import streamlit as st
import pandas as pd
import requests
import datetime
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Painel Ciber - Supabase",
    page_icon="🛡️",
    layout="wide"
)

# --- CREDENCIAIS DO SUPABASE (LIGAÇÃO DIRETA SEM TÚNEL) ---
SUPABASE_URL = "https://sonjvqvaithtpzrqbolf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvbmp2cXZhaXRodHB6cnFib2xmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE3MzI0NzQsImV4cCI6MjEwNzMwODQ3NH0.U30fYDFbG418bDzY7ampcy30ZiVun7DBr4T7FjKchPg"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- SISTEMA DE AUTENTICAÇÃO POR SENHA ---
def verificar_autenticacao():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.sidebar.subheader("🔒 Acesso Restrito")
        senha_input = st.sidebar.text_input("Palavra-passe corporativa:", type="password")
        if st.sidebar.button("Entrar"):
            if senha_input == "ciber2026":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.sidebar.error("Palavra-passe incorreta.")
        return False
    return True

if not verificar_autenticacao():
    st.title("🛡️ Painel de Inteligência de Ameaças (Cibersegurança)")
    st.warning("⚠️ Por favor, introduza a palavra-passe corporativa (`ciber2026`) na barra lateral para aceder ao dashboard.")
    st.stop()

# --- FUNÇÕES DE CONEXÃO E LEITURA DE DADOS ---
@st.cache_data(ttl=5)
def carregar_dados():
    endpoint = f"{SUPABASE_URL}/rest/v1/historico_pesquisas?select=*&order=id.desc"
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                if "data_hora" in df.columns:
                    df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
                return df
    except Exception as e:
        st.error(f"Erro ao conectar com o Supabase: {e}")
    return pd.DataFrame()

def inserir_registo(nome_operador, termo):
    endpoint = f"{SUPABASE_URL}/rest/v1/historico_pesquisas"
    data_hora_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_id = int(datetime.datetime.now().timestamp() * 1000)

    payload = {
        "id": timestamp_id,
        "nome_operador": str(nome_operador)[:100],
        "data_nascimento": "Automático",
        "termo_pesquisado": str(termo)[:255],
        "data_hora": data_hora_atual
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        return response.status_code in [200, 201]
    except:
        return False

# --- INTERFACE LATERAL ---
st.sidebar.header("📝 Novo Registo de Ameaça")
with st.sidebar.form("form_registo"):
    operador = st.text_input("Nome do Operador", value="Analista SOC")
    termo_pesquisa = st.text_area("Termo Técnico / Ameaça / Vetor")
    submit_button = st.form_submit_button("💾 Enviar para o Supabase")

if submit_button:
    if termo_pesquisa.strip():
        sucesso = inserir_registo(operador, termo_pesquisa)
        if sucesso:
            st.sidebar.success("Registo inserido com sucesso!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.sidebar.error("Erro ao enviar para o Supabase.")
    else:
        st.sidebar.warning("Por favor, insira um termo técnico.")

if st.sidebar.button("🚪 Terminar Sessão"):
    st.session_state.autenticado = False
    st.rerun()

# --- PAINEL PRINCIPAL ---
st.title("🛡️ Painel de Inteligência de Ameaças (Cibersegurança)")
st.markdown("Dashboard executivo com relatórios profissionais, gráficos analíticos e auditoria avançada.")

df = carregar_dados()

if not df.empty:
    total_registos = len(df)
    operadores_unicos = df["nome_operador"].nunique()
    ultima_atualizacao = df["data_hora"].max().strftime("%Y-%m-%d %H:%M:%S") if "data_hora" in df.columns and pd.notnull(df["data_hora"].max()) else "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total de Ameaças", total_registos)
    col2.metric("👥 Operadores Ativos", operadores_unicos)
    col3.metric("🕒 Última Atividade", ultima_atualizacao)

    st.markdown("---")

    # Tabela simples e direta
    st.subheader("📊 Histórico Recente no Supabase")
    st.dataframe(df, use_container_width=True)
else:
    st.info("A tabela de dados está vazia ou a carregar...")
