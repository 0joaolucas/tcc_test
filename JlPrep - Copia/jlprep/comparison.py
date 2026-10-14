
__all__ = ["comparison"]

import pandas as pd


def compare_datasets(
    original: pd.DataFrame,
    processed: pd.DataFrame
) -> dict:
    """
    Compara indicadores de dois DataFrames antes e depois
    de um procedimento de pré-processamento.
    """
    if not isinstance(original, pd.DataFrame):
        raise TypeError("original deve ser um DataFrame.")

    if not isinstance(processed, pd.DataFrame):
        raise TypeError("processed deve ser um DataFrame.")

    def metrics(df):
        total_cells = df.shape[0] * df.shape[1]
        missing = int(df.isna().sum().sum())

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": missing,
            "missing_percentage": round(
                missing / total_cells * 100, 2
            ) if total_cells else 0.0,
            "duplicates": int(df.duplicated().sum()),
        }

    before = metrics(original)
    after = metrics(processed)

    return {
        "before": before,
        "after": after,
        "changes": {
            "row_difference": after["rows"] - before["rows"],
            "column_difference": (
                after["columns"] - before["columns"]
            ),
            "missing_difference": (
                after["missing_values"]
                - before["missing_values"]
            ),
            "duplicate_difference": (
                after["duplicates"] - before["duplicates"]
            ),
        },
    }
  