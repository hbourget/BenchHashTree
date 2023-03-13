
class ABR:
    def __init__(self):
        self.racine = None

    class Node:
        def __init__(self, data):
            self.data = data
            self.filsDroit = None
            self.filsGauche = None

    # Verifie si une valeur est présente dans l'arbre - récursif
    def _exist(self, valeur):
        if self.racine is None:
            return False
        compteur = 0
        current_node = self.racine
        while current_node is not None:
            compteur = compteur + 1
            if current_node.data == valeur:
                return True
            elif valeur < current_node.data:
                current_node = current_node.filsGauche
            else:
                current_node = current_node.filsDroit

        return False

    def exist2(self, valeur):
        ret = self._exist(valeur)
        if ret:
            print("La valeur " + valeur.__str__() + " existe dans cet arbre.")
        else:
            print("La valeur " + valeur.__str__() + " n'existe pas dans cet arbre.")
    
    # Verifie si une valeur est présente dans l'arbre - récursif
    def exist(self, valeur):
        ret = self._exist(valeur)
        if ret:
            return True
        else:
            return False

    # Inserer une valeur dans l'arbre
    def insert(self, valeur):
        nouveau_noeud = ABR.Node(valeur)

        if self.racine is None:
            self.racine = nouveau_noeud
            return

        current_node = self.racine
        while True:
            if valeur < current_node.data:
                if current_node.filsGauche is None:
                    current_node.filsGauche = nouveau_noeud
                    return
                else:
                    current_node = current_node.filsGauche
            else:
                if current_node.filsDroit is None:
                    current_node.filsDroit = nouveau_noeud
                    return
                else:
                    current_node = current_node.filsDroit

    # Afficher l'arbre sous forme d'arbre - recursif
    def afficher_base(self):
        self._afficher_base_rec(self.racine, 0)

    def _afficher_base_rec(self, node, niveau):
        if node is not None:
            self._afficher_base_rec(node.filsDroit, niveau + 1)
            print(" " * 4 * niveau + str(node.data))
            self._afficher_base_rec(node.filsGauche, niveau + 1)

    # Afficher l'infixe de l'arbre - recursif
    def afficher_infixe(self):
        self._afficher_infixe_rec(self.racine)

    def _afficher_infixe_rec(self, node):
        if node is not None:
            self._afficher_infixe_rec(node.filsGauche)
            print(node.data, end=" ")
            self._afficher_infixe_rec(node.filsDroit)

    # Afficher le prefixe de l'arbre - recursif
    def afficher_prefixe(self):
        self._afficher_prefixe_rec(self.racine)

    def _afficher_prefixe_rec(self, node):
        if node is not None:
            print(node.data, end=" ")
            self._afficher_prefixe_rec(node.filsGauche)
            self._afficher_prefixe_rec(node.filsDroit)

    # Supprimer une valeur de l'arbre - recursif
    def supprimer(self, data):
        self.racine = self._supprimer_rec(data, self.racine)

    def _supprimer_rec(self, data, node):
        if node is None:
            return None
        if data < node.data:
            node.filsGauche = self._supprimer_rec(data, node.filsGauche)
        elif data > node.data:
            node.filsDroit = self._supprimer_rec(data, node.filsDroit)
        else:
            if node.filsGauche is None and node.filsDroit is None:
                node = None
            elif node.filsGauche is None:
                node = node.filsDroit
            elif node.filsDroit is None:
                node = node.filsGauche
            else:
                successeur = self._minimum(node.filsDroit)
                node.data = successeur.data
                node.filsDroit = self._supprimer_rec(successeur.data, node.filsDroit)
        return node

    # Afficher la valeur minimum de l'arbre - recursif
    def _minimum(self, node):
        while node.filsGauche is not None:
            node = node.filsGauche
        return node

    # Afficher l'union de 2 arbres - recursif
    def union(self, autre_abr):
        nouvel_arbre = ABR()
        self._union(nouvel_arbre, self.racine)
        self._union(nouvel_arbre, autre_abr.racine)
        return nouvel_arbre

    def _union(self, nouvel_arbre, node):
        if node is not None:
            if not nouvel_arbre._exist(node.data):
                nouvel_arbre.insert(node.data)
            self._union(nouvel_arbre, node.filsGauche)
            self._union(nouvel_arbre, node.filsDroit)

    # Afficher l'intersection de 2 arbres - recursif
    def intersection(self, autre_abr):
        nouvel_arb = ABR()
        self._intersection(nouvel_arb, self.racine, autre_abr)
        return nouvel_arb

    def _intersection(self, nouvel_arb, node, autre_abr):
        if node is not None:
            if autre_abr._exist(node.data):
                nouvel_arb.insert(node.data)
            self._intersection(nouvel_arb, node.filsGauche, autre_abr)
            self._intersection(nouvel_arb, node.filsDroit, autre_abr)

    # Affiche la grandeur de l'arbre
    def height(self):
        return self._height(self.racine)

    def _height(self, node):
        if node is None:
            return 0
        else:
            left_height = self._height(node.filsGauche)
            right_height = self._height(node.filsDroit)
            return max(left_height, right_height) + 1

    # Supprime toutes les valeurs de l'arbre
    def clear(self):
        self.racine = None
