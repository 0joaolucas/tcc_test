__all__ = ["remove_duplicates",
           "remove_outliers",
           "clean_missing"]

import pandas as pd

def remove_duplicates(data: pd.DataFrame,
                      visualization: bool = False,
                      remove: bool = False) -> pd.DataFrame:
    """
    Remove ou visualiza duplicatas de um dataframe.

    :param data: Dataframe com os dados a serem analisados.
    :param visualization: Se True, visualiza as duplicatas no Dataframe.
    :param remove: Se True, remove as duplicatas no Dataframe.
    :return: Dataframe com ou sem duplicatas, dependendo do parâmetro 'remove'
    
    """
    #Verificando o comportamento
    if visualization and remove:
        print("Exibindo duplicatas")
        print(data[data.duplicated()])
        print("\nRemovendo duplicatas...")
        return data.drop_duplicates()
        
    elif visualization:
        
        print("Exibindo duplicatas:")
        return data[data.duplicated()]

    elif remove:
       
        print("Removendo duplicatas...")
        return data.drop_duplicates()

    else:
        
        print("Nenhuma ação foi realizada. Use 'visualization' para visualizar ou 'remove' para remover duplicatas.")
        return data



def remove_outliers(data: pd.DataFrame,
                    method:str = "iqr",
                    threshold: float = 1.5,
                    columns: list[str] | None = None) -> pd.DataFrame:

    """
    Remove outliers de um DataFrame com base em métodos estatísticos.

    Parâmetros
    ----------
    data : pandas.DataFrame
        Conjunto de dados a ser processado.
    method : str, opcional (default='iqr')
        Método usado para detecção de outliers. Pode ser:
        - 'iqr': usa o intervalo interquartil (Q1 - 1.5*IQR, Q3 + 1.5*IQR)
        - 'zscore': usa o desvio padrão em relação à média.
    threshold : float, opcional (default=1.5)
        Fator usado para definir o limite dos outliers.
        - Para 'iqr': multiplicador do IQR.
        - Para 'zscore': valor absoluto do Z-score máximo permitido.
    columns : list ou None, opcional
        Lista de colunas numéricas a serem analisadas. Se None, aplica em todas as colunas numéricas.

    Retorna
    -------
    pandas.DataFrame
        DataFrame sem os outliers detectados.

    Lança
    -----
    ValueError
    Se o método informado não for reconhecido ou se o threshold for menor ou igual a zero.

    KeyError
        Se alguma coluna informada não existir no DataFrame.

    TypeError
        Se alguma coluna informada não for numérica.
    """

    df = data.copy()

    # Seleciona as colunas numéricas
    if columns is None:
        columns = df.select_dtypes(include=["number"]).columns.tolist()


    # Valida as colunas
    for col in columns:
        if col not in df.columns:
            raise KeyError(f"A coluna '{col}' não existe no DataFrame.")

        # Verifica se as colunas são numéricas
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise TypeError(f"A coluna '{col}' deve ser numérica")


    if threshold <= 0:
        raise ValueError("O threshold deve ser maior que zero.")
    
    # Verifica o método escolhido
    match method:
        case "iqr":

            for col in columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1

                lower_limit = Q1 - threshold * IQR
                upper_limit = Q3 + threshold * IQR

                df = df[(df[col] >= lower_limit) & (df[col] <= upper_limit)]

            return df
            

        case "zscore":

            for col in columns:
                mean = df[col].mean()
                std = df[col].std()

                z_scores = (df[col] - mean) / std

                df = df[z_scores.abs() <= threshold]

            return df
            
        case _:
            raise ValueError(f"Método '{method}' não reconhecido. Use 'iqr' ou 'zscore'.")
        



def clean_missing(
        data: pd.DataFrame,
        strategy: str = "drop",
        columns: list[str] | None = None,
        value: object | None = None,
        threshold: float | None = None,
        visualize: bool = False
    ) -> pd.DataFrame:
    
    """
    Trata valores ausentes em um DataFrame com diferentes estratégias.

    Parâmetros:
    - data: DataFrame do pandas.
    - strategy: Estratégia de tratamento. Pode ser 'drop', 'mean', 'median', 'mode', 'value' ou 'interpolate'.
    - columns: Lista de colunas a serem tratadas. Se None, serão escolhidas com base na estratégia.
    - value: Valor específico para preenchimento (usado apenas se strategy='value').
    - threshold: Proporção de valores ausentes para remover colunas (usado apenas com strategy='drop').
    - visualize: Se True, exibe o resumo de valores ausentes antes do tratamento.

    Retorna:
    - DataFrame com valores ausentes tratados.
    """

    df = data.copy()

    if columns is None:
        if strategy in ["mean", "median", "zscore"]:
            columns = df.select_dtypes(include=["number"]).columns
        elif strategy in ["mode", "value", "drop", "interpolate"]:
            columns = df.columns
        else:
            raise ValueError(f"Estratégia '{strategy}' não reconhecida.")

    match strategy:
        case "drop":
            if threshold is not None:
                
                df = df.loc[:, df.isnull().mean() < threshold]
            else:
                
                df = df.dropna(subset=columns)

        case "mean":
            for col in columns:
                df[col] = df[col].fillna(df[col].mean())

        case "median":
            for col in columns:
                df[col] = df[col].fillna(df[col].median())

        case "mode":
            for col in columns:
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode[0])

        case "value":
            if value is None:
                raise ValueError("Para a estratégia 'value', o parâmetro 'value' deve ser fornecido.")
            for col in columns:
                df[col] = df[col].fillna(value)

        case "interpolate":
            df[columns] = df[columns].interpolate()

        case _:
            raise ValueError(f"Estratégia '{strategy}' não reconhecida.")

    return df

            