# A07 - POV-Ray
etoh6.pov places six ethanol molecules at the vertices of a regular hexagon. The molecular coordinates were generated from the SMILES structure with Open Babel.
## How to run the program
### 1. Clone the repository
```git clone https://github.com/ludmilahamrle-natur/ci2.git```

```cd ci2/A07```

### 2. Create enviroment + install requirements
```python3 -m venv .venv```

```source .venv/bin/activate```

```python3 -m pip install openbabel-wheel==3.2.1.23```

```sudo apt update```

```sudo apt install povray```

### 3. Convert and render
```obabel etoh.smi -0 etoh-generated.pov --gen3D```

```povray +etoh6.pov +0etoh6.png +W1200 +H1200 +FN +A -D```

Image is saved as etoh6.png.
