
import pandas as pd
from jlprep import analyze_dataset


def test_analyze_dataset():
    df = pd.DataFrame({
        "idade": [20, 21, 22, None, 100],
        "classe": ["A", "A", "A", "A", "B"],
    })

    report = analyze_dataset(df, target="classe")

    types = {alert["type"] for alert in report["alerts"]}

    assert report["rows"] == 5
    assert "missing_values" in types
    assert "class_imbalance" in types
