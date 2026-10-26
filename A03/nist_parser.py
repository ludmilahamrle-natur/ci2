from bs4 import BeautifulSoup

with open("nist_benzidine.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

for a in soup.find_all("a", href=True):
    if "/cgi/cbook.cgi" in a["href"]:
        print(a.get_text(strip=True))