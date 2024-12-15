import bs4
import requests

class Scrapper:
    def __init__(self, url: str):
        self.response = requests.get(url, header={"User-Agent": "PaylessMusicApi/1.0 (Unknown; Unknown; Unknown)"})
        self.html = bs4.BeautifulSoup(self.response.text, "html.parser")