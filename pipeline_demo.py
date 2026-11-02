"""Pipeline educacional local: ingestão de arquivos e modelo dimensional em memória."""
from datetime import date, datetime, timezone
from pathlib import Path
import csv
import json
import sqlite3

PASTA = Path(__file__).parent / "exemplos_pipeline"


def executar_pipeline(pasta=PASTA):
    instante = datetime.now(timezone.utc).isoformat()
    aceitos, erros, ids = [], [], set()
    for caminho in sorted(Path(pasta).iterdir()):
        if not caminho.is_file() or caminho.suffix.lower() not in {".csv", ".json", ".txt"}:
            continue
        try:
            with caminho.open(encoding="utf-8-sig", newline="") as f:
                if caminho.suffix.lower() == ".csv":
                    entradas = list(csv.DictReader(f))
                elif caminho.suffix.lower() == ".json":
                    entradas = json.load(f)
                    if not isinstance(entradas, list):
                        raise ValueError("JSON deve conter uma lista de objetos")
                else:
                    entradas = []
                    for linha in f:
                        partes = linha.strip().split("|", 3)
                        entradas.append(dict(zip(("id", "canal", "data", "descricao"), partes)))
            for indice, item in enumerate(entradas, 1):
                try:
                    if not isinstance(item, dict):
                        raise ValueError("registro não é um objeto")
                    ident, canal, descricao = (str(item.get(k) or "").strip() for k in ("id", "canal", "descricao"))
                    dia = date.fromisoformat(str(item.get("data") or "").strip())
                    if not ident or not canal or not descricao:
                        raise ValueError("campo obrigatório vazio")
                    if ident in ids:
                        raise ValueError("ID duplicado")
                    ids.add(ident)
                    aceitos.append((ident, canal.lower(), dia, descricao, caminho.name, instante))
                except (ValueError, TypeError) as exc:
                    erros.append(f"{caminho.name}, registro {indice}: {exc}")
        except (OSError, UnicodeError, ValueError, csv.Error) as exc:
            erros.append(f"{caminho.name}: {exc}")
    with sqlite3.connect(":memory:") as db:
        db.executescript('''
          CREATE TABLE dim_tempo (id_data INTEGER PRIMARY KEY, data TEXT, ano INTEGER, mes INTEGER, dia_semana INTEGER, fim_de_semana INTEGER, _etl_inserted_at TEXT);
          CREATE TABLE dim_canal (id_canal INTEGER PRIMARY KEY, canal TEXT UNIQUE, _etl_inserted_at TEXT);
          CREATE TABLE fato_atendimentos (id TEXT PRIMARY KEY, id_data INTEGER, id_canal INTEGER, descricao TEXT, sla_violado INTEGER, atendimento_recorrente INTEGER, _source_file TEXT, _etl_inserted_at TEXT, FOREIGN KEY(id_data) REFERENCES dim_tempo(id_data), FOREIGN KEY(id_canal) REFERENCES dim_canal(id_canal));
        ''')
        db.execute("PRAGMA foreign_keys = ON")
        for ident, canal, dia, descricao, origem, criado in aceitos:
            chave = int(dia.strftime("%Y%m%d"))
            db.execute("INSERT OR IGNORE INTO dim_tempo VALUES (?,?,?,?,?,?,?)", (chave, dia.isoformat(), dia.year, dia.month, dia.weekday(), int(dia.weekday() >= 5), criado))
            db.execute("INSERT OR IGNORE INTO dim_canal(canal,_etl_inserted_at) VALUES (?,?)", (canal, criado))
            canal_id = db.execute("SELECT id_canal FROM dim_canal WHERE canal=?", (canal,)).fetchone()[0]
            db.execute("INSERT INTO fato_atendimentos VALUES (?,?,?,?,NULL,NULL,?,?)", (ident, chave, canal_id, descricao, origem, criado))
        resumo = db.execute("SELECT c.canal, COUNT(*) FROM fato_atendimentos f JOIN dim_canal c ON c.id_canal=f.id_canal GROUP BY c.canal ORDER BY c.canal").fetchall()
    return aceitos, resumo, erros
