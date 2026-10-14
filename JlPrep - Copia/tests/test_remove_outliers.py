import pandas as pd
from jlprep.cleaning import remove_outliers

def test_remove_outliers_iqr():
    df = pd.DataFrame({
        "idade": [10,12,11,13,100],
        "salario": [1000,1100,1050,1200,50000]
    })

    result = remove_outliers(df, method="iqr", columns=["idade", "salario"])

    assert 100 not in result["idade"].values
    assert 50000 not in result["salario"].values



def test_remove_outliers_zscore():
    df = pd.DataFrame({
        "idade": [10, 11, 12, 13, 100]
    })

    result = remove_outliers(df, method="zscore", threshold=1.5, columns=["idade"])

    assert 100 not in result["idade"].values