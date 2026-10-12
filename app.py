import datetime
import time
import requests
import pandas as pd
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Painel Ciber - Supabase", page_icon="🛡️", layout="wide")

SUPABASE_URL = "https://sonjvqvaithtpzrqbolf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJz dXBhYmFzZSIsInJlZiI6InNvbmp2cXZhaXRodHB6cnFib2xmIi wicm9sZSI6ImFub24iLCJpYXQiOjE3OTE3MzI0NzQsImV4cCI6 MjEwNzMwODQ3NH0.U30fYDFbG418bDzY7ampcy30ZiVun7DBr4 T7FjKchPg"

class RepositorioSupabaseApp:
    def __init__(self, url: str, chave: str):
        self.url = url.rstrip('/')
        self.headers = {
            "apikey": chave,
            "Authorization": f"Bearer {chave}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
    def inserir_registo(self, termo: str, nome_operador: str, severidade: str, categoria: str, status: str):
        endpoint = f"{self.url}/rest/v1/historico_pesquisas"
        data_hora_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_id = int(time.time() * 1000)
        
        payload = [{
            "id": timestamp_id,
            "nome_operador": str(nome_operador)[:100],
            "data_nascimento": "Automático",
            "termo_pesquisado": str(termo)[:255],
            "data_hora": data_hora_atual,
            "nivel_severidade": severidade,
            "categoria_ameaca": categoria,
            "status_investigacao": status
        }]
            
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as err:
            st.error(f"Erro ao inserir: {err}")
            return False
            
    def consultar_dados(self, limite: int = 10) -> pd.DataFrame:
        endpoint = f"{self.url}/rest/v1/historico_pesquisas?select=*&order=id.desc&limit={limite}"
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            registos = response.json()
            if not registos:
                return None
            return pd.DataFrame(registos)
        except Exception as e:
            st.error(f"Erro ao consultar base de dados: {e}")
            return None

db = RepositorioSupabaseApp(SUPABASE_URL, SUPABASE_KEY)

st.title("🛡️ Painel de Inteligência de Ameaças (Cibersegurança)")
st.markdown("Dashboard interativo conectado diretamente à sua base de dados na nuvem (**Supabase**).")

# Formulário na Barra Lateral
st.sidebar.header("Novo Registo de Ameaça")
operador_input = st.sidebar.text_input("Nome do Operador", value="Analista SOC")
termo_input = st.sidebar.text_input("Termo Técnico / Ameaça")
severidade_input = st.sidebar.selectbox("Nível de Severidade", ["Baixa", "Média", "Alta", "Crítica"])
categoria_input = st.sidebar.selectbox("Categoria", ["Ransomware", "Phishing", "Vulnerabilidade", "Zero Trust", "Supply Chain", "Outros"])
status_input = st.sidebar.selectbox("Status", ["Pendente", "Em Análise", "Mitigado"])

if st.sidebar.button("💾 Enviar para o Supabase"):
    if termo_input.strip():
        if db.inserir_registo(termo_input, operador_input, severidade_input, categoria_input, status_input):
            st.sidebar.success("Registo guardado com sucesso!")
            st.rerun()
    else:
        st.sidebar.warning("Insira um termo válido.")

st.subheader("📊 Histórico Recente de Pesquisas e Ameaças")
limite_registos = st.slider("Quantidade de registos a exibir", min_value=5, max_value=50, value=10)

df = db.consultar_dados(limite=limite_registos)
if df is not None:
    st.dataframe(df, use_container_width=True)
else:
    st.info("A tabela encontra-se vazia.")
