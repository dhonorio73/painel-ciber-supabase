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
st.markdown("Dashboard executivo com tabela otimizada, análise gráfica e relatórios limpos.")

df = carregar_dados()

if not df.empty:
    # --- MÉTRICAS SUPERIORES (KPIs) ---
    total_registos = len(df)
    operadores_unicos = df["nome_operador"].nunique()
    ultima_atualizacao = df["data_hora"].max().strftime("%Y-%m-%d %H:%M:%S") if "data_hora" in df.columns and pd.notnull(df["data_hora"].max()) else "N/A"
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total de Ameaças", total_registos)
    col2.metric("👥 Operadores Ativos", operadores_unicos)
    col3.metric("🕒 Última Atividade", ultima_atualizacao)
    
    st.markdown("---")
    
    # --- FILTROS E AUDITORIA ---
    st.subheader("🔍 Filtros e Segmentação")
    f_col1, f_col2 = st.columns(2)
    
    with f_col1:
        operadores_lista = ["Todos"] + list(df["nome_operador"].unique())
        filtro_operador = st.selectbox("Filtrar por Operador:", operadores_lista)
        
    with f_col2:
        filtro_termo = st.text_input("Pesquisar palavra-chave:", "")

    df_filtrado = df.copy()
    if filtro_operador != "Todos":
        df_filtrado = df_filtrado[df_filtrado["nome_operador"] == filtro_operador]
    if filtro_termo.strip():
        df_filtrado = df_filtrado[df_filtrado["termo_pesquisado"].str.contains(filtro_termo, case=False, na=False)]

    # --- ALERTAS DE SEGURANÇA INTELIGENTES ---
    termos_criticos = ["virus", "ransomware", "zero-day", "malicious", "compromised", "attack"]
    alerta_detectado = df_filtrado["termo_pesquisado"].str.contains("|".join(termos_criticos), case=False, na=False).any()
            
    if alerta_detectado:
        st.error("🚨 **ALERTA CRÍTICO DE SEGURANÇA:** Foram encontrados vetores de ataque maliciosos ou termos críticos nos registos filtrados abaixo!")
    else:
        st.success("✅ **Estado Normal:** Nenhum vetor crítico ativo nos filtros atuais.")

    # --- GRÁFICOS ANALÍTICOS ---
    st.markdown("### 📈 Análise Gráfica e Desempenho")
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.markdown("**Registos por Operador**")
        if not df_filtrado.empty:
            contagem_ops = df_filtrado["nome_operador"].value_counts()
            st.bar_chart(contagem_ops)
            
    with g_col2:
        st.markdown("**Distribuição de Atividade Temporal**")
        if "data_hora" in df_filtrado.columns:
            df_temporal = df_filtrado.copy()
            df_temporal["data_dia"] = pd.to_datetime(df_temporal["data_hora"]).dt.date
            contagem_tempo = df_temporal["data_dia"].value_counts().sort_index()
            st.line_chart(contagem_tempo)

    # --- ORGANIZAÇÃO E FORMATAÇÃO DA TABELA ---
    st.markdown("### 📊 Histórico Detalhado de Pesquisas")
    limite_slider = st.slider("Quantidade de registos a exibir na tabela", 5, 50, 10)
    
    # Organizar, selecionar colunas úteis e excluir a coluna "data_nascimento" (desnecessária)
    colunas_desejadas = ["id", "data_hora", "nome_operador", "termo_pesquisado"]
    df_organizado = df_filtrado[[c for c in colunas_desejadas if c in df_filtrado.columns]].copy()
    
    # Renomear colunas para exibição profissional
    df_organizado.rename(columns={
        "id": "ID do Registo",
        "data_hora": "Data e Hora",
        "nome_operador": "Operador",
        "termo_pesquisado": "Termo Técnico / Ameaça"
    }, inplace=True)

    def colorir_criticos(val):
        criticos = ["virus", "ransomware", "zero-day", "malicious", "compromised", "attack"]
        if any(c in str(val).lower() for c in criticos):
            return 'background-color: rgba(255, 75, 75, 0.2); color: #ff4b4b; font-weight: bold;'
        return ''

    if not df_organizado.empty:
        df_exibicao = df_organizado.head(limite_slider)
        st.dataframe(
            df_exibicao.style.map(colorir_criticos, subset=["Termo Técnico / Ameaça"]),
            use_container_width=True
        )
    
    # O CSV descarregado também virá limpo e estruturado sem colunas desnecessárias
    csv_dados = df_organizado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descarregar Relatório Limpo (CSV)",
        data=csv_dados,
        file_name="relatorio_ciber_organizado.csv",
        mime="text/csv",
    )
else:
    st.info("A tabela de dados está vazia ou a carregar...")
