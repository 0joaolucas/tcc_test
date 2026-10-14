import pandas as pd
from jlprep.cleaning import clean_missing


def test_clean_missing_drop():
    df = pd.DataFrame({
        "nome": ["João", None, "Maria"],
        "idade": [20, 25, None]
    })

    result = clean_missing(df, strategy="drop")

    assert result.isna().sum().sum() == 0
    assert len(result) == 1