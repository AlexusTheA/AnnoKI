import numpy as np

building_cost = np.array([[0, 0]    #None
                          [2, 0],   #House
                          [0, 3],   #Wood
                          [5, 3],   #Fish
                          [4, 2],   #Sheep
                          [3, 2]])  #Workshop

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

    def can_remove(self, current_time):
        """Ein Gebäude kann nur entfernt werden, wenn es mindestens einmal produziert hat."""
        return (current_time - self.time_since_last_production) % self.interval == 0
    
    def remove(self, resources, buildings):
        """Entfernt das Gebäude, wenn es produzieren konnte."""

        resources[0b1] += building_cost[id][0]
        resources[0b10] += building_cost[id][1]
        buildings[self.produces].pop(self.id)
        del self





# Spezialisierte Gebäudetypen (Unterklassen)
class House(Building):
    def __init__(self, id, current_time, pop):
        super().__init__(id = id, wood_cost=2, tool_cost=0, interval=15, produces=0b0, production_amount=1, current_time = current_time)
        self.limit = 8
        self.pop = pop

    def produce(self, resources, current_time):
        if self.pop < self.limit:
            super().produce(resources, current_time)

class Fisher(Building):
    def __init__(self, id, current_time):
        super().__init__(id, wood_cost=5, tool_cost=3, interval=90, produces=0b11, production_amount=1, current_time = current_time)

    def produce(self, resources, current_time):
        if current_time - self.time_since_last_production >= self.interval:
            a = self.production_amount
            self.production_amount *= -1
            resources[self.produces] += 1 if a > 0 else 2
            self.time_since_last_production = current_time  # Produktion zurücksetzen

class Woodcutter(Building):
    def __init__(self, id, current_time):
        super().__init__(id, wood_cost=0, tool_cost=3, interval=40, produces=0b1, production_amount=2, current_time = current_time)

class Sheep(Building):
    def __init__(self, id, current_time):
        super().__init__(id, wood_cost=4, tool_cost=2, interval=30, produces=0b100, production_amount=1, current_time = current_time)

class Workshop(Building):
    def __init__(self, id, current_time):
        super().__init__(id, wood_cost=3, tool_cost=2, interval=30, produces=0b101, production_amount=1, current_time = current_time)
        self.need = 2
        self.starttime = 30

    def produce(self, resources, current_time):
        if resources[0b100] >= self.need:
            self.starttime -= 1
            if self.starttime < 0:
                super().produce(resources, current_time)
                resources[0b100] -= 2
                self.starttime = 30







create = np.array([
    lambda id: House(id, 1),
    lambda id: Woodcutter(id),
    lambda id: Fisher(id),
    lambda id: Sheep(id),
    lambda id: Workshop(id)
])


def can_build(resources):
    buildable = np.array([])
    # Houses
    i = 0
    for _ in building_cost:
        a = resources[0b1] // building_cost[i][0]
        b = resources[0b10] // building_cost[i][1]
        i += 1
        buildable.append(a if a <= b else b)


def can_build(resources):
    buildable = np.array([])
    
    for _ in building_cost:
        if

def build(resources, buildings, id):
    resources[0b1] -= building_cost[id][0]
    resources[0b10] -= building_cost[id][1]
    buildings[id].append(create[id](len(buildings[id])))
    

    
def check_removable_buildings(self, current_time):
    """Überprüft, welche Gebäude entfernt werden können."""
    removable_buildings = {}

    for building_type, buildings in self.buildings.items():
        # Liste der Gebäude, die entfernt werden können
        removable_buildings[building_type] = [building for building in buildings if building.can_remove(current_time)]
    
    return removable_buildings








class Simulation:
    def __init__(self):
        # Ressourcen am Start
        self.resources = np.array(24, 15, 6, 4, 0, 0)
            

        
        # Gebäude in einem Dictionary speichern
        self.buildings = [
            [House(0, 8), House(1, 8), House(2, 8),],  # 3 Häuser
            [Woodcutter(0)],  # 1 Holzfäller
            [Fisher(0)],  # 1 Fischer
            [],
            [],
        ]
        
        # Zeit-Tracking
        self.time_elapsed = -1 


    def run(self):

        while(self.time_elapsed <= 300):
            
            #Produzieren
            for bulding_list in self.buildings:
                for building in bulding_list:
                    building.produce(self.resources, self.time_elapsed)

            #