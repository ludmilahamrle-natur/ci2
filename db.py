"""Import world CSV files into SQLite and answer assignment question 2."""


class WorldDatabase:
    QUESTION = "What is the total population of Southern Europe?"

    def __init__(self, filenames):
        from pathlib import Path

        self.filenames = filenames
        self.database_path = Path(__file__).resolve().with_name("db.sqlite")

    @staticmethod
    def quote_identifier(name):
        """Quote a table or column name for use in an SQL statement."""
        if not name.strip() or "\x00" in name:
            raise ValueError("Table and column names must be nonempty and contain no NUL.")
        return '"' + name.replace('"', '""') + '"'

    def import_csv(self, connection, filename):
        import csv
        from pathlib import Path

        path = Path(filename)
        if path.suffix.lower() != ".csv":
            raise ValueError(f"Expected a CSV filename: {filename}")

        table_name = path.stem
        existing = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ? COLLATE NOCASE",
            (table_name,),
        ).fetchone()
        if existing:
            return

        with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            sample = csv_file.read(8192)
            csv_file.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel

            reader = csv.reader(csv_file, dialect, strict=True)
            columns = next(reader, None)
            if not columns:
                raise ValueError(f"{filename}: the CSV header is missing.")
            if len({column.lower() for column in columns}) != len(columns):
                raise ValueError(f"{filename}: the CSV header contains duplicate names.")

            table = self.quote_identifier(table_name)
            fields = ", ".join(
                self.quote_identifier(column) + " TEXT" for column in columns
            )
            connection.execute(f"CREATE TABLE {table} ({fields})")

            placeholders = ", ".join("?" for column in columns)
            connection.executemany(
                f"INSERT INTO {table} VALUES ({placeholders})",
                self.read_rows(reader, len(columns), filename),
            )

    @staticmethod
    def read_rows(reader, column_count, filename):
        """Validate records before SQLite inserts them; ignore empty lines."""
        for row in reader:
            if not row:
                continue
            if len(row) != column_count:
                raise ValueError(
                    f"{filename}, line {reader.line_num}: expected "
                    f"{column_count} fields, found {len(row)}."
                )
            yield row

    def print_answer(self, connection):
        # CSV values are stored as text, so convert population values for SUM.
        answer = connection.execute(
            """
            SELECT COALESCE(SUM(CAST(c.Population AS INTEGER)), 0)
            FROM country AS c
            WHERE c.Region = ?
            """,
            ("Southern Europe",),
        ).fetchone()[0]
        print(self.QUESTION)
        print(f"Answer: {answer}")

    def run(self):
        import csv
        import sqlite3
        import sys

        connection = None
        try:
            if not self.filenames and not self.database_path.is_file():
                raise ValueError(
                    "db.sqlite does not exist yet. First run: "
                    "python3 db.py country.csv"
                )

            connection = sqlite3.connect(self.database_path)
            with connection:
                # Include CREATE TABLE in the transaction, so a failed import
                # cannot leave a partly populated table behind.
                connection.execute("BEGIN")
                for filename in self.filenames:
                    self.import_csv(connection, filename)

            self.print_answer(connection)
            return 0
        except (OSError, UnicodeError, ValueError, csv.Error, sqlite3.Error) as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        finally:
            if connection is not None:
                connection.close()

    @classmethod
    def main(cls):
        import sys

        database = cls(sys.argv[1:])
        sys.exit(database.run())


if __name__ == "__main__":
    WorldDatabase.main()
