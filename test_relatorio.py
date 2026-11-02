import unittest
import pandas as pd
from relatorio import gerar_relatorio


class TestRelatorio(unittest.TestCase):
    def test_periodo_grafico_e_escape(self):
        frame = pd.DataFrame({"departamento": ["<script>alert(1)</script>", "TI"], "data_hora": pd.to_datetime(["2026-01-03", "2026-01-01"], utc=True)})
        html = gerar_relatorio(frame, "Demonstração")
        self.assertIn("01/01/2026 a 03/01/2026", html)
        self.assertIn("Pesquisas por dia (UTC)", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>alert(1)</script>", html)


if __name__ == "__main__":
    unittest.main()
