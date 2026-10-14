import pandas as pd
from jlprep.encoding import encode_label

def test_encode_label_basic():
    df = pd.DataFrame({
        "cor": ["azul", "verde", "azul"],
        "idade": [10,20,30]
    })

    result = encode_label(df.copy(), columns=["cor"])

    expected = pd.DataFrame({
        "cor": [0, 1, 0],
        "idade": [10, 20, 30]
    })

    pd.testing.assert_frame_equal(result, expected)