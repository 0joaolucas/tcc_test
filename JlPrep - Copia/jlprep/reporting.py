__all__ = ["reporting"]


"""Geração de relatórios HTML a partir de analyze_dataset e compare_datasets."""
from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any
import webbrowser


def _text(value: Any) -> str:
    return escape(str(value), quote=True)


def _number(value: Any) -> str:
    return _text(value if value is not None else "—")


def generate_report(
    diagnosis: dict,
    comparison: dict | None = None,
    output_path: str | Path = "jlprep_report.html",
    title: str = "Relatório de qualidade dos dados — JlPrep",
    open_browser: bool = False,
) -> Path:
    """Gera um relatório HTML local com diagnóstico e comparação."""

    if not isinstance(diagnosis, dict) or not isinstance(
        diagnosis.get("alerts"), list
    ):
        raise TypeError(
            "diagnosis deve ser o retorno de analyze_dataset()."
        )

    if comparison is not None and not isinstance(comparison, dict):
        raise TypeError(
            "comparison deve ser o retorno de compare_datasets()."
        )

    path = Path(output_path).expanduser().resolve()

    if path.suffix.lower() != ".html":
        raise ValueError("O arquivo deve terminar em .html")

    path.parent.mkdir(parents=True, exist_ok=True)

    labels = {
        "missing_values": "Valores ausentes",
        "duplicates": "Registros duplicados",
        "outliers": "Valores extremos (IQR)",
        "class_imbalance": "Desbalanceamento de classes",
    }

    metric_labels = {
        "rows": "Registros",
        "columns": "Colunas",
        "missing_values": "Células ausentes",
        "missing_percentage": "Ausentes (%)",
        "duplicates": "Duplicatas",
    }

    alerts = diagnosis["alerts"]
    alert_html = []

    for alert in alerts:
        if not isinstance(alert, dict):
            continue

        details = []

        fields = [
            ("column", "Coluna"),
            ("count", "Ocorrências"),
            ("percentage", "Percentual (%)"),
            ("ratio", "Razão"),
            ("method", "Método"),
        ]

        for key, label in fields:
            if key in alert:
                details.append(
                    f'<span class="chip">'
                    f'{label}: {_text(alert[key])}'
                    f'</span>'
                )

        recommendation = alert.get(
            "recommendation",
            "Investigar o indicador antes de decidir o tratamento.",
        )

        alert_html.append(
            '<article class="alert">'
            f'<h3>{_text(labels.get(alert.get("type"), alert.get("type", "Alerta")))}</h3>'
            f'<div class="chips">{"".join(details)}</div>'
            f'<p><strong>Recomendação:</strong> '
            f'{_text(recommendation)}</p>'
            '</article>'
        )

    if not alert_html:
        alert_html = [
            '<p class="empty">Nenhum alerta encontrado pelas regras '
            'implementadas. Isso não garante ausência de problemas.</p>'
        ]

    comparison_html = ""

    if comparison is not None:
        before = comparison.get("before", {})
        after = comparison.get("after", {})

        if not isinstance(before, dict) or not isinstance(after, dict):
            raise ValueError(
                "comparison precisa conter 'before' e 'after'."
            )

        rows = []

        for key, label in metric_labels.items():
            if key in before or key in after:
                rows.append(
                    f'<tr><th scope="row">{_text(label)}</th>'
                    f'<td>{_number(before.get(key))}</td>'
                    f'<td>{_number(after.get(key))}</td></tr>'
                )

        comparison_html = (
            '<section class="panel">'
            '<h2>Comparação antes e depois</h2>'
            '<p class="muted">Indicadores agregados; '
            'não identifica alterações individuais de registros.</p>'
            '<div class="table-wrap"><table>'
            '<thead><tr><th>Indicador</th>'
            '<th>Antes</th><th>Depois</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody>'
            '</table></div></section>'
        )

    generated = datetime.now().strftime("%d/%m/%Y %H:%M")

    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_text(title)}</title>
<style>
:root {{
    --bg: #f4f7fb;
    --ink: #17243a;
    --muted: #596b82;
    --line: #dce5ef;
    --brand: #2357a4;
    --paper: #fff;
}}
* {{ box-sizing: border-box; }}
body {{
    margin: 0;
    background: var(--bg);
    font: 16px/1.55 system-ui, sans-serif;
    color: var(--ink);
}}
header {{
    background: linear-gradient(110deg, #17396d, #2862b1);
    color: white;
    padding: 38px max(24px, calc((100vw - 1040px)/2));
}}
header p {{ opacity: .88; margin: 6px 0 0; }}
main {{
    max-width: 1040px;
    margin: 30px auto 70px;
    padding: 0 20px;
}}
h1 {{ font-size: 2rem; margin: 0; }}
h2 {{ margin: 0 0 14px; font-size: 1.25rem; }}
h3 {{ margin: 0 0 8px; font-size: 1.03rem; }}
.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-bottom: 24px;
}}
.card, .panel {{
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 14px;
    box-shadow: 0 4px 16px #17243a0a;
}}
.card {{ padding: 20px; }}
.card .value {{
    font-size: 2rem;
    font-weight: 750;
    color: var(--brand);
}}
.card .label {{
    color: var(--muted);
    font-size: .9rem;
}}
.panel {{ padding: 24px; margin-bottom: 22px; }}
.alert {{
    border-left: 4px solid #e6a43d;
    background: #fffbf3;
    padding: 16px 18px;
    margin: 12px 0;
    border-radius: 7px;
}}
.alert p {{ margin: 10px 0 0; }}
.chips {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.chip {{
    background: #e8eef7;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: .85rem;
}}
.muted, .empty {{ color: var(--muted); }}
.table-wrap {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; text-align: left; }}
th, td {{ padding: 12px 14px; border-bottom: 1px solid var(--line); }}
thead {{ background: #eaf1fa; }}
footer {{
    text-align: center;
    color: var(--muted);
    font-size: .85rem;
    margin-top: 25px;
}}
@media print {{
    body {{ background: white; }}
    .panel, .card {{ box-shadow: none; break-inside: avoid; }}
}}
</style>
</head>
<body>
<header>
    <h1>{_text(title)}</h1>
    <p>Gerado em {generated} · Diagnóstico automatizado</p>
</header>
<main>
<section class="cards">
    <div class="card">
        <div class="label">Registros</div>
        <div class="value">{_number(diagnosis.get("rows"))}</div>
    </div>
    <div class="card">
        <div class="label">Colunas</div>
        <div class="value">{_number(diagnosis.get("columns"))}</div>
    </div>
    <div class="card">
        <div class="label">Alertas</div>
        <div class="value">{len(alerts)}</div>
    </div>
    <div class="card">
        <div class="label">Variável-alvo</div>
        <div class="value" style="font-size:1.3rem;overflow-wrap:anywhere">
            {_text(diagnosis.get("target") or "Não definida")}
        </div>
    </div>
</section>

<section class="panel">
    <h2>Diagnóstico e recomendações</h2>
    {"".join(alert_html)}
</section>

{comparison_html}

<section class="panel">
    <h2>Como interpretar</h2>
    <p>Os alertas indicam situações que merecem investigação.
    Valores extremos não são necessariamente erros, e nem toda
    ausência ou duplicata deve ser removida. As recomendações
    não substituem a análise do contexto dos dados.</p>
</section>

<footer>JlPrep · Relatório gerado localmente.</footer>
</main>
</body>
</html>"""

    path.write_text(html, encoding="utf-8")

    if open_browser:
        webbrowser.open(path.as_uri())

    return path
