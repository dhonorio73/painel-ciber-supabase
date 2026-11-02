"""Exporta a demonstração local para Parquet; não modifica os arquivos de origem."""
from __future__ import annotations

import argparse
import json
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from pipeline_demo import PASTA, executar_pipeline

COLUNAS = ["id", "canal", "data", "descricao", "_source_file", "_etl_inserted_at"]


def executar(raw: Path, destino: Path) -> Path:
    if not raw.is_dir():
        raise ValueError("A pasta de entrada não existe.")
    linhas, _, erros = executar_pipeline(raw)
    if erros:
        raise ValueError("Entrada rejeitada; nenhum conjunto foi publicado: " + "; ".join(erros))
    if not linhas:
        raise ValueError("Nenhum registro válido encontrado.")
    silver = pd.DataFrame(linhas, columns=COLUNAS)
    silver["data"] = pd.to_datetime(silver["data"])
    dias = silver[["data"]].drop_duplicates().sort_values("data").copy()
    dias["id_data"] = dias["data"].dt.strftime("%Y%m%d").astype("int32")
    dias["ano"] = dias["data"].dt.year.astype("int16")
    dias["mes"] = dias["data"].dt.month.astype("int8")
    dias["dia_semana"] = dias["data"].dt.day_of_week.astype("int8")
    dias["fim_de_semana"] = dias["dia_semana"] >= 5
    dias["_etl_inserted_at"] = silver["_etl_inserted_at"].iloc[0]
    canais = pd.DataFrame({"canal": sorted(silver["canal"].unique())})
    canais["id_canal"] = range(1, len(canais) + 1)
    canais["_etl_inserted_at"] = silver["_etl_inserted_at"].iloc[0]
    fatos = silver.merge(dias[["data", "id_data"]], on="data", validate="many_to_one").merge(canais[["canal", "id_canal"]], on="canal", validate="many_to_one")
    fatos = fatos[["id", "id_data", "id_canal", "descricao", "_source_file", "_etl_inserted_at"]].copy()
    fatos["sla_violado"] = pd.Series(pd.NA, index=fatos.index, dtype="boolean")
    fatos["atendimento_recorrente"] = pd.Series(pd.NA, index=fatos.index, dtype="boolean")
    destino.mkdir(parents=True, exist_ok=True)
    nome = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    with tempfile.TemporaryDirectory(prefix=".etl-", dir=destino) as temporaria:
        pasta = Path(temporaria)
        (pasta / "silver").mkdir()
        (pasta / "gold").mkdir()
        silver.assign(ano=silver["data"].dt.year, mes=silver["data"].dt.month).to_parquet(pasta / "silver" / "atendimentos", index=False, partition_cols=["ano", "mes"])
        dias.to_parquet(pasta / "gold" / "dim_tempo.parquet", index=False)
        canais.to_parquet(pasta / "gold" / "dim_canal.parquet", index=False)
        fatos.to_parquet(pasta / "gold" / "fato_atendimentos.parquet", index=False)
        (pasta / "manifesto.json").write_text(json.dumps({"registros": len(fatos), "arquivos_origem": sorted(silver["_source_file"].unique().tolist()), "executado_em_utc": silver["_etl_inserted_at"].iloc[0]}, ensure_ascii=False, indent=2), encoding="utf-8")
        final = destino / nome
        pasta.rename(final)
    return final


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL local demonstrativo para Parquet")
    parser.add_argument("--raw", type=Path, default=PASTA, help="Pasta de entrada CSV/JSON/TXT")
    parser.add_argument("--destino", type=Path, default=Path(__file__).parent / "dados_processados", help="Pasta para novos lotes")
    args = parser.parse_args()
    try:
        print(f"Lote criado em: {executar(args.raw, args.destino)}")
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Erro: {exc}\n")

