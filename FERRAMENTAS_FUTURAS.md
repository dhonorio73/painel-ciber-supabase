# Referências para evolução da arquitetura

Este registro reúne alternativas discutidas para avaliar conforme volume, custo, equipe e requisitos. A escolha depende de testes e da necessidade do projeto.

- **Armazenamento em nuvem:** Amazon S3, Google Cloud Storage ou Azure Blob Storage para guardar arquivos compartilhados e ampliar a capacidade.
- **Formatos de tabela analítica:** Apache Iceberg ou Delta Lake para acrescentar recursos de gerenciamento e transações a tabelas em armazenamento compatível. Parquet isoladamente não fornece esses recursos.
- **Processamento:** Polars pode ser avaliado para processamento local eficiente; Apache Spark pode ser avaliado quando houver necessidade de processamento distribuído. Desempenho depende dos dados e da carga.
- **BI:** Power BI, Tableau ou Apache Superset podem consumir bases analíticas para relatórios e visualizações, sujeitos aos recursos e licenças de cada ferramenta.
- **Orquestração e governança:** ferramentas de agendamento, catálogo, monitoramento e controle de acesso podem ser consideradas quando a operação exigir.

A implementação atual é uma demonstração local com Python, Parquet, SQLite em memória, Streamlit e Supabase. Essas alternativas não estão instaladas ou integradas.
