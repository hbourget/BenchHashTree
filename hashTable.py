
class Table:
    def __init__(self, hash_table_size, hash_function=hash, hash_function_2=hash, rehash_type='linear'):
        self.hash_table_size = hash_table_size
        self.hash_function = hash_function
        self.hash_function_2 = hash_function_2
        self.rehash_type = rehash_type
        self.table = [None] * hash_table_size
        self.rehash_count = {}
        self.deleted_keys = set()

    # Inserer une valeur dans la table
    def insert(self, key, value):
        index = self.hash_function(key) % self.hash_table_size
        if self.table[index] is None or self.table[index][0] == key:
            self.table[index] = (key, value)
        else:
            i = 1
            while True:
                if self.rehash_type == 'linear':
                    new_index = (index + i) % self.hash_table_size
                elif self.rehash_type == 'quadratic':
                    new_index = (index + i*i) % self.hash_table_size

                if self.table[new_index] is None or self.table[new_index][0] == key:
                    self.table[new_index] = (key, value)
                    break
                else:
                    i += 1

            self.rehash_count[key] = self.rehash_count.get(key, 0) + 1

    # Supprimer une valeur de la table
    def delete(self, key):
        index = self.hash_function(key) % self.hash_table_size
        if self.table[index] is not None and self.table[index][0] == key:
            self.table[index] = None
            self.deleted_keys.add(key)
            self.rehash_count[key] = 0
        elif self.rehash_type == 'linear' or self.rehash_type == 'quadratic':
            i = 1
            while self.table[(index + i*i) % self.hash_table_size] is not None:
                if self.table[(index + i*i) % self.hash_table_size][0] == key:
                    self.table[(index + i*i) % self.hash_table_size] = None
                    self.deleted_keys.add(key)
                    self.rehash_count[key] = 0
                    return
                i += 1

    # Verifie si une valeur de la table
    def exist(self, key):
        if key in self.deleted_keys:
            return False
        index = self.hash_function(key) % self.hash_table_size
        if self.table[index] is not None and self.table[index][0] == key:
            return True
        elif self.rehash_type == 'linear' or self.rehash_type == 'quadratic':
            i = 1
            while self.table[(index + i*i) % self.hash_table_size] is not None:
                if self.table[(index + i*i) % self.hash_table_size][0] == key:
                    return True
                i += 1
            if key in self.rehash_count and self.rehash_count[key] > 0:
                return True
        return False

    # Retourne la valeur associee a une cle
    def value(self, key):
        index = self.hash_function(key) % self.hash_table_size
        if self.table[index] is not None and self.table[index][0] == key:
            return self.table[index][1]
        elif self.rehash_type == 'linear' or self.rehash_type == 'quadratic':
            i = 1
            while self.table[(index + i*i) % self.hash_table_size] is not None:
                if self.table[(index + i*i) % self.hash_table_size][0] == key:
                    return self.table[(index + i*i) % self.hash_table_size][1]
                i += 1
        raise KeyError("Cette clé n'existe pas dans la table de hachage.")

    def union(self, other):
        union_table = Table(self.hash_table_size, self.hash_function, self.hash_function_2)
        for i in range(self.hash_table_size):
            if self.table[i] is not None:
                union_table.insert(*self.table[i])
        for i in range(other.hash_table_size):
            if other.table[i] is not None and not union_table.exist(other.table[i][0]):
                union_table.insert(*other.table[i])
        return union_table

    def intersection(self, other):
        intersection_table = Table(self.hash_table_size, self.hash_function, self.hash_function_2)
        for i in range(self.hash_table_size):
            if self.table[i] is not None and other.exist(self.table[i][0]):
                intersection_table.insert(*self.table[i])
        return intersection_table

    # Afficher la table
    def affichage(self):
        for i in range(self.hash_table_size):
            if self.table[i] is not None:
                key, value = self.table[i]
                count = self.rehash_count.get(key, 0)
                print(f"Clé: {key} - Valeur: {value} - Nombre de rehachage(s): {count}")

# Hashage modulo
def hachage_modulo(c):
    return c % 10

# Hashage modulo 2
def hachage_modulo_2(key):
    return 1 + (key % 7)

