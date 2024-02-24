# Outils de gestion de cours UL
L'objet Bacc implémente différentes méthodes utiles
- look_for_conflict()
- show_credit()
- add_course()
- print(into_course("phy-1002")) donne les infos sur le cours phy-1002 par exemple!

Ces méthodes s'appliquent à un objet Bacc initialisé avec une liste de liste d'objet Course 
ex: `[[cours1, cours2, ...],..., [... ,cours_n-1, cours_n]]`

Rouler le programme `ParcourGPH.py` pour tester vos combos de cours!

Par exemple, on souhaite regarder les conflits pour les combos suivants:

`sigles.py`
``` 
S1 = ["phy-1001", "phy-1002", "gph-1000", "gmc-1000", "phy-1003", "GLO-1901"]
S2 = ["gph-2006", "phy-1004", "phy-1005", "phy-1007", "gel-1001"]
S3 = ["GMC-1002", "GML-1001", "GEL-2005", "PHY-2001", "GPH-1799", "GEL-4799"]
S4 = ["GMC-1003", "GMN-2900", "GPH-2004", "GPH-2005", "GPH-2104", "PHY-1006"]

S5 = ["GMC-3005", "STT-2920", "GPH-3004", "Phi-2910", "GEL-2001"]
S6 = ["GPH-2002", "GMC-2001", "GPH-3110", "GML-1001", "GEL-4201"]
S7 = ["GPH-3000", "IFT-4030", "GEL-3003", "GEL-4200"]
S8 = ["PHY-3003", "GPH-3001", "PHY-3500", "GEL-4202"]
E6_5 = ["PHI-3900", "ECN-2901"]
Bac = [S1] + [S2] + [S3] + [S4] + [S5] + [S6] + [E6_5] + [S7] + [S8]
```

`ParcourGPH.py`
```    """ Exemple! """
    gph = into_course(Bac)
    gph.look_for_conflict()
    gph.show_credit()
    """ On ajoute un cours sur le fly ... IFT-4030 à la 9ième session """
    print((into_course("IFT-4030")) # on affiche les infos obtenues sur le cours, pourquoi pas ?!
    gph.add_course((into_course("IFT-4030"),9))
    gph.look_for_conflict()
    gph.show_credit()
```

# TODO
- Implémenter une manière de "clear" la cache pour (un cours spécifique ou tous les cours) pour réinitialiser les infos d'un cours.
- Faire une interface graphique.
- Implémenter une vérification des préalables (les infos sont déja dans le json!) .. \[en cours\]
