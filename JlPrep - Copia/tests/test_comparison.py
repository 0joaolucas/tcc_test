
import pandas as pd
from jlprep import compare_datasets


def test_compare_datasets():
    original = pd.DataFrame({
        "idade": [20, None, 30],
        "cidade": ["A", "B", "C"],
    })

    processed = original.fillna({"idade": 25})

    report = compare_datasets(original, processed)

    assert report["before"]["missing_values"] == 1
    assert report["after"]["missing_values"] == 0
    assert report["changes"]["row_difference"] == 0
