from bs4 import BeautifulSoup
import requests


class Extractor:
    def __init__(self, url):
        self.url = url
        self.name = self.get_name()
        self.results = self.get_info()

    def get_name(self):
        return self.url.strip().split('/')[-1]

    def get_info(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, features="lxml")
        cells = soup.find_all('div', attrs= {'class': "table-cell"})
        results = []
        for cell in cells:
            answer = cell.find('div', attrs={"class": "answer"})
            question = cell.find('div', attrs={"class": "question"})
            if answer is not None and question is not None:
                results.append((answer.text, question.text))
        return results

    def write(self):
        while ('', '') in self.results:
            self.results.remove(('', ''))
        with open(self.name + ".txt", "w+") as file:
            for word in self.results:
                print(word)
                file.write(word[0] + ":" + word[1] + "\n\n")


if __name__ == "__main__":
    url_input = input("URL of Jeopardy game: ")  # https://jeopardylabs.com/
    extractor = Extractor(url=url_input)
    extractor.write()
