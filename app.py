import pandas as pd
import streamlit as st
from supabase import create_client
from relatorio import gerar_relatorio
from pipeline_demo import executar_pipeline

st.set_page_config(page_title="Dh73 # Painel de Atividades e Pesquisas", page_icon="📊", layout="wide")
st.markdown("""
<style>
.stApp { background: #f4f7fb; color: #15283f; }
[data-testid="stHeader"] { background: #f4f7fb; }
[data-testid="stSidebar"] { background: #12263e; }
[data-testid="stSidebar"] * { color: #e6edf6; }
[data-testid="stSidebar"] input { color: #ffffff !important; caret-color: #ffffff; }
.block-container { max-width: 1500px; padding-top: 2.4rem; padding-bottom: 3rem; }
.dh-hero { background: linear-gradient(115deg, #102841 0%, #174365 72%, #126c77 100%); color: white; border-radius: 18px; padding: 2rem 2.3rem; margin-bottom: 1.4rem; }
.dh-kicker { color: #99e1db; text-transform: uppercase; letter-spacing: .16em; font-size: .72rem; font-weight: 700; }
.dh-hero h1 { color: white; font-size: clamp(1.8rem, 3vw, 2.7rem); line-height: 1.15; margin: .5rem 0; padding: 0; }
.dh-hero p { color: #d7e6ef; margin: .6rem 0 0; font-size: 1rem; }
[data-testid="stMetric"] { background: white; border: 1px solid #dce6ef; border-radius: 14px; padding: 1.1rem 1.2rem; box-shadow: 0 4px 18px rgba(27, 55, 82, .05); }
[data-testid="stMetricLabel"] { color: #60758a; font-weight: 600; }
[data-testid="stMetricValue"] { color: #143a5a; font-weight: 700; }
[data-testid="stExpander"] { border: 1px solid #dce6ef; border-radius: 12px; background: #fff; }
[data-testid="stDownloadButton"] button { border: 1px solid #a8c5d8; border-radius: 9px; color: #164b68; }
h2, h3 { color: #193a56; }
@media(max-width: 700px) { .dh-hero { padding: 1.35rem; } .block-container { padding-top: 1rem; } }
</style>
<div class="dh-hero"><div class="dh-kicker">DH73 · INTELIGÊNCIA DE DADOS</div><h1>Painel de Atividades e Pesquisas</h1><p>Uma visão clara dos registros, pessoas e departamentos.</p></div>
""", unsafe_allow_html=True)
st.sidebar.markdown("### DH73 | Painel")
st.sidebar.caption("Selecione a fonte e refine sua análise.")

with st.expander("DH73 Atendimento | Indicadores de suporte (demonstração)", expanded=False):
    st.caption("Cenário fictício independente das pesquisas e do Supabase. Os filtros desta seção não alteram o painel abaixo.")
    chamados = pd.DataFrame([
        {"chamado": "AT-001", "assunto": "Acesso à conta", "equipe": "Suporte", "canal": "E-mail", "status": "Concluído", "abertura": "2026-10-01 09:00", "conclusão": "2026-10-01 13:00"},
        {"chamado": "AT-002", "assunto": "Pagamento", "equipe": "Financeiro", "canal": "Chat", "status": "Em andamento", "abertura": "2026-10-02 10:00", "conclusão": None},
        {"chamado": "AT-003", "assunto": "Erro no sistema", "equipe": "Suporte", "canal": "Chat", "status": "Aberto", "abertura": "2026-10-03 08:00", "conclusão": None},
        {"chamado": "AT-004", "assunto": "Pagamento", "equipe": "Financeiro", "canal": "Telefone", "status": "Concluído", "abertura": "2026-10-03 09:00", "conclusão": "2026-10-04 09:00"},
        {"chamado": "AT-005", "assunto": "Acesso à conta", "equipe": "Suporte", "canal": "E-mail", "status": "Concluído", "abertura": "2026-10-04 12:00", "conclusão": "2026-10-04 14:00"},
    ])
    chamados["abertura"] = pd.to_datetime(chamados["abertura"], utc=True)
    chamados["conclusão"] = pd.to_datetime(chamados["conclusão"], utc=True)
    filtro_status = st.selectbox("Status dos atendimentos", ["Todos", "Aberto", "Em andamento", "Concluído"], key="suporte_status")
    if filtro_status != "Todos":
        chamados = chamados[chamados["status"] == filtro_status]
    finalizados = chamados[chamados["status"] == "Concluído"].copy()
    horas = (finalizados["conclusão"] - finalizados["abertura"]).dt.total_seconds().div(3600)
    horas = horas[horas >= 0].dropna()
    total, abertos, andamento, resolucao = st.columns(4)
    total.metric("Atendimentos", len(chamados))
    abertos.metric("Abertos", int((chamados["status"] == "Aberto").sum()))
    andamento.metric("Em andamento", int((chamados["status"] == "Em andamento").sum()))
    resolucao.metric("Tempo médio de resolução", f"{horas.mean():.1f} h" if not horas.empty else "Sem dados")
    st.caption("Tempo médio em horas corridas, somente para chamados concluídos com abertura e conclusão válidas. Indicadores seguem o filtro de status.")
    assuntos, canais = st.columns(2)
    with assuntos:
        st.subheader("Assuntos mais frequentes")
        if chamados.empty:
            st.info("Nenhum chamado para o filtro escolhido.")
        else:
            st.bar_chart(chamados["assunto"].value_counts())
    with canais:
        st.subheader("Atendimentos por canal")
        if not chamados.empty:
            st.bar_chart(chamados["canal"].value_counts())
    st.dataframe(chamados, hide_index=True, use_container_width=True)

COLUNAS = ["id", "nome_operador", "departamento", "termo_pesquisado", "data_hora"]
DEMO = [
    {"id": 1, "nome_operador": "Ana", "departamento": "Segurança", "termo_pesquisado": "Vulnerabilidades", "data_hora": "2026-10-01T09:15:00Z"},
    {"id": 2, "nome_operador": "Carlos", "departamento": "Infraestrutura", "termo_pesquisado": "Firewall", "data_hora": "2026-10-02T11:30:00Z"},
    {"id": 3, "nome_operador": "Ana", "departamento": "Segurança", "termo_pesquisado": "DDoS", "data_hora": "2026-10-03T08:45:00Z"},
]

def carregar_atividades(cliente):
    # Limite explícito para evitar apresentar uma amostra como histórico completo.
    resposta = cliente.table("historico_pesquisas").select(",".join(COLUNAS)).order("id", desc=True).limit(1000).execute()
    return resposta.data

fonte = st.sidebar.radio("Fonte dos dados", ["Demonstração", "Supabase"])
if fonte == "Demonstração":
    registros = DEMO
    st.info("Modo de demonstração: dados fictícios, sem conexão com banco de dados.")
else:
    try:
        url = st.secrets["SUPABASE_URL"]
        chave = st.secrets["SUPABASE_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("Configure SUPABASE_URL e SUPABASE_KEY nos secrets do Streamlit. Consulte o README.")
        st.stop()
    cliente = create_client(url, chave)
    with st.sidebar.form("login"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")
    if st.sidebar.button("Sair"):
        st.session_state.pop("tokens", None)
        st.rerun()
    try:
        if entrar:
            sessao = cliente.auth.sign_in_with_password({"email": email, "password": senha}).session
            st.session_state["tokens"] = (sessao.access_token, sessao.refresh_token)
        elif "tokens" in st.session_state:
            sessao = cliente.auth.set_session(*st.session_state["tokens"]).session
            st.session_state["tokens"] = (sessao.access_token, sessao.refresh_token)
        else:
            st.info("Entre com um usuário autorizado do Supabase para consultar os dados.")
            st.stop()
        registros = carregar_atividades(cliente)
    except Exception:
        st.error("Não foi possível consultar as atividades. Verifique a configuração, a tabela e as permissões de acesso.")
        st.stop()
    with st.sidebar.expander("Alterar senha"):
        with st.form("alterar_senha", clear_on_submit=True):
            nova_senha = st.text_input("Nova senha", type="password")
            confirmar_senha = st.text_input("Confirme a nova senha", type="password")
            alterar = st.form_submit_button("Salvar nova senha")
        if alterar:
            if len(nova_senha) < 8 or nova_senha != confirmar_senha:
                st.error("Use pelo menos 8 caracteres e confirme a mesma senha.")
            else:
                try:
                    cliente.auth.update_user({"password": nova_senha})
                    st.success("Senha alterada. Use a nova senha no próximo acesso.")
                except Exception:
                    st.error("Não foi possível alterar a senha. Verifique as regras de segurança do Supabase.")
    st.caption("Consulta concluída. São exibidos até 1.000 registros com maior ID; os indicadores consideram apenas os registros retornados. A data é armazenada como texto no banco.")

frame = pd.DataFrame(registros, columns=COLUNAS)
frame["data_hora"] = pd.to_datetime(frame["data_hora"], errors="coerce", utc=True, format="mixed")
invalidas = int(frame["data_hora"].isna().sum())
st.sidebar.header("Filtros")
for coluna, rotulo in [("nome_operador", "Operador"), ("departamento", "Departamento")]:
    opcoes = sorted(frame[coluna].dropna().astype(str).unique().tolist())
    selecionado = st.sidebar.selectbox(rotulo, ["Todos"] + opcoes)
    if selecionado != "Todos":
        frame = frame[frame[coluna] == selecionado]

if not frame["data_hora"].dropna().empty and st.sidebar.checkbox("Filtrar por período"):
    datas = frame["data_hora"].dropna().dt.date
    periodo = st.sidebar.date_input("Período (UTC)", value=(datas.min(), datas.max()), min_value=datas.min(), max_value=datas.max())
    if len(periodo) == 2:
        inicio, fim = periodo
        if inicio > fim:
            st.sidebar.error("A data inicial deve ser anterior à data final.")
            st.stop()
        datas_frame = frame["data_hora"].dt.date
        frame = frame[datas_frame.between(inicio, fim)]
        st.sidebar.caption("O período exclui registros sem data reconhecida.")
    else:
        st.sidebar.info("Selecione as datas inicial e final.")
        st.stop()

if invalidas:
    st.warning(f"{invalidas} registro(s) na amostra estão sem data reconhecida. Confira o formato no banco.")
st.markdown("### Visão geral")
st.caption("Indicadores e filtros consideram somente os registros carregados. Datas sem fuso informado são interpretadas como UTC.")
ultimo = frame["data_hora"].max()
a, b, c, d = st.columns(4)
a.metric("Pesquisas", len(frame))
b.metric("Operadores", frame["nome_operador"].nunique())
c.metric("Departamentos", frame["departamento"].nunique())
d.metric("Última atividade (UTC)", ultimo.strftime("%d/%m/%Y %H:%M") if pd.notna(ultimo) else "Sem data")
if frame.empty:
    st.info("Nenhum registro encontrado para os filtros selecionados.")
else:
    st.markdown("### Análise de atividades")
    esquerda, direita = st.columns(2)
    with esquerda:
        st.subheader("Pesquisas por departamento")
        st.bar_chart(frame["departamento"].fillna("Não informado").value_counts())
    with direita:
        st.subheader("Pesquisas por dia (UTC)")
        por_dia = frame.dropna(subset=["data_hora"]).groupby(frame["data_hora"].dt.date).size()
        if por_dia.empty:
            st.info("Não há datas reconhecidas para este gráfico.")
        else:
            st.line_chart(por_dia)
    st.subheader("Registros de atividades")
    tabela = frame.sort_values("data_hora", ascending=False)
    st.dataframe(tabela, use_container_width=True, hide_index=True)
    st.download_button("Baixar registros em CSV", tabela.to_csv(index=False).encode("utf-8-sig"), file_name="atividades.csv", mime="text/csv")
    st.download_button("Baixar relatório com gráfico (HTML)", gerar_relatorio(tabela, fonte).encode("utf-8"), file_name="relatorio_dh73.html", mime="text/html")
    st.caption("Abra o relatório no navegador para imprimir ou salvar como PDF.")

with st.expander("Como os dados chegam ao painel"):
    st.markdown("O PostgreSQL do Supabase armazena os registros. O painel consulta a tabela com as permissões do usuário e apresenta os resultados. No modo demonstração, usa exemplos fictícios.")
    st.code("SELECT departamento, COUNT(*) AS total\nFROM public.historico_pesquisas\nGROUP BY departamento\nORDER BY total DESC;", language="sql")


with st.expander("Demonstração de pipeline: atendimento fictício"):
    st.caption("Exemplo local: CSV, JSON e texto são tratados e analisados em SQLite em memória. Os dados não são enviados ao Supabase.")
    linhas_demo, resumo_demo, erros_demo = executar_pipeline()
    st.write(f"Registros tratados: {len(linhas_demo)} | Problemas: {len(erros_demo)}")
    if erros_demo:
        st.warning("; ".join(erros_demo))
    st.dataframe(pd.DataFrame(linhas_demo, columns=["ID", "Canal", "Data", "Descrição", "Arquivo de origem", "Processado em UTC"]), hide_index=True)
    if resumo_demo:
        st.bar_chart(pd.DataFrame(resumo_demo, columns=["Canal", "Tickets"]).set_index("Canal"))
    st.caption("SLA e recorrência não são calculados: faltam os dados e regras necessários. Isto é uma simulação, não um lakehouse de produção.")

with st.expander("Lotes Parquet do ETL"):
    from pathlib import Path
    import json
    pasta_lotes = Path(__file__).parent / "dados_processados"
    lotes = sorted((p for p in pasta_lotes.iterdir() if p.is_dir() and not p.name.startswith(".") and (p / "manifesto.json").is_file()), reverse=True) if pasta_lotes.exists() else []
    if not lotes:
        st.info("Nenhum lote encontrado. Execute python etl.py para gerar os dados fictícios.")
    else:
        escolhido = st.selectbox("Lote", lotes, format_func=lambda p: p.name)
        try:
            manifesto = json.loads((escolhido / "manifesto.json").read_text(encoding="utf-8"))
            fatos = pd.read_parquet(escolhido / "gold" / "fato_atendimentos.parquet")
            canais = pd.read_parquet(escolhido / "gold" / "dim_canal.parquet")
            datas = pd.read_parquet(escolhido / "gold" / "dim_tempo.parquet")
            visual = fatos.merge(canais[["id_canal", "canal"]], on="id_canal", validate="many_to_one").merge(datas[["id_data", "data"]], on="id_data", validate="many_to_one")
            st.caption(f"Lote {escolhido.name} • {len(visual)} registros • processado em {manifesto.get('executado_em_utc', 'não informado')}")
            st.write("Arquivos de origem:", ", ".join(manifesto.get("arquivos_origem", [])))
            st.bar_chart(visual["canal"].value_counts())
            st.dataframe(visual[["id", "data", "canal", "descricao", "_source_file"]], hide_index=True)
        except (OSError, ValueError, KeyError) as exc:
            st.error(f"Não foi possível abrir este lote: {exc}")


st.markdown('<div style="margin-top:3rem;padding:1.3rem 0;border-top:1px solid #dce6ef;color:#60758a;text-align:center;font-size:.85rem;">DH73 · Criado por Douglas Honório</div>', unsafe_allow_html=True)

