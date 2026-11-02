"""Relatório HTML independente, sem conteúdo externo."""
from html import escape
import pandas as pd


def barras(contagens):
    maior = max(contagens.max(), 1) if len(contagens) else 1
    return ''.join('<div class="linha"><span>' + escape(str(k)) + '</span><div class="fundo"><div class="barra" style="width:' + str(round(int(v) * 100 / int(maior), 1)) + '%"></div></div><b>' + str(int(v)) + '</b></div>' for k, v in contagens.items()) or '<p>Sem dados disponíveis.</p>'


def gerar_relatorio(frame, fonte):
    contagens = frame["departamento"].fillna("Não informado").value_counts()
    datas = frame["data_hora"].dropna()
    periodo = datas.min().strftime("%d/%m/%Y") + " a " + datas.max().strftime("%d/%m/%Y") + " (UTC)" if not datas.empty else "Sem datas reconhecidas"
    diarias = datas.dt.strftime("%Y-%m-%d").value_counts().sort_index()
    tabela = frame.to_html(index=False, escape=True, na_rep="—", border=0)
    estilo = '''body{font:15px system-ui;margin:40px auto;max-width:1000px;padding:0 20px;color:#19324d}header{background:#173a5e;color:white;padding:25px;border-radius:10px}section{margin-top:25px}.linha{display:grid;grid-template-columns:2fr 4fr 1fr;gap:10px;margin:12px 0}.fundo{background:#e9eef4}.barra{height:16px;background:#1976bd;print-color-adjust:exact;-webkit-print-color-adjust:exact}table{border-collapse:collapse;width:100%;font-size:12px}td,th{border-bottom:1px solid #ddd;text-align:left;padding:8px}button{padding:10px}@media print{button{display:none}}'''
    return ('<!doctype html><html lang="pt-br"><meta charset="utf-8"><title>Relatório Dh73</title><style>' + estilo + '</style><header><h1>Dh73 • Relatório de atividades</h1><p>Fonte: ' + escape(fonte) + ' | Registros: ' + str(len(frame)) + ' | Período dos registros: ' + periodo + '</p></header><section><h2>Pesquisas por departamento</h2>' + barras(contagens) + '</section><section><h2>Pesquisas por dia (UTC)</h2>' + barras(diarias) + '</section><section><h2>Registros selecionados</h2>' + tabela + '</section><p>Registros carregados e filtros aplicados no painel. No Supabase, até 1.000 maiores IDs. Datas sem fuso são interpretadas como UTC.</p><button onclick="window.print()">Imprimir / Salvar como PDF</button></html>')
