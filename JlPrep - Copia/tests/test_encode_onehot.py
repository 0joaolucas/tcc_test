import pandas as pd
import pytest
from jlprep.encoding import encode_onehot

def test_encode_onehot_basic():
    df = pd.DataFrame({
        "cor": ["azul", "verde"],
        "idade": [10,20]
    })

    result = encode_onehot(df)

    expected = pd.DataFrame({
        "idade": [10,20],
        "cor_azul": [1,0],
        "cor_verde": [0,1]
    })

    pd.testing.assert_frame_equal(result, expected)