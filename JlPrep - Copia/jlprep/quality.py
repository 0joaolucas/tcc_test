# preprocess/exploration.py
from pandas.api.types import (
    is_numeric_dtype,
    is_categorical_dtype,
    is_object_dtype,
    is_bool_dtype,
)

import pandas as pd
import matplotlib.pyplot as plt

__all__ = ["check_class_balance"]

def check_class_balance(
    data: pd.DataFrame,
    target: str,
    plot: bool = False
) -> dict:
    """
    Analisa o balanceamento das classes em uma variável alvo de um dataset.

    Esta função calcula a distribuição das classes, identifica o tipo de problema
    (classificação binária ou multiclasse), mede o nível de desbalanceamento por meio
    da razão entre a classe majoritária e minoritária (imbalance ratio) e fornece
    um diagnóstico com sugestões de tratamento.

    Parâmetros
    ----------
    data : pandas.DataFrame
        Dataset contendo a variável alvo.

    target : str
        Nome da coluna que representa a variável alvo.

    plot : bool, opcional (default=False)
        Se True, exibe um gráfico de barras com a distribuição das classes.

    Retorna
    -------
    dict
        Um dicionário contendo:
        - n_classes
        - problem_type
        - imbalance_ratio
        - status
        - suggestion

    Levanta
    -------
    KeyError
        Se a coluna especificada não existir.

    TypeError
        Se o parâmetro target não for uma string.

    ValueError
        Se a variável alvo possuir menos de duas classes.
    """

    if not isinstance(target, str):
        raise TypeError("O parâmetro 'target' deve ser uma string.")

    if target not in data.columns:
        raise KeyError(f"A coluna '{target}' não existe no DataFrame.")

    col = data[target].dropna()

    class_count = col.value_counts()
    class_proportion = col.value_counts(normalize=True) * 100

    n_classes = len(class_count)

    if n_classes == 2:
        problem = "Binary classification"
    elif n_classes > 2:
        problem = "Multiclass classification"
    else:
        raise ValueError("O dataset deve possuir pelo menos duas classes.")

    max_class = class_count.max()
    min_class = class_count.min()

    imbalance_ratio = max_class / min_class

    if imbalance_ratio <= 1.5:
        status = "Dataset balanceado"
        suggestion = "Nenhuma ação necessária."

    elif imbalance_ratio <= 3:
        status = "Dataset levemente desbalanceado"
        suggestion = "Monitorar o desempenho do modelo."

    elif imbalance_ratio <= 10:
        status = "Dataset moderadamente desbalanceado"
        suggestion = "Considerar técnicas de balanceamento."

    else:
        status = "Dataset altamente desbalanceado"
        suggestion = "Aplicar técnicas de balanceamento (SMOTE, Oversampling, etc.)."

    print("Distribuição das classes:\n")

    for classe in class_count.index:
        print(f"{classe}: {class_count[classe]} ({class_proportion[classe]:.2f}%)")

    print(f"\nNúmero de classes: {n_classes}")
    print(f"Tipo de problema: {problem}")
    print(f"\nImbalance ratio: {imbalance_ratio:.2f}")
    print(f"Status: {status}")
    print(f"Sugestão: {suggestion}")

    if plot:
        class_count.plot(kind="bar", title="Distribuição das classes")
        plt.show()

    return {
        "n_classes": n_classes,
        "problem_type": problem,
        "imbalance_ratio": imbalance_ratio,
        "status": status,
        "suggestion": suggestion
    }