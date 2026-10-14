__all__ = ["encode_label",
           "encode_onehot"]

import pandas as pd


def encode_label(data: pd.DataFrame,
                columns: list[str] | None = None,
                return_mapping: bool = False) -> pd.DataFrame:

    
    """

    Aplica codificação label encoding em colunas categóricas de um Dataframe.

    Cada valor único de texto é substituído por um número inteiro, facilitando o uso
    de dados categóricos em algoritmos de Machine Learning.

    Parâmetros:
    ----------
    data: pandas.Dataframe
        O DataFrame de entrada que contém os dados a serem codificados

    columns: list (opcional)
        Lista de colunas a serem codificadas. Se "None", todas as colunas do tipo 'object' serão usadas.

    return_mapping : bool, opcional
        Se True, retorna também um dicionário com os mapeamentos de rótulo para número inteiro
        para cada coluna codificada.

    Retorna:
    -------
    pandas.DataFrame
        O DataFrame com as colunas especificadas codificadas.

    dict (opcional)
        Um dicionário contendo os mapeamentos usados para cada coluna, se return_mapping=True.
    """

    if columns is None:
        columns = data.select_dtypes(include=["object", "string", "category"]).columns

    if return_mapping:
        mapping_dict = {}

    for col in columns:
        unique_values = data[col].unique()
        mapping = {label: idx for idx, label in enumerate(unique_values)}
        data[col] = data[col].map(mapping)

        if return_mapping:
            mapping_dict[col] = mapping

    
    if return_mapping:
        return data, mapping_dict
    return data



def encode_onehot(
    data: pd.DataFrame,
    columns: list[str] | None = None,
    drop_first: bool = False
) -> pd.DataFrame:
    """
    Codifica variáveis categóricas usando One-Hot Encoding.

    Parâmetros
    ----------
    data : pandas.DataFrame
        DataFrame contendo os dados.

    columns : list[str] | None, opcional
        Lista das colunas categóricas que serão codificadas.
        Se None, todas as colunas dos tipos 'object', 'string' e 'category'
        serão utilizadas.

    drop_first : bool, opcional
        Se True, remove a primeira categoria de cada coluna codificada,
        evitando multicolinearidade.

    Retorna
    -------
    pandas.DataFrame
        Novo DataFrame contendo as colunas categóricas codificadas.

    Levanta
    -------
    KeyError
        Se alguma coluna informada não existir no DataFrame.

    TypeError
        Se alguma coluna informada não for categórica.
    """

    if columns is None:
        columns = data.select_dtypes(include=["object", "string", "category"]).columns.tolist()

    for col in columns:
        if col not in data.columns:
            raise KeyError(f"A coluna '{col}' não existe no DataFrame.")

        if not (
            pd.api.types.is_object_dtype(data[col])
            or pd.api.types.is_string_dtype(data[col])
            or pd.api.types.is_categorical_dtype(data[col])
        ):
            raise TypeError(f"A coluna '{col}' deve ser categórica.")

    return pd.get_dummies(
        data,
        columns=columns,
        drop_first=drop_first,
        dtype=int
    )