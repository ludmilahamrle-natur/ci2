"""Convert ChemDraw CDXML structures to SMILES and MACCS bit lists."""


class CDXMLConverter:
    def __init__(self, arguments):
        self.arguments = arguments
        self.input_paths = []
        self.output_path = None
        self.output_mode = "w"

    def read_arguments(self):
        import glob
        from pathlib import Path

        seen = set()
        for argument in self.arguments:
            path = Path(argument)
            if path.suffix.lower() == ".csv":
                # Use the first CSV argument that does not already exist.
                if self.output_path is None and not path.exists():
                    self.output_path = path
                    self.output_mode = "x"
                continue

            # Accept both shell-expanded filenames and a quoted "*.cdxml".
            matches = [argument] if path.is_file() else sorted(glob.glob(argument))
            if not matches:
                raise ValueError(f"No input file matches: {argument}")
            for match in matches:
                input_path = Path(match)
                if input_path.suffix.lower() != ".cdxml" or not input_path.is_file():
                    raise ValueError(f"Expected a CDXML file: {match}")
                if input_path.resolve() not in seen:
                    self.input_paths.append(input_path)
                    seen.add(input_path.resolve())

        if not self.input_paths:
            raise ValueError("Usage: python3 cdxml2csv.py *.cdxml [output.csv]")
        if self.output_path is None:
            self.output_path = Path("cdxml2csv.csv")

    def read_molecules(self):
        import xml.etree.ElementTree as ET
        from openbabel import openbabel, pybel

        # Older releases can read CDXML with incorrect implicit hydrogens.
        version = tuple(int(part) for part in openbabel.OBReleaseVersion().split(".")[:3])
        if version < (3, 2, 1):
            raise ValueError("Open Babel 3.2.1 or newer is required; install requirements.txt.")

        rows = []
        for path in self.input_paths:
            # Reject malformed XML before Open Babel can return partial data.
            try:
                document = ET.parse(path)
            except ET.ParseError as error:
                raise ValueError(f"Invalid XML in {path}: {error}") from error
            if document.getroot().tag != "CDXML":
                raise ValueError(f"Not a CDXML document: {path}")
            found = False
            for mol in pybel.readfile("cdxml", str(path)):
                if mol.OBMol.NumAtoms() == 0:
                    raise ValueError(f"No atoms found in {path}")
                smiles = mol.write("smi").split()[0]
                bits = mol.calcfp("maccs").bits
                rows.append((path.name, smiles, bits))
                found = True
            if not found:
                raise ValueError(f"No readable molecule found in {path}")
        return rows

    def write_csv(self, rows):
        import csv

        with self.output_path.open(self.output_mode, encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter=";", lineterminator="\n")
            writer.writerow(("name", "smiles", "maccs"))
            writer.writerows(rows)

    @staticmethod
    def print_largest_fingerprint(rows):
        # Each list entry is the position of a set bit, so count its entries.
        largest = rows[0]
        for row in rows[1:]:
            if len(row[2]) > len(largest[2]):
                largest = row
        print(f"Most MACCS bits set: {largest[0]} ({len(largest[2])} bits)")

    def run(self):
        import csv
        import sys

        try:
            self.read_arguments()
            # Finish conversion before opening the output file for writing.
            rows = self.read_molecules()
            self.write_csv(rows)
            self.print_largest_fingerprint(rows)
            return 0
        except ImportError:
            print(
                "Error: Open Babel is required. Install it with: "
                "python3 -m pip install -r requirements.txt",
                file=sys.stderr,
            )
            return 1
        except (OSError, ValueError, RuntimeError, csv.Error) as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1

    @classmethod
    def main(cls):
        import sys

        converter = cls(sys.argv[1:])
        sys.exit(converter.run())


if __name__ == "__main__":
    CDXMLConverter.main()
