import warnings
import spacy
from queue import PriorityQueue
from WikiNode import WikiNode

warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)
nlp = spacy.load("en_core_web_lg")

def h_func_1(txt1: WikiNode, txt2: WikiNode) -> float:
    global nlp
    txt_1 = nlp(txt1.title)
    url_1 = nlp(txt1.url)
    txt_2 = nlp(txt2.title)
    url_2 = nlp(txt2.url)
    # print(txt1.title, "and", txt2.title)
    if(txt1.title == "" or txt2.title == ""):
        print(txt1.url, txt2.url)
    return round(abs(1 - txt_1.similarity(txt_2)), 5)

class BnBSolver(object):
    def __init__(self, start: str, end: str, h_func) -> None:
        self.start = WikiNode(start)
        self.start.parse_page()
        self.end = WikiNode(end)
        self.end.parse_page()
        self.heuristic = h_func
        self.prio_queue = PriorityQueue()
        self.opened = {}
        self.enqueue(self.start)
        self.visit_counter = 0
    
    def enqueue(self, node) -> None:
        if not self.opened.setdefault(node.url, False):
            rating = self.heuristic(node, self.end)
            self.prio_queue.put((rating, node))
    
    def dequeue(self) -> WikiNode:
        res = self.prio_queue.get()
        self.opened.setdefault(res[1].url, True)
        return res
    
    def solve(self):
        if self.prio_queue.empty():
            return None
        else:
            curr = self.dequeue()
            curr_page = curr[1]
            
            self.visit_counter += 1
            print(f"[{self.visit_counter}] Visiting {curr_page.title} at {curr_page.url}")

            if(curr_page == self.end):
                return curr_page
            else:
                curr_page.parse_page()
                for curr_child in curr_page.children:
                    self.enqueue(curr_child)
                return self.solve()


if __name__ == "__main__":
    # Tests Examples
    # Cat -> Computer
    # Banana -> Knife
    # Batik -> Banana
    # Computer_keyboard -> Bucket
    # Plastic -> Calculator
    # Spoon -> Cartoons
    
    start_link = "https://en.wikipedia.org/wiki/Spoon"
    end_link   = "https://en.wikipedia.org/wiki/Cartoons"

    solver = BnBSolver(start_link, end_link, h_func_1)
    print("=== SOLVING ===")
    solution = solver.solve()

    print("=== PATH ===")
    print(solution.parse_path())
