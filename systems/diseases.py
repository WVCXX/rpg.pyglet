import random

class DiseaseSystem:
    """Система болезней"""
    def __init__(self):
        self.diseases = {
            "common_cold": {
                "name": "Простуда",
                "symptoms": ["кашель", "насморк", "температура"],
                "duration": (3, 7),
                "effects": {
                    "health": -5,
                    "stamina": -10,
                    "strength": -2
                },
                "contagious": True,
                "treatment": ["rest", "herbs", "potion"]
            },
            "wound_infection": {
                "name": "Заражение раны",
                "symptoms": ["лихорадка", "гной", "слабость"],
                "duration": (5, 14),
                "effects": {
                    "health": -15,
                    "stamina": -20,
                    "strength": -5
                },
                "contagious": False,
                "treatment": ["surgery", "strong_herbs", "magic"]
            },
            "plague": {
                "name": "Чума",
                "symptoms": ["бубоны", "кровотечение", "бред"],
                "duration": (7, 21),
                "effects": {
                    "health": -30,
                    "stamina": -40,
                    "strength": -10,
                    "luck": -20
                },
                "contagious": True,
                "treatment": ["quarantine", "rare_herbs", "powerful_magic"],
                "deadly": True
            },
            "blood_cough": {
                "name": "Кровавый кашель",
                "symptoms": ["кашель с кровью", "боль в груди", "бледность"],
                "duration": (10, 30),
                "effects": {
                    "health": -20,
                    "stamina": -30,
                    "strength": -8
                },
                "contagious": True,
                "treatment": ["bed_rest", "special_medicine", "holy_water"]
            },
            "madness": {
                "name": "Безумие",
                "symptoms": ["галлюцинации", "паранойя", "агрессия"],
                "duration": (30, 100),
                "effects": {
                    "intelligence": -15,
                    "wisdom": -20,
                    "charisma": -25
                },
                "contagious": False,
                "treatment": ["exorcism", "rare_herbs", "mind_magic"]
            }
        }
        
        self.active_diseases = []
        self.herbs = {
            "common_herb": {"cures": ["common_cold"], "effect": 30},
            "healing_herb": {"cures": ["wound_infection"], "effect": 50},
            "rare_herb": {"cures": ["plague", "blood_cough"], "effect": 70},
            "magic_herb": {"cures": ["madness"], "effect": 90}
        }
    
    def infect(self, disease_id, player):
        """Заражение болезнью"""
        if disease_id not in self.diseases:
            return False
        
        disease = self.diseases[disease_id].copy()
        
        # Длительность
        duration = random.randint(*disease["duration"])
        
        infection = {
            "id": disease_id,
            "name": disease["name"],
            "symptoms": disease["symptoms"],
            "days_infected": 0,
            "duration": duration,
            "effects": disease["effects"],
            "contagious": disease["contagious"],
            "treatment": disease["treatment"],
            "deadly": disease.get("deadly", False)
        }
        
        self.active_diseases.append(infection)
        self.apply_effects(infection, player, add=True)
        
        return True
    
    def apply_effects(self, infection, player, add=True):
        """Применение эффектов болезни"""
        multiplier = 1 if add else -1
        
        for effect, value in infection["effects"].items():
            if effect in player.stats:
                player.stats[effect] += value * multiplier
            elif effect == "health":
                player.max_health += value * multiplier
                if player.health > player.max_health:
                    player.health = player.max_health
            elif effect == "stamina":
                player.max_stamina += value * multiplier
    
    def daily_update(self, player):
        """Ежедневное обновление болезней"""
        for infection in self.active_diseases[:]:
            infection["days_infected"] += 1
            
            # Проверка на смерть
            if infection.get("deadly", False):
                death_chance = 0.05 + (infection["days_infected"] / infection["duration"]) * 0.1
                if random.random() < death_chance:
                    player.health = 0
                    return f"Ты умер от {infection['name']}!"
            
            # Ухудшение состояния
            if infection["days_infected"] > infection["duration"]:
                self.cure(infection["id"], player, complete=False)
            else:
                # Случайное ухудшение
                if random.random() < 0.1:
                    player.health -= 5
                    return f"Твое состояние ухудшается из-за {infection['name']}"
        
        # Распространение болезни 
        if any(d["contagious"] for d in self.active_diseases):
            if random.random() < 0.3:
                return "Ты чихаешь. Кажется, ты можешь заразить других..."
        
        return None
    
    def cure(self, disease_id, player, complete=True):
        """Лечение болезни"""
        for i, infection in enumerate(self.active_diseases):
            if infection["id"] == disease_id:

                self.apply_effects(infection, player, add=False)
                
                if complete:
                    self.active_diseases.pop(i)
                    return f"Ты вылечился от {infection['name']}!"
                else:
                    # Болезнь прошла сама
                    self.active_diseases.pop(i)
                    return f"{infection['name']} прошла сама собой"
        
        return None
    
    def treat_with_herb(self, herb_id, player):
        """Лечение травой"""
        if herb_id not in self.herbs:
            return "У тебя нет такой травы"
        
        herb = self.herbs[herb_id]
        cured_any = False
        
        for infection in self.active_diseases[:]:
            if infection["id"] in herb["cures"]:
                if random.random() * 100 < herb["effect"]:
                    self.cure(infection["id"], player)
                    cured_any = True
                else:
                    return f"{herb_id} не помог от {infection['name']}"
        
        if cured_any:
            return f"{herb_id} помог вылечить болезнь!"
        
        return "Эта трава не помогает от твоих болезней"
    
    def get_symptoms(self):
        """Получение симптомов"""
        if not self.active_diseases:
            return "Ты здоров"
        
        symptoms = []
        for d in self.active_diseases:
            symptoms.extend(d["symptoms"])
        
        return f"Симптомы: {', '.join(set(symptoms))}"