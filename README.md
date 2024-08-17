# PyLTLParser

This python library could parse different kinds of LTLs used in different tools with customizable LTL tokens.
such as UPPAAL, XSTAMPP, ... etc

## Installation

(Will be deployed to pypi soon...)

```cmd
python -m pip install py_ltl_parser
```

## Packup

```python
pip wheel --wheel-dir ./dist .
```

## Usage

```python
ltl = "[] ((((controlAction==IncreasePower))->(((!((controlAction==IncreasePower)))U(((MyVar==Abnormal)))))))"
parsed = parse_ltl(ltl)
print(json.dumps(parsed.to_dict(), indent=2))
print(parsed.unparse())
```

The dumped json in line 3：

```json
{
  "operator": "[]",
  "operand": {
    "left": {
      "left": {
        "name": "controlAction"
      },
      "operator": "==",
      "right": {
        "name": "IncreasePower"
      }
    },
    "operator": "->",
    "right": {
      "left": {
        "operator": "!",
        "operand": {
          "left": {
            "name": "controlAction"
          },
          "operator": "==",
          "right": {
            "name": "IncreasePower"
          }
        }
      },
      "operator": "U",
      "right": {
        "left": {
          "name": "MyVar"
        },
        "operator": "==",
        "right": {
          "name": "Abnormal"
        }
      }
    }
  }
}
```

The printted LTL formula in line 4：

```cmd
[]controlAction==IncreasePower->!(controlAction==IncreasePower)UMyVar==Abnormal
```

## Parsing UPPAAL LTL Expression

```python
from py_ltl_parser import parse_uppaal_ltl
parsed = parse_uppaal_ltl(
    "(((ACE4==0)&&(ACE3==0)&&(ACE1==0)&&(ACE2==2)))--> (!((s==0)))"
)
print(parsed.to_dict())
```

## Development

```cmd
pip install autoflake black isort pytest
pytest -s
pip install build
python3 -m build
```
