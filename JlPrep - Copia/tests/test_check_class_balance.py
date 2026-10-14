import pandas as pd
import pytest
from jlprep.quality import check_class_balance

# def test_check_class_balance_binary():
#     df = pd.DataFrame({
#         "classe": [0, 0, 1, 1, 1]
#     })

#     result = check_class_balance(df, target="classe")

#     assert result["n_classes"] == 2
#     assert result["problem_type"] == "Binary classification"
#     assert result["imbalance_ratio"] == 3 / 2


# def test_check_class_balance_multiclass():
#     df = pd.DataFrame({
#         "classe": [0, 0, 1, 2, 2, 2]
#     })

#     result = check_class_balance(df, target="classe")

#     assert result["n_classes"] == 3
#     assert result["problem_type"] == "Multiclass classification"
#     assert result["imbalance_ratio"] == 3 / 1


# def test_check_class_balance_missing_column():
#     df = pd.DataFrame({
#         "classe": [0, 1, 1]
#     })

#     with pytest.raises(KeyError):
#         check_class_balance(df, target="inexistente")


def test_check_class_balance_single_class():
    df = pd.DataFrame({
        "classe": [0, 0, 0]
    })

    with pytest.raises(ValueError):
        check_class_balance(df, target="classe")