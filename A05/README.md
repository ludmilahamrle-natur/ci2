# A05 - Cheminformatics
This script reads ChemDraw CDXML files and writes CSV with three columns: name, smiles, maccs.

## How to run the program
### 1. Clone the repository
```git clone https://github.com/ludmilahamrle-natur/ci2.git```

```cd ci2/A05```
### 2. Create enviroment + install requirements
```python3 -m venv .venv```

```source .venv/bin/activate```

```python3 -m pip install -r requirements.txt```
### 3. Run the script
```python3 cdxml2csv.py *.cdxml```
