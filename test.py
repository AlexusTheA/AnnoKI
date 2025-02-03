import numpy as np
from itertools import product

# Gegebene building_costs und resources
building_cost = np.array([[0, 0],    # None
                          [2, 0],    # House
                          [0, 3],    # Wood
                          [5, 3],    # Fish
                          [4, 2],    # Sheep
                          [3, 2]])   # Workshop

# Funktion, um Permutationen zu finden, die mit den Ressourcen übereinstimmen
def can_build(resources):
    # Filtere "None"-Elemente heraus (z.B. [0, 0])
    valid_elements = [i for i in range(len(building_cost)) if not np.array_equal(building_cost[i], [0, 0])]
    
    # Maximal 6 Elemente in der Permutation
    max_length = 6
    
    # Ergebnisarray, das gültige Permutationen speichern wird
    buildable = []
    
    # Alle Permutationen der gültigen Elemente (max. 6 lang)
    for length in range(1, max_length + 1):
        for perm in product(valid_elements, repeat=length):
            # Summiere die Kosten der aktuellen Permutation
            total_cost = np.sum([building_cost[i] for i in perm], axis=0)
            
            # Prüfe, ob die Permutation mit den Ressourcen kompatibel ist
            if total_cost[0] <= resources[1] and total_cost[1] <= resources[2]:
                buildable.append(perm)
    
    # Gib die Liste der Permutationen zurück (keine Umwandlung in ein numpy Array nötig)
    return buildable

# Beispiel-Ressourcen
resources = np.array([0, 1000, 1000])  # [Summe der Ressourcen, Holz, Fisch]

# Finde alle baubaren Permutationen
buildable_permutations = can_build(resources)
print("Baubare Permutationen:")
print(buildable_permutations)
