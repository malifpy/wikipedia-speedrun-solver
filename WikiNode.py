import re
import requests
from bs4 import BeautifulSoup

class WikiNode(object):
    def __init__(self, url : str, title : str = "", visited_links = None, parent = None):
        self.url : str = url
        self.title : str = title

        if visited_links == None:
            self.memo = {}
        else:
            self.memo = visited_links

        self.parent = parent
        self.children : set(WikiNode) = set()

    def verify_url(self) -> bool:
        """
        Mem-verifikasi url wikipedia
        """
        page = requests.get(self.url)
        self.url = page.url

    def parse_page(self):
        """
        mem-parse halaman dari url self
        """

        PAGE_RAW     = requests.get(self.url)
        self.url = PAGE_RAW.url

        if PAGE_RAW.status_code == 200:
            soup = BeautifulSoup(PAGE_RAW.content, "html.parser")
            self.title = soup.find("h1", id="firstHeading").get_text()

            body = soup.find("div", id="bodyContent")
            
            for tr in body.find_all(style=True):
                if "display:none" in tr.get("style"):
                    tr.extract()
            
            for t in body.find_all(lambda t: t.name == 'a' and t.get_text(strip=True) != ""):
                link_url = t.get("href")
                if link_url and re.match(u"\/wiki\/\w+$", link_url):
                    full_url = "https://en.wikipedia.org" + link_url
                    if full_url not in self.memo:
                        self.memo[full_url] = WikiNode(full_url, visited_links=self.memo, parent=self, title=t.get_text())
                    page = self.memo[full_url]
                    self.children.add(page)
        else:
            print("Error")

    def __str__(self) -> str:
        return f"{self.title} [{self.url}]"
    
    def __hash__(self) -> int:
        return hash(self.url)
    
    def __eq__(self, other):
        if isinstance(other, WikiNode):
            return (self.url == other.url)
        else:
            return False
    
    def __lt__(self, other):
        if isinstance(other, WikiNode):
            return self.url == other.url
        else:
            return False
    
    def parse_path(self):
        if self.parent == None:
            return str(self)
        else:
            return self.parent.parse_path() + "\n" + str(self)


# For debugging
if __name__ == "__main__":
    start_link = WikiNode("https://en.wikipedia.org/wiki/Argentina")
    start_link.parse_page()
    print(start_link)
