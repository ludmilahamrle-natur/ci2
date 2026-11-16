import argparse
from pathlib import Path
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(
        description="Print names of compounds linked from a NIST HTML/XML file."
    )
    parser.add_argument("filename", help="path to the HTML or XML file to parse")
    args = parser.parse_args()

    html = Path(args.filename).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all(
        "a", href=lambda href: href and "/cgi/cbook.cgi" in href
    ):
        name = link.get_text(" ", strip=True)
        if name:
            print(name)


if __name__ == "__main__":
    main()
