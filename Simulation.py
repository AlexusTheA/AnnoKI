from Buildings import *

class Simulation:
    def __init__(self):
        # Ressourcen am Start
        self.resources = {
            "wood": 15,
            "tools": 6,
            "fish": 4,
            "cloth": 0,
            "wool": 0,
            "population": 24,
        }
        
        # Gebäude in einem Dictionary speichern
        self.buildings = {
            "houses": [House() for _ in range(3)],  # 3 Häuser
            "fishers": [Fisher()],  # 1 Fischer
            "woodcutters": [Woodcutter()]  # 1 Holzfäller
        }
        
        # Zeit-Tracking
        self.time_elapsed = 0  

    def aktualisiere_produktion(self):
        """
        Lässt alle Gebäude produzieren und aktualisiert das Inventar.
        """
        pass

    def berechne_optionen(self):
        """
        Berechnet, welche Aktionen im aktuellen Spielzustand möglich sind.
        Rückgabe: Liste von möglichen Aktionen (z.B. ['sammle_holz', 'baue_haus'])
        """
        pass

    def ausfuehren_aktion(self, aktion):
        """
        Führt die von der KI gewählte Aktion aus und aktualisiert den Spielzustand.
        """
        pass

    def status(self):
        """
        Gibt den aktuellen Spielstatus aus (Inventar, Zeit, Gebäude).
        """
        pass

