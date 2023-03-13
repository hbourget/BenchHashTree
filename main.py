import random
import time
import matplotlib.pyplot as plt
from arbre import *
from hashTable import *

if __name__ == '__main__':
    def test_abr():
        arbre = ABR()
        assert arbre.racine is None
        # Test d'insertion
        arbre.insert(8)
        arbre.insert(3)
        arbre.insert(10)
        arbre.insert(1)
        arbre.insert(6)
        arbre.insert(14)
        arbre.insert(4)
        arbre.insert(7)
        arbre.insert(13)
        assert arbre.racine.data == 8
        assert arbre.racine.filsGauche.data == 3
        assert arbre.racine.filsDroit.data == 10
        assert arbre.racine.filsGauche.filsGauche.data == 1
        assert arbre.racine.filsGauche.filsDroit.data == 6
        assert arbre.racine.filsDroit.filsDroit.data == 14
        assert arbre.racine.filsGauche.filsDroit.filsGauche.data == 4
        assert arbre.racine.filsGauche.filsDroit.filsDroit.data == 7
        assert arbre.racine.filsDroit.filsDroit.filsGauche.data == 13

        # Test de recherche
        assert arbre.exist(6) is True
        assert arbre.exist(11) is False

        # Test d'affichage
        print("\n\nAffichage de l'arbre de base :")
        arbre.afficher_base()

        print("\n\nAffichage Infixe :")
        arbre.afficher_infixe()

        print("\n\nAffichage Prefixe :")
        arbre.afficher_prefixe()

        # Test de suppression
        arbre.supprimer(6)
        print("\n\nAffichage de l'arbre de base apres suppression de 6 :")
        assert arbre.exist(6) is False
        arbre.afficher_base()

        # Test d'union
        # Ajout de valeurs dans l'autre arbre qui ne sont presentes dans l'arbre de base 
        autre_arbre = ABR()
        autre_arbre.insert(5)
        autre_arbre.insert(2)
        autre_arbre.insert(9)

        nouvel_arbre = arbre.union(autre_arbre)
        assert nouvel_arbre.exist(5) is True
        assert nouvel_arbre.exist(2) is True
        assert nouvel_arbre.exist(9) is True
        print("\n\nAffichage de l'union de l'arbre et de l'autre_arbre :")
        nouvel_arbre.afficher_base()

        # Test d'intersection
        # Ajout de valeurs dans l'autre arbre qui sont presentes dans l'arbre de base 
        autre_arbre.insert(8)
        autre_arbre.insert(10)
        autre_arbre.insert(7)
        nouvel_arb = arbre.intersection(autre_arbre)
        assert nouvel_arbre.exist(8) is True
        assert nouvel_arbre.exist(10) is True
        assert nouvel_arbre.exist(7) is True
        print("\n\nAffichage de l'intersection de l'arbre et de l'autre_arbre :")
        nouvel_arb.afficher_base()

        # Test de hauteur
        assert arbre.height() == 4

        # Test de suppression totale
        print("\n**Clear de l'arbre**")
        arbre.clear()
        assert arbre.racine is None

        print("\n---------------------\n")

    def test_hachage():
        # Test de la classe Table
        table = Table(hash_table_size=10, hash_function=hachage_modulo, hash_function_2=hachage_modulo_2,
                      rehash_type='linear')

        # Insérer des valeurs dans la table
        table.insert(1, "A")
        table.insert(3, "B")
        table.insert(4, "C")
        table.insert(11, "D")
        table.insert(21, "E")

        print("\nAffichage de la table\n")
        table.affichage()
        # Vérifier que les valeurs ont été correctement insérées
        assert table.exist(1) == True
        assert table.exist(3) == True
        assert table.exist(4) == True
        assert table.exist(11) == True
        assert table.exist(21) == True

        # Insérer une valeur avec la même clé pour forcer un rehachage linéaire
        table.insert(21, "F")

        # Vérifier que la valeur a été mise à jour
        assert table.value(21) == "F"
        # Vérifier que le rehachage a été effectué pour la clé 21
        assert table.rehash_count.get(21, 0) == 2

        print("\nAffichage de la table avec la clé 21 mise à jour\n")
        table.affichage()

        print("\nAffichage de la table avec la clé 21 supprimée\n")
        table.delete(21)
        table.affichage()

        # On verifie que le compteur d'une clé supprimé est bien remis à 0 après une suppression.
        table.insert(21, "G")
        assert table.value(21) == "G"
        assert table.rehash_count.get(21, 0) == 1

        # Création des tables
        table1 = Table(hash_table_size=10, hash_function=hachage_modulo, hash_function_2=hachage_modulo_2,
                       rehash_type='linear')
        table1.insert(1, 'A')
        table1.insert(2, 'B')
        table1.insert(3, 'C')

        table2 = Table(hash_table_size=10, hash_function=hachage_modulo, hash_function_2=hachage_modulo_2,
                       rehash_type='linear')
        table2.insert(3, 'D')
        table2.insert(4, 'E')
        table2.insert(5, 'F')

        print("\nAffichage d'une union de la table1 et de la table2 - [1,A ; 2,B ; 3,C + 3,D ; 4,E ; 5,F\n")
       
        # Union des tables
        union_table = table1.union(table2)
        union_table.affichage()
        assert union_table.value(1) == 'A'
        assert union_table.value(2) == 'B'
        assert union_table.value(3) == 'C'
        assert union_table.value(4) == 'E'
        assert union_table.value(5) == 'F'
        assert union_table.hash_table_size == 10

        print("\nAffichage d'une intersection de la table1 et de la table2 - [1,A ; 2,B ; 3,C + 3,D ; 4,E ; 5,F\n")
        
        # Intersection des tables
        intersection_table = table1.intersection(table2)
        intersection_table.affichage()
        assert intersection_table.value(3) == 'C'
        assert not intersection_table.exist(1)
        assert not intersection_table.exist(2)
        assert not intersection_table.exist(4)
        assert not intersection_table.exist(5)
        assert intersection_table.hash_table_size == 10

    def perf_abr(nbEssais, nbValAbr, nbValRecherche, maxInterRercherche):
        print("\nTests de performances ABR :\n")
        # Ajout de 500 valeurs aléatoires
        # Récupération de la hauteur de l'arbre
        total_temps = 0
        total_height = 0
        timesAbr = []
        for i in range(nbEssais):
            abr = ABR()
            for k in range(nbValAbr):
                abr.insert(random.randint(0, maxInterRercherche))
            height = abr.height()
            total_height = total_height + height

            start = time.time()
            for j in range(nbValRecherche):
                abr.exist(random.randint(0, maxInterRercherche))
            end = time.time()
            elapsed = end - start
            total_temps = total_temps + elapsed
            timesAbr.append(elapsed)
            print("Hauteur de l'arbre: " + height.__str__() + " - " + "%.5f" % elapsed + " secondes pour rechercher " + nbValRecherche.__str__() + " valeurs comprises entre 0 et "+ maxInterRercherche.__str__() +"")

        print("\nPour " + nbEssais.__str__() + " essais, le temps de recherche moyen pour " + nbValRecherche.__str__() + " valeurs, comprise entre 0 et "+ maxInterRercherche.__str__() +" dans un arbre de hauteur moyenne " + (total_height // nbEssais).__str__() + " comprenant des valeurs entre 0 et "+ maxInterRercherche.__str__() +", pour " + nbEssais.__str__() + " essais est de " + "{:.5f}".format(total_temps / nbEssais).__str__() + " secondes")
        return total_height ,timesAbr
    
    def perf_hachage(nbEssais, tailleTable, nbValRecherche, maxInterRercherche):
        print("\nTest des performances du temps de recherche Table de Hachage\n")
        # Fonction pour mesurer le temps de recherche d'une clé dans une table
        timesHash = []
        def profile_temps(table_mesure, nbEssais):
            total = 0
            for i in range(nbEssais):
                start = time.time()
                for j in range(nbValRecherche):
                    table_mesure.exist(random.randint(0, maxInterRercherche))
                end = time.time()
                elapsed = end - start
                print("Temps essai " + i.__str__() + ": " + "{:.5f}".format(elapsed) + " secondes")
                total = total + elapsed
                timesHash.append(elapsed)
            return total / nbEssais

        # Insertion de 10000 éléments dans la table
        table_mesure = Table(tailleTable)
        for i in range(tailleTable):
            table_mesure.insert(random.randint(0, maxInterRercherche), str(i))

        # Mesure du temps de recherche pour une clé aléatoire
        print("Le temps moyen de recherche de " + nbValRecherche.__str__() + " éléments dans une table de hachage de taille "+ maxInterRercherche.__str__() +" comprenant des valeurs comprises entre 0 et "+ maxInterRercherche.__str__() +", pour " + nbEssais.__str__() + " essais, est de : " + "{:.5f}".format(profile_temps(table_mesure, nbEssais)) + " secondes")
        return timesHash

    def draw(typeStruct, times, nbValRecherche, maxInterRercherche, nbEssais, total_height, tailleTable):
        if typeStruct == "abr":
            plt.plot(times)
            plt.xlabel('Essai')
            plt.ylabel('Temps d\'exécution (secondes)')
            plt.title('Temps moyen de recherche de ' + nbValRecherche.__str__() + ' elements dans un ABR H±' + (total_height // nbEssais).__str__())
            plt.show()
        else:
            plt.plot(times)
            plt.xlabel('Essai')
            plt.ylabel('Temps d\'exécution (secondes)')
            plt.title('Temps moyen de recherche de ' + nbValRecherche.__str__() + ' elements dans une hashtable t=' + tailleTable.__str__())
            plt.show()

    def drawCompare(timesHash, timesAbr, nbValRecherche):
        plt.plot(timesAbr, 'b', label='Temps ABR')
        plt.plot(timesHash, 'r', label='Temps table hachage')
        plt.xlabel('Essai')
        plt.ylabel('Temps d\'exécution (secondes)')
        plt.title('Temps moyen de recherche de ' + nbValRecherche.__str__() + ' elements pour un ABR et une hashtable')
        plt.legend()
        plt.show()

    nbValRecherche = 100000
    maxInterRercherche = 10000
    nbEssais = 15
    nbValAbr = 500
    tailleTable = 1000
    
    test_abr()
    test_hachage
    total_height, timesAbr = perf_abr(nbEssais, nbValAbr, nbValRecherche, maxInterRercherche)
    timesHash = perf_hachage(nbEssais, tailleTable, nbValRecherche, maxInterRercherche)
    draw("abr", timesAbr, nbValRecherche, maxInterRercherche, nbEssais, total_height, None)
    draw("hash", timesAbr, nbValRecherche, maxInterRercherche, nbEssais, None, tailleTable)
    drawCompare(timesHash, timesAbr, nbValRecherche)