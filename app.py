import streamlit as st
import pandas as pd
import requests
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Painel Ciber - Supabase",
    page_icon="🛡️",
    layout="wide"
)

# --- CREDENCIAIS DO SUPABASE ---
SUPABASE_URL = "https://sonjvqvaithtpzrqbolf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNvbmp2cXZhaXRodHB6cnFib2xmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE3MzI0NzQsImV4cCI6MjEwNzMwODQ3NH0.U30fYDFbG418bDzY7ampcy30ZiVun7DBr4T7FjKchPg"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# --- FUNÇÕES DE CONEXÃO E DADOS ---
@st.cache_data(ttl=5)
def carregar_dados():
    endpoint = f"{SUPABASE_URL}/rest/v1/historico_pesquisas?select=*&order=id.desc"
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data) if data else pd.DataFrame()
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

# --- INTERFACE DO UTILIZADOR (SIDEBAR) ---
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

# --- PAINEL PRINCIPAL ---
st.title("🛡️ Painel de Inteligência de Ameaças (Cibersegurança)")
st.markdown("Dashboard corporativo conectado diretamente à base de dados em tempo real (*Supabase*).")

# Carregar dados
df = carregar_dados()

if not df.empty:
    # --- MÉTRICAS SUPERIORES (KPIs) ---
    total_registos = len(df)
    operadores_unicos = df["nome_operador"].nunique()
    ultima_atualizacao = df["data_hora"].max() if "data_hora" in df.columns else "N/A"
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Ameaças Registadas", total_registos)
    col2.metric("Operadores Ativos", operadores_unicos)
    col3.metric("Última Atividade", ultima_atualizacao)
    
    st.markdown("---")
    
    # --- FILTROS VISUAIS AVANÇADOS ---
    st.subheader("🔍 Filtros e Auditoria")
    f_col1, f_col2 = st.columns(2)
    
    with f_col1:
        operadores_lista = ["Todos"] + list(df["nome_operador"].unique())
        filtro_operador = st.selectbox("Filtrar por Operador:", operadores_lista)
        
    with f_col2:
        filtro_termo = st.text_input("Pesquisar palavra-chave nos registos:", "")

    # Aplicar filtros
    df_filtrado = df.copy()
    if filtro_operador != "Todos":
        df_filtrado = df_filtrado[df_filtrado["nome_operador"] == filtro_operador]
    if filtro_termo.strip():
        df_filtrado = df_filtrado[df_filtrado["termo_pesquisado"].str.contains(filtro_termo, case=False, na=False)]

    # --- ALERTAS DE SEGURANÇA INTELIGENTES ---
    termos_criticos = ["virus", "ransomware", "zero-day", "malicious", "compromised"]
    alerta_detectado = False
    for termo in termos_criticos:
        if df_filtrado["termo_pesquisado"].str.contains(termo, case=False, na=False).any():
            alerta_detectado = True
            break
            
    if alerta_detectado:
        st.error("🚨 **ALERTA DE SEGURANÇA:** Foram detetados indicadores de ameaças críticas ou vectores maliciosos nos registos filtrados abaixo!")

    # --- TABELA DE DADOS ---
    st.markdown("### 📊 Histórico de Pesquisas")
    limite_slider = st.slider("Quantidade de registos a exibir", 5, 50, 10)
    
    st.dataframe(df_filtrado.head(limite_slider), use_container_width=True)
else:
    st.info("A tabela de dados está vazia ou a carregar...")
