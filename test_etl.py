import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from etl import executar


class TestETL(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.raw = self.base / "raw"
        self.raw.mkdir()
        self.out = self.base / "saida"

    def test_lote_dimensional_e_rastreabilidade(self):
        (self.raw / "dados.csv").write_text("id,canal,data,descricao\n1,email,2026-10-03,Ajuda\n", encoding="utf-8")
        (self.raw / "dados.json").write_text(json.dumps([{"id":"2", "canal":"chat", "data":"2026-10-05", "descricao":"Dúvida"}]), encoding="utf-8")
        lote = executar(self.raw, self.out)
        fatos = pd.read_parquet(lote / "gold/fato_atendimentos.parquet")
        tempo = pd.read_parquet(lote / "gold/dim_tempo.parquet")
        canais = pd.read_parquet(lote / "gold/dim_canal.parquet")
        self.assertEqual(len(fatos), 2)
        self.assertTrue(fatos.id_data.isin(tempo.id_data).all())
        self.assertTrue(fatos.id_canal.isin(canais.id_canal).all())
        self.assertEqual(set(fatos._source_file), {"dados.csv", "dados.json"})
        self.assertTrue(fatos.sla_violado.isna().all())
        self.assertTrue(tempo.loc[tempo.id_data == 20261003, "fim_de_semana"].iloc[0])

    def test_erro_ou_duplicata_nao_publicam_lote(self):
        (self.raw / "dados.csv").write_text("id,canal,data,descricao\n1,email,2026-01-01,a\n1,email,2026-01-02,b\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            executar(self.raw, self.out)
        self.assertFalse(self.out.exists())
        (self.raw / "dados.csv").write_text("id,canal,data,descricao\n1,email,inválida,a\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            executar(self.raw, self.out)
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
