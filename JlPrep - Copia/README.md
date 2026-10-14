# jlprep

Biblioteca em Python para **análise e pré-processamento de dados** voltada para aplicações de Machine Learning.

A `jlprep` foi desenvolvida como parte de um **Trabalho de Conclusão de Curso (TCC)**, com foco na análise e melhoria da qualidade de dados utilizados em modelos de Machine Learning.

---

## Objetivo

A biblioteca busca centralizar etapas comuns do pré-processamento de dados, como:

* Limpeza de dados
* Codificação de variáveis categóricas
* Análise exploratória
* Avaliação da qualidade dos dados

Além disso, fornece **diagnósticos interpretáveis**, auxiliando na tomada de decisão antes do treinamento de modelos de Machine Learning.

---

## Contexto do TCC

Este projeto foi desenvolvido no contexto do tema:

> **Qualidade dos dados em Machine Learning (dados faltantes, desbalanceados e ruidosos)**

A proposta da `jlprep` é oferecer uma abordagem prática para identificação e tratamento desses problemas, reunindo funcionalidades essenciais em uma única biblioteca.

---

## Funcionalidades

### Limpeza de dados

* Remoção de valores duplicados
* Tratamento de valores faltantes
* Remoção de outliers

### Transformação

* Label Encoding
* One-Hot Encoding

### Exploração de dados

* Resumo estatístico do dataset
* Visualização da distribuição de valores

### Qualidade dos dados

* Verificação de inconsistências
* Análise de desbalanceamento de classes
* Sugestões de pré-processamento

---

## Instalação

Clone o repositório e acesse a pasta do projeto.

Em seguida, instale as dependências necessárias utilizando o arquivo `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

As principais dependências utilizadas pelo projeto são:

* `pandas`
* `matplotlib`
* `pytest`

---

## Testes

Os testes automatizados estão localizados na pasta `tests/`.

Para executar todos os testes, utilize:

```bash
python -m pytest
```

Para executar um teste específico:

```bash
python -m pytest tests/test_encode_onehot.py
```

---

## Exemplo de uso

```python
import pandas as pd

from jlprep import check_class_balance

df = pd.DataFrame({
    "classe": ["A", "A", "B", "B", "A"]
})

resultado = check_class_balance(
    df,
    target="classe"
)

print(resultado)
```

A função retorna um dicionário contendo informações sobre a quantidade de classes, o tipo de classificação, o nível de desbalanceamento e uma sugestão de tratamento.

---

## Estrutura do projeto

```text
JlPrep/
├── jlprep/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── encoding.py
│   ├── exploration.py
│   └── quality.py
│
├── tests/
│   ├── test_clean_missing.py
│   ├── test_encode_label.py
│   ├── test_encode_onehot.py
│   ├── test_remove_outliers.py
│   └── test_check_class_balance.py
│
├── examples/
├── requirements.txt
└── README.md
```

---

## Projeto acadêmico

A `jlprep` foi desenvolvida como parte de um Trabalho de Conclusão de Curso, com o objetivo de aplicar conceitos de programação em Python, pré-processamento de dados, qualidade de dados e testes automatizados em uma biblioteca voltada para aplicações de Machine Learning.
