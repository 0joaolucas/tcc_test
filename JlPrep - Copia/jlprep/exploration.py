# preprocess/exploration.py
from pandas.api.types import (
    is_numeric_dtype,
    is_categorical_dtype,
    is_object_dtype,
    is_bool_dtype,
)

import pandas as pd

__all__ = ["summarize_data",
           "value_counts_plot",
           "check_data_quality"]

def summarize_data(data: pd.DataFrame):
    """
    Gera um resumo exploratório do DataFrame:
      - Tamanho (linhas/colunas)
      - Tipos de dados por coluna
      - Valores ausentes (contagem e %)
      - Estatísticas por coluna:
          * Numéricas: média, mediana, moda, min, max
          * Categóricas (object/category/bool): moda, nº de categorias únicas, freq. da moda
    Retorna:
      dict: {nome_da_coluna: {estatísticas...}}
    """
    # 1) Tamanho
    print("Número de linhas e colunas:", len(data), "linhas,", len(data.columns), "colunas")

    # 2) Tipos
    print("\nTipos de dados por coluna:")
    print(data.dtypes)

    # 3) Ausentes (contagem e %)
    print("\nValores ausentes por coluna (ordem decrescente):")
    print(data.isnull().sum().sort_values(ascending=False))

    print("\nPorcentagem de valores ausentes por coluna:")
    print(((data.isnull().sum() / len(data)) * 100).round(2))

    # 4) Amostra
    print("\n5 primeiras linhas do DataFrame:")
    print(data.head(5))

    # 5) Estatísticas por coluna
    resumo = {}
    for col in data.columns:
        if is_numeric_dtype(data[col]):
            s = data[col].dropna()
            moda_series = s.mode()
            moda = moda_series.iloc[0] if not moda_series.empty else None
            resumo[col] = {
                "média": s.mean() if not s.empty else None,
                "mediana": s.median() if not s.empty else None,
                "moda": moda,
                "mínimo": s.min() if not s.empty else None,
                "máximo": s.max() if not s.empty else None,
            }
        elif is_categorical_dtype(data[col]) or is_object_dtype(data[col]) or is_bool_dtype(data[col]):
            s = data[col].dropna()
            moda_series = s.mode()
            moda = moda_series.iloc[0] if not moda_series.empty else None
            freq_moda = s.value_counts().iloc[0] if not s.value_counts().empty else 0
            resumo[col] = {
                "moda": moda,
                "n_categorias": s.nunique(),
                "freq_moda": int(freq_moda),
            }
        else:
            # Para tipos como datetime, etc., um resumo simples:
            s = data[col].dropna()
            resumo[col] = {
                "tipo": str(data[col].dtype),
                "n_únicos": s.nunique(),
            }

    # Imprime o resumo
    for col, stats in resumo.items():
        print(f"\nColuna: {col}")
        for k, v in stats.items():
            print(f"  {k}: {v}")

    return resumo


def value_counts_plot(
        data: pd.DataFrame,
        column: str,
        normalize: bool = False,
        top_n: int | None = None
    ) -> None:
     
     import matplotlib.pyplot as plt

     """
    Gera um gráfico de barras com a contagem (ou proporção) dos valores únicos
    em uma coluna categórica.

    Parâmetros
    ----------
    data : pandas.DataFrame
        O DataFrame com os dados.
    column : str
        Nome da coluna categórica a ser analisada.
    normalize : bool, opcional (default=False)
        Se True, mostra proporções (%) em vez de contagens absolutas.
    top_n : int, opcional
        Se definido, mostra apenas as top N categorias mais frequentes.

    Retorno
    -------
    None
        Exibe o gráfico.
    """
     
     #Obtendo frequências
     counts = data[column].value_counts(normalize=normalize)

     if top_n is not None:
         counts = counts.head(top_n)

     counts.plot(kind="bar")
     plt.title(f"Distribuição de valores - {column}")
     plt.xlabel("Categorias")
     plt.ylabel("Frequências (%)" if normalize else "Frequências")
     plt.show()



def check_data_quality(data: pd.DataFrame):
    """
    Analisa a qualidade dos dados de um DataFrame.

    Funcionalidades:
    - Valores ausentes (%)
    - Duplicatas por coluna (%)
    - Outliers (IQR) para colunas numéricas (quantidade)
    - Cardinalidade de colunas categóricas (com gráfico)

    Parâmetros
    ----------
    data : pandas.DataFrame
        O DataFrame a ser analisado.

    Retornos
    -------
    dict
        Dicionários com informações sobre valores ausentes, duplicatas,
        outliers e cardinalidade.
    """

    import numpy as np
    import matplotlib.pyplot as plt
    from pandas.api.types import is_numeric_dtype, is_object_dtype, is_categorical_dtype

    dict_missing_col = {}
    dict_duplicated_col = {}
    dict_outliers_col = {}
    dict_cardinality = {}

    total_rows = len(data)

    # Valores ausentes
    for col in data.columns:
        percentual_missing = (data[col].isnull().sum() / total_rows) * 100
        dict_missing_col[col] = round(float(percentual_missing), 2)

    # Duplicatas
    for col in data.columns:
        duplicated_count = total_rows - data[col].nunique()
        duplicated_percent = (duplicated_count / total_rows) * 100
        dict_duplicated_col[col] = {
            "quantidade": int(duplicated_count),
            "percentual": round(float(duplicated_percent), 2)
        }

    # Outliers (IQR)
    for col in data.columns:
        if is_numeric_dtype(data[col]):
            col_clean = data[col].dropna()

            Q1 = np.percentile(col_clean, 25)
            Q3 = np.percentile(col_clean, 75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers_count = ((col_clean < lower_bound) | (col_clean > upper_bound)).sum()
            dict_outliers_col[col] = int(outliers_count)

    # Cardinalidade (object + categorical)
    for col in data.columns:
        if is_object_dtype(data[col]) or is_categorical_dtype(data[col]):
            unique_values = data[col].nunique()
            proportion = (unique_values / total_rows) * 100

            dict_cardinality[col] = {
                "unicos": int(unique_values),
                "percentual": round(float(proportion), 2)
            }

    # PRINT ORGANIZADO
    print("\n=== QUALIDADE DOS DADOS ===\n")

    print("🔹 Valores ausentes:")
    for col, perc in dict_missing_col.items():
        if perc > 0:
            print(f"- {col}: {perc}%")

    print("\n🔹 Duplicatas:")
    for col, info in dict_duplicated_col.items():
        if info["quantidade"] > 0:
            print(f"- {col}: {info['quantidade']} ({info['percentual']}%)")

    print("\n🔹 Outliers:")
    has_outliers = False
    for col, count in dict_outliers_col.items():
        if count > 0:
            print(f"- {col}: {count} outliers")
            has_outliers = True
    if not has_outliers:
        print("- Nenhum outlier detectado")

    print("\n🔹 Cardinalidade:")
    if dict_cardinality:
        for col, info in dict_cardinality.items():
            print(f"- {col}: {info['unicos']} valores únicos ({info['percentual']}%)")

            if info["percentual"] > 50:
                print(f"  ⚠️ Alta cardinalidade, considerar tratamento")
    else:
        print("- Nenhuma coluna categórica detectada")

    # Gráfico de cardinalidade
    if dict_cardinality:
        cols = list(dict_cardinality.keys())
        percents = [info["percentual"] for info in dict_cardinality.values()]

        plt.figure(figsize=(10, 6))
        plt.bar(cols, percents)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Percentual de cardinalidade")
        plt.title("Cardinalidade das colunas categóricas")
        plt.show()

    # Retorno estruturado
    return {
        "missing": dict_missing_col,
        "duplicated": dict_duplicated_col,
        "outliers": dict_outliers_col,
        "cardinality": dict_cardinality
    }

