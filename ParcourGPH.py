from scrapper import Scrapper, Course, convert_to_number
from sigles import sigles, Bac
from sys import exit

class Bacc():
    def __init__(self, bacc=[[] for i in range(8)]):
        self.bacc = bacc

    def add_course(self, tup):
        # bac grille 2D avec Bacc[session][cours]
        try:
            course, session = tup
        except(TypeError):
            print("Erreur détecté: ","add_course() s'attend a recevoir un tuple, exemple: (GEL_XXXX,1)")
            exit(1)
        self.bacc[session - 1].append(course)

    def look_for_conflict(self):
        print("Attention! les conflits avec les cours qui comporte des labos sont fréquents et susceptible de bugger")
        is_conflict = False
        for session in self.bacc:
            # Convertire les heures en chiffre, start_1 < stop_2 && start_1 > start_2 or
            # filter(session -> jour des cours )
            for c1 in session:
                for c2 in session:
                    if c1 == c2:
                        continue
                    for j1 in c1.horaire:
                        jour1 = j1.get("Journée")
                        if jour1 is None:
                            continue
                        else:
                            for j2 in c2.horaire:
                                jour2 = j2.get("Journée")
                                if jour2 is None:
                                    continue
                                else:
                                    if jour1 == jour2:
                                        sta1, sto1 = j1.get("Horaire")
                                        sta1, sto1 = (
                                            convert_to_number(sta1), convert_to_number(sto1))
                                        sta2, sto2 = j2.get("Horaire")
                                        sta2, sto2 = (
                                            convert_to_number(sta2), convert_to_number(sto2))
                                        if ((sta1 < sta2) and (sta2 < sto1)) or (
                                                (sta1 < sto2) and (sto2 < sto1)):
                                            is_conflict = True

                                            print(f"Session: {self.bacc.index(session) + 1}")
                                            print(
                                                f"Conflit entre {c1.sigle} et {c2.sigle}")
                                            print(
                                                f"jour: {jour1}\nheure: {j1.get('Horaire')} et {j2.get('Horaire')}")
                                    else:
                                        continue
        print("\n")
        if not is_conflict:
            print("*** Pas de conflit d'horaire décelé ***\n")

    def show_credit(self):
        total_credit = 0
        index_de_session = 1
        for session in self.bacc:
            credit_par_session = 0
            for cour in session:
                credit_par_session += int(cour.credit)
            print(
                f"session : {index_de_session} -> nombre de crédit : {credit_par_session}")
            total_credit += credit_par_session
            index_de_session += 1

        print(f"Crédit totaux: {total_credit}\n")


def into_course(listedeliste):
    """
    Retourne une liste de liste de sigles en liste de liste d'objet 'Cours'
    ex: coursX = Bacc[session][cours]
    """

    if type(listedeliste) == list:
        if type(listedeliste[0]) == list:
            res = [[] for i in listedeliste]
            for number, session in enumerate(listedeliste):
                res[number] = list(map(lambda x: Scrapper(x).into_Course(), session))
            return Bacc(res)
    elif type(listedeliste) == str:
        return Scrapper(listedeliste).into_Course()
    else:
        raise Exception("L'argument n'est pas un sigle, une liste de  sigle ou une liste de liste de sigle")


if __name__ == "__main__":
    """ Exemple! """
    gph = into_course(Bac)

    """ On ajoute un cours sur le fly ... IFT-4030 à la 9ième session """
    print(into_course("GEL-2003"))
    gph.add_course(into_course("GEL-2003"))
    gph.look_for_conflict()

    

