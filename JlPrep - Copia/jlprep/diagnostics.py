__all__ = ["diagnostics"]

import pandas as pd


def analyze_dataset(df: pd.DataFrame, target: str | None = None) -> dict:
    """
    Analisa um DataFrame e gera um diagnóstico com recomendações.

    A análise não modifica os dados originais.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df deve ser um DataFrame do Pandas.")

    if target is not None and target not in df.columns:
        raise KeyError(f"Coluna-alvo '{target}' não encontrada.")

    alerts = []

    # 1. Valores ausentes
    for column in df.columns:
        missing_count = int(df[column].isna().sum())

        if missing_count == 0:
            continue

        missing_pct = (
            missing_count / len(df) * 100 if len(df) else 0.0
        )

        if pd.api.types.is_numeric_dtype(df[column]):
            suggestion = (
                "Investigar a distribuição da variável e avaliar "
                "imputação pela mediana ou outra estratégia adequada."
            )
        else:
            suggestion = (
                "Investigar os valores ausentes e avaliar "
                "imputação pela moda ou criação de uma categoria."
            )

        alerts.append({
            "type": "missing_values",
            "column": column,
            "count": missing_count,
            "percentage": round(missing_pct, 2),
            "recommendation": suggestion,
        })

    # 2. Registros duplicados
    duplicates = int(df.duplicated().sum())

    if duplicates:
        alerts.append({
            "type": "duplicates",
            "count": duplicates,
            "recommendation": (
                "Verificar se os registros repetidos são erros "
                "antes de removê-los."
            ),
        })

    # 3. Outliers pelo método IQR
    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        if column == target:
            continue

        values = df[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outlier_count = int(
            ((values < lower) | (values > upper)).sum()
        )

        if outlier_count:
            alerts.append({
                "type": "outliers",
                "column": column,
                "count": outlier_count,
                "method": "IQR",
                "recommendation": (
                    "Investigar os valores extremos antes de "
                    "decidir pela remoção ou transformação."
                ),
            })

    # 4. Balanceamento das classes
    if target is not None:
        counts = df[target].value_counts(dropna=True)

        if len(counts) >= 2:
            majority = int(counts.max())
            minority = int(counts.min())
            ratio = majority / minority

            if ratio >= 3:
                alerts.append({
                    "type": "class_imbalance",
                    "column": target,
                    "ratio": round(ratio, 2),
                    "recommendation": (
                        "Investigar o impacto do desbalanceamento "
                        "e avaliar métricas por classe e "
                        "estratégias de amostragem."
                    ),
                })

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "target": target,
        "total_alerts": len(alerts),
        "alerts": alerts,
    }
  