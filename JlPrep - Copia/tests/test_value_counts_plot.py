import pandas as pd
from jlprep.exploration import value_counts_plot


def test_value_counts_plot_basic():
    df = pd.DataFrame({
        "cor": ["azul", "verde", "azul", "vermelho"]
    })

    result = value_counts_plot(df, column="cor")

    assert result is None