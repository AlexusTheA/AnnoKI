import numpy as np
import time
building_id = np.array([])



class Building:
    def __init__(self, id, wood_cost, tool_cost, interval, produces, production_amount, current_time):
        self.id = id
        self.wood_cost = wood_cost
        self.tool_cost = tool_cost
        self.interval = interval  # Alle wie viele Sekunden wird produziert
        self.produces = produces  # Welche Ressource wird produziert
        self.production_amount = production_amount  # Menge pro Produktion
        self.time_since_last_production = current_time  # Zählt die Sekunden mit

    def produce(self, resources: np.ndarray[np.int32], current_time):
        """Prüft, ob das Gebäude produzieren darf, und fügt Ressourcen hinzu."""
        if current_time - self.time_since_last_production >= self.interval:
            resources[self.produces] += self.production_amount
            self.time_since_last_production = current_time  # Produktion zurücksetzen
        
    """
   def can_remove(self, current_time):
        ""Ein Gebäude kann nur entfernt werden, wenn es mindestens einmal produziert hat.""
        return (current_time - self.time_since_last_production) % self.interval == 0
    
    def remove(self, resources, buildings):
        ""Entfernt das Gebäude, wenn es produzieren konnte.""

        resources[0b1] += building_cost[id][0]
        resources[0b10] += building_cost[id][1]
        buildings[self.produces].pop(self.id)
        del self"""





# Spezialisierte Gebäudetypen (Unterklassen)
class House(Building):
    def __init__(self, id, current_time, pop):
        super().__init__(id = id, wood_cost=2, tool_cost=0, interval=15, produces=0b1, production_amount=1, current_time = current_time)
        self.limit = 8
        self.pop = pop

    def produce(self, resources, current_time):
        if self.pop < self.limit:
            if current_time - self.time_since_last_production >= self.interval:
                resources[self.produces] += self.production_amount
                self.time_since_last_production = current_time  # Produktion zurücksetzen
                self.pop +=1

    def __str__(self):
        return "House"

class Woodcutter(Building):
    def __init__(self, id, current_time):
        super().__init__(id, wood_cost=0, tool_cost=3, interval=40, produces=0b10, production_amount=2, current_time = current_time)

    def __str__(self):
        return "Woodcutter"
    
class Fisher(Building):
    def __init__(self, id, current_time):
        super().__init__(id, wood_cost=5, tool_cost=3, interval=90, produces=0b100, production_amount=1, current_time = current_time)

    def produce(self, resources, current_time):
        if current_time - self.time_since_last_production >= self.interval:
            a = self.production_amount
            self.production_amount *= -1
            resources[self.produces] += 1 if a > 0 else 2
            self.time_since_last_production = current_time  # Produktion zurücksetzen
    
    def __str__(self):
        return "Fisher"

class Sheep(Building):
    def __init__(self, id, current_time):
        super().__init__(id, wood_cost=4, tool_cost=2, interval=30, produces=0b101, production_amount=1, current_time = current_time)

    def __str__(self):
        return "Sheep"

class Workshop(Building):
    def __init__(self, id, current_time):
        super().__init__(id, wood_cost=3, tool_cost=2, interval=30, produces=0b110, production_amount=1, current_time = current_time)
        self.need = 2
        self.starttime = 30

    def produce(self, resources, current_time):
        if resources[0b101] >= self.need:
            self.starttime -= 1
            if self.starttime < 0:
                super().produce(resources, current_time)
                resources[0b101] -= 2
                self.starttime = 30
        
    def __str__(self):
        return "Workshop"







create = np.array([
    lambda id: House(id, 1),
    lambda id: Woodcutter(id),
    lambda id: Fisher(id),
    lambda id: Sheep(id),
    lambda id: Workshop(id)
])

class GameSimulation():

    """
    def can_build(resources):
        buildable = np.array([])
        # Houses
        i = 0
        for _ in building_cost:
            a = resources[0b1] // building_cost[i][0]
            b = resources[0b10] // building_cost[i][1]
            i += 1
            buildable.append(a if a <= b else b)"""
    def __init__(self):
        # Ressourcen am Start
        # einwohner, holz, werkzeug, fisch, wolle, kleidung
        self.resources = np.array([0, 24, 1000, 1000, 4, 0, 0])

        # Gebäude in einem Dictionary speichern
        self.buildings = [
            [],
            [House(0, 0, 8), House(1, 0, 8), House(2, 0, 8)],  # 3 Häuser
            [Woodcutter(0, 0)],  # 1 Holzfäller
            [],
            [Fisher(0, 0)],  # 1 Fischer
            [],
            [],
        ]
        
        # Zeit-Tracking
        self.time_elapsed = -1 

    def can_build(self, building):
        return (building.wood_cost <= self.resources[2]) and (building.tool_cost <= self.resources[3])

    
    def build(self, building):
        if self.can_build(building):
            if isinstance(building, House):
                self.buildings[1].append(building)
                self.resources[2] -= building.wood_cost
                self.resources[3] -= building.tool_cost
            elif isinstance(building, Woodcutter):
                self.buildings[2].append(building)
                self.resources[2] -= building.wood_cost
                self.resources[3] -= building.tool_cost
            elif isinstance(building, Fisher):
                self.buildings[4].append(building)
                self.resources[2] -= building.wood_cost
                self.resources[3] -= building.tool_cost
            elif isinstance(building, Sheep):
                self.buildings[5].append(building)
                self.resources[2] -= building.wood_cost
                self.resources[3] -= building.tool_cost
            elif isinstance(building, Workshop):
                self.buildings[6].append(building)
                self.resources[2] -= building.wood_cost
                self.resources[3] -= building.tool_cost

    # checkt ressourcen, baut das gebäude, aktualisiert ressourcen
    def run(self, actions, state):
        match actions:
            case 1:
                self.build(House(len(self.buildings[0]), state, 1))
            case 2:
                self.build(Woodcutter(len(self.buildings[1]), state))
            case 4:
                self.build(Fisher(len(self.buildings[2]), state))
            case 5:
                self.build(Sheep(len(self.buildings[3]), state))
            case 6:
                self.build(Workshop(len(self.buildings[4]), state))
            case _:
                pass
        self.produce_all(state)
        
    def produce_all(self, state):
        for x in range(len(self.buildings)):
            for y in self.buildings[x]:
                y.produce(self.resources, state)

        

        
    def check_removable_buildings(self, current_time):
        """Überprüft, welche Gebäude entfernt werden können."""
        removable_buildings = {}

        for building_type, buildings in self.buildings.items():
            # Liste der Gebäude, die entfernt werden können
            removable_buildings[building_type] = [building for building in buildings if building.can_remove(current_time)]
        
        return removable_buildings


'''
start_time = time.time()
test = GameSimulation()
for i in range(300):
    test.run(1, i)
    print(test.resources)
    for i in range(len(test.buildings)):
        for j in range(len(test.buildings[i])):
            print(test.buildings[i][j])
end_time = time.time()
print(end_time - start_time)
'''


"""
a = []
Sim = GameSimulation()
state = 0
for _ in range(300):
    state +=1
    
    Sim.run(2, state)
    print(Sim.resources)
    print_a = []
    for i in Sim.buildings:
        print_a.append(len(i))
    print(print_a)
    print(state)
    a.append(str(Sim.buildings[2][0].time_since_last_production) + "\n")

with open("ausgabe.txt", "w") as datei:

    datei.write(str(a))
"""

if __name__ == "__main__":
    Sim = GameSimulation()
    Sim.resources = np.array([0, 0, 0, 0, 0, 0, 0])
    Sim.buildings = [
            [],
            [House(0, 0, 0)],  # 3 Häuser
            [Woodcutter(0, 0)],  # 1 Holzfäller
            [],
            [Fisher(0, 0)],  # 1 Fischer
            [Sheep(0, 0)],
            [Workshop(0, 0)],
        ]
    
    state = 0
    for i in range(300):
        state +=1
        print(f"{i} {Sim.resources}")
        Sim.run(0, i)
    print(Sim.resources)