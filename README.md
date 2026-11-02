# Dh73 # Painel de Atividades e Pesquisas

Painel interativo de pesquisas com integração ao Supabase e uma demonstração de engenharia de dados. Criado por **Douglas Honório** para apresentar análise de dados, consultas SQL e processamento em camadas.

[Abrir demonstração online](https://painel-ciber-supabase-lgeyn7zzphlichhycpfqkb.streamlit.app/) — selecione **Demonstração** para explorar dados fictícios.

## Funcionalidades

- Indicadores, filtros e gráficos com dados fictícios no modo demonstração.
- Seção independente de atendimento fictício, com filtro de status, canais, assuntos e tempo médio de resolução em horas corridas.
- Consulta ao Supabase com autenticação e permissões de acesso.
- Exportação em CSV e relatório HTML, que pode ser impresso em PDF pelo navegador.
- Demonstração de ingestão de dados CSV, JSON e TXT e geração de arquivos Parquet.

## Tecnologias

Python · Streamlit · Pandas · PostgreSQL / Supabase · PyArrow / Parquet · SQLite

## Executar no computador

Com Git e Python 3.12 instalados:

```bash
git clone https://github.com/dhonorio73/painel-ciber-supabase.git
cd painel-ciber-supabase
python -m venv .venv
```

Ative o ambiente virtual no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS: `source .venv/bin/activate`. Depois:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

No painel, selecione **Demonstração**. Os dados são fictícios e não é necessária uma conta no Supabase.

## Conectar ao Supabase

Configure `.streamlit/secrets.toml` no computador ou os secrets da hospedagem:

```toml
SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
SUPABASE_KEY = "SUA_CHAVE_PUBLICA"
```

Use somente chave pública publishable/anon; nunca exponha senhas, chaves secretas ou service role. Selecione **Supabase** e entre com uma conta autorizada no Supabase Auth. As políticas RLS determinam o acesso aos registros e devem ser configuradas antes do uso de dados reais.

O painel consulta `public.historico_pesquisas` e considera os **1.000 maiores IDs**. Filtros, indicadores e exportações abrangem essa amostra. Datas sem fuso são interpretadas como UTC; datas não reconhecidas aparecem vazias. Confira a origem antes de analisar horários. O [schema.sql](./schema.sql) é um exemplo separado para novos projetos; [analise_dados.sql](./analise_dados.sql) contém consultas de diagnóstico.

## Pipeline local

```text
Arquivos fictícios CSV, JSON e TXT
   → validação e padronização em Python
   → Silver: atendimentos em Parquet particionado por ano e mês
   → Gold: dimensões de tempo e canal e fato de atendimentos
   → exploração no painel
```

Execute `python etl.py` para gerar um lote em `dados_processados/`, pasta ignorada pelo Git. Os exemplos estão em `exemplos_pipeline/`; use `--raw CAMINHO` e `--destino CAMINHO` para escolher outras pastas. Cada lote inclui manifesto e informações de origem. Arquivos inválidos ou IDs duplicados impedem a publicação de resultados parciais. O pipeline é independente do Supabase.

O painel também apresenta uma simulação SQLite em memória. SLA e recorrência ficam nulos porque faltam dados para calculá-los. A arquitetura em camadas é educacional e não implementa Delta Lake, transações ACID de lakehouse ou atualização em tempo real. Veja [FERRAMENTAS_FUTURAS.md](./FERRAMENTAS_FUTURAS.md) para possíveis evoluções.

## Organização

| Arquivo | Finalidade |
| --- | --- |
| `app.py` | Interface, filtros e conexão ao Supabase |
| `relatorio.py` | Relatório HTML |
| `pipeline_demo.py` | Simulação analítica local |
| `etl.py` | Processamento e geração de Parquet |
| `exemplos_pipeline/` | Dados fictícios de entrada |
| `test_etl.py` e `test_relatorio.py` | Testes automatizados |

## Testes

```bash
python -m unittest -v test_etl test_relatorio
```

---

**Criado por Douglas Honório.**
