import csv 
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    folder = Path(__file__).resolve().parent
    csv_path = folder / "graph.csv"
    image_path = folder / "graph.png"

    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != ["x", "y"]:
            raise ValueError("graph.csv must have exactly the columns x and y.")
        rows = list(reader)

    if len(rows) < 20:
        raise ValueError("graph.csv must contain at least 20 data rows.")
    try:
        x = np.array([float(row["x"]) for row in rows])
        y = np.array([float(row["y"]) for row in rows])
    except (TypeError, ValueError) as error:
        raise ValueError("All x and y values in graph.csv must be numbers.") from error

    if not np.allclose(y, np.square(x)):
        raise ValueError("Every y value in graph.csv must equal x squared.")

    figure, axes = plt.subplots()
    axes.plot(x, y, marker="o", color="royalblue")
    axes.set_title("The square function")
    axes.set_xlabel("x")
    axes.set_ylabel("y = x²")
    axes.grid(True, alpha=0.35)
    figure.tight_layout()
    figure.savefig(image_path, dpi=150)
    plt.close(figure)


if __name__ == "__main__":
    main()
