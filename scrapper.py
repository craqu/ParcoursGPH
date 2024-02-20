#!/bin/python3
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup as bs
from random import choice
from Agents import agents
import json

"""
TODO
- regler probleme avec circuit logique pour conflit d'horaire
"""


class Course():
    def __init__(self, scrapper):
        self.name = scrapper.name
        self.sigle = scrapper.sigle
        self.preliminary = scrapper.preliminary
        self.horaire = scrapper.horaire
        self.session = scrapper.session
        self.mode = scrapper.mode
        self.credit = scrapper.credit

    def __repr__(self):
        res = f"{'Sigle:':<10}{self.sigle:<25}\n{'Nom:':<10}{self.name:<25}\n"
        if self.preliminary:
            res += f"{'Préalable:':<10}\n"
            for index, obj in enumerate(self.preliminary):
                res += f"{obj} ET "
                if index == len(self.preliminary) - 1:
                    res = res[:-4]
        res += "\n" f"session {self.session}" + "\n" + f"{'Horaire':^25}"
        for jour in self.horaire:
            try:
                res += "\n" + \
                    f"""{jour["Journée"]:<10}  {jour["Horaire"][0]} à {jour["Horaire"][1]}"""
            except(KeyError):
                res += "\n" + "À distance"
        return res + "\n\n"

    def Warning(self):
        pr = self.preliminary
        wn = []
        if pr and any([(("*" in i) or ("!" in i)) for i in pr]):
            temp = filter(lambda i: (("*" in i) or ("!" in i)), pr)
            wn += temp
            print(
                f"Attention, vous devrez contacter la gestion des étude pour lever les préalable de {wn}")


class Scrapper():
    UL = "https://www.ulaval.ca/"

    def __init__(self, sigle):
        self.sigle = sigle.upper()
        self.agent = choice(agents)
        if self.get_cache():
            pass
        else:
            self.preliminary = []
            self.get_page_info()  # initialise credit and modes_enseignement
            self.credit  # nombre de crédit du cours
            self.session = []  # automne et/ou hiver +
            # {jour:"jour de la semaine", "heure":(heure début, heure fin)} +
            self.horaire = []
            self.initialise_attributes()  # initialise agenda
            self.write_to_cache()

    def initialise_attributes(self):  # session, horaire, mode_enseignement
        # premier element de la liste affin d'avoir la dernière version
        page = self.page.find(
            "div", class_="fe--horaire fe--section-contenu--transparent")
        session_sub = page.findAll("p", class_="controls-title")
        self.session = list(
            set([i.strong.text[:-2].split()[0] for i in session_sub]))
        hor = page.findAll("div", class_="toggle-section")[0]
        for ul in hor.findAll(
                "ul", class_="section-cours--liste liste-elements--vertical"):
            temp = {}
            for li in ul.findAll("li", class_="section-cours--etiquette"):
                k, v = li.text.split(":")
                if k == "Journée":
                    res = v.strip()
                    temp[k] = res
                elif k == "Horaire":
                    res = (v.strip().split()[1], v.strip().split()[-1])
                    temp[k] = res
                else:
                    continue
            self.horaire.append(temp)

    def get_page_info(self):
        params = {"search": self.sigle}
        API_url = self.UL + "etudes/cours?" + urlencode(params)
        page = requests.post(
            API_url,
            headers={
                "User-Agent": self.agent,
                "Referer": 'https://www.google.com/'},
            timeout=4,
        )
        cours = bs(
            page.text,
            'html.parser').find(
            id="resultats").find_all(
            "div",
            class_="cours-element carte-accessible")
        for cour in cours:
            href = [
                i for i in cour.find_all(
                    "a",
                    href=True) if i.find(
                    "span",
                    class_="cours-element--sigle").text == self.sigle]
            if href:
                break
        mypage = bs(
            requests.get(
                self.UL +
                href[0]["href"]).text,
            'html.parser')
        soup = mypage.find(id="main-content")
        self.page = soup
        name = soup.find("span", class_="fe--titre-nom").text
        try:
            prea = soup.find("div",
                             class_="fe--prealables fe--section-contenu--fond").find("p",
                                                                                     class_="etiquette-container")
            prelim = [i.strip() for i in prea.text.split("ET")]
            self.preliminary = prelim
        except(AttributeError):
            #print(f"no preliminary found for {self.sigle}")
            pass
        self.name = name
        p = soup.find('ul', class_="fe--faits-rapides")
        try:
            credit = p.find("span", class_="promo-entete--titre").text
            self.credit = credit
        except(AttributeError):
            self.credit = "0"
        mode = p.find(
            "li",
            class_="fe--bloc-promo carte-meta carte-meta--ombre carte-accessible").findAll(
            "ul",
            class_="promo-entete--contenu liste-elements--vertical")
        self.mode = [i.strong.text for i in mode]

    def write_to_cache(self):
        f = open("cache.json", "r", encoding='utf-8')
        d = json.loads(f.read())
        f.close()
        with open("cache.json", "w", encoding='utf-8') as f:
            d.append(Course(self).__dict__)
            json.dump(d, f, indent=4)

    def get_cache(self) -> bool:
        f = open("cache.json", "r", encoding='utf-8')
        data = json.loads(f.read())
        f.close()
        cached = next((i for i in data if i.get("sigle") == self.sigle), False)
        if cached:
            self.preliminary = cached["preliminary"]
            self.credit = cached["credit"]
            self.name = cached["name"]
            self.session = cached["session"]
            self.horaire = cached["horaire"]
            self.mode = cached["mode"]
            return True
        return False

    def into_Course(self) -> Course:
        return Course(self)


def convert_to_number(weird):
    hour, minute = weird.split("h")
    try:
        hour = int(hour)
    except BaseException:
        hour = 0
    try:
        minute = int(minute) / 60
    except BaseException:
        minute = 0
    time = hour + minute
    return time


if __name__ == "__main__":
    test = Scrapper("phy-1001")
