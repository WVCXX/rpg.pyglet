import random
class RomanceSystem:
    """Система романтических отношений"""
    def __init__(self):
        self.relationships = {}  # id персонажа -> объект отношений
        self.married_to = None
        self.lovers = []
        self.children = []
    
    def add_relationship(self, npc_id, npc_name):
        """Добавление новых отношений"""
        self.relationships[npc_id] = {
            "name": npc_name,
            "affection": 0,  # 0-100
            "jealousy": 0,   # 0-100
            "trust": 50,      # 0-100
            "passion": 0,    
            "status": "acquainted",  
            "gifts_given": [],
            "dates": 0,
            "secrets_shared": [],
            "last_interaction": None
        }
    
    def interact(self, npc_id, action):
        """Взаимодействие с персонажем"""
        if npc_id not in self.relationships:
            return "Ты не знаком с этим человеком"
        
        rel = self.relationships[npc_id]
        
        effects = {
            "compliment": {"affection": +5, "passion": +2},
            "gift": {"affection": +10, "jealousy": -5 if len(self.lovers) <= 1 else +10},
            "flirt": {"affection": +3, "passion": +5, "trust": -2},
            "confess": {"trust": +15, "affection": +10, "passion": +20},
            "jealous": {"jealousy": +20, "trust": -10},
            "ignore": {"affection": -5, "trust": -3},
            "insult": {"affection": -20, "trust": -15, "status": "enemies"},
            "defend": {"affection": +15, "trust": +10}
        }
        
        if action in effects:
            for stat, change in effects[action].items():
                if stat in rel:
                    rel[stat] = max(0, min(100, rel[stat] + change))
        
        # Проверка смены статуса
        self.check_status_change(npc_id)
        
        return self.get_reaction(npc_id, action)
    
    def check_status_change(self, npc_id):
        """Проверка смены статуса отношений"""
        rel = self.relationships[npc_id]
        
        if rel["affection"] >= 80 and rel["trust"] >= 70 and rel["passion"] >= 60:
            if rel["status"] == "lovers" and self.married_to is None:
                if random.random() < 0.3:  # 30% шанс предложения
                    rel["status"] = "engaged"
        
        elif rel["affection"] >= 60 and rel["passion"] >= 50:
            if rel["status"] == "friends":
                rel["status"] = "lovers"
                self.lovers.append(npc_id)
        
        elif rel["affection"] >= 40:
            if rel["status"] == "acquainted":
                rel["status"] = "friends"
        
        elif rel["affection"] <= -30:
            rel["status"] = "enemies"
            if npc_id in self.lovers:
                self.lovers.remove(npc_id)
    
    def get_reaction(self, npc_id, action):
        """Получение реакции персонажа"""
        rel = self.relationships[npc_id]
        
        reactions = {
            "compliment": {
                80: f"{rel['name']} краснеет: 'Ты такой милый...'",
                50: f"{rel['name']}: 'Спасибо, приятно слышать'",
                20: f"{rel['name']}: 'Эм... спасибо'",
                0: f"{rel['name']} игнорирует комплимент"
            },
            "flirt": {
                70: f"{rel['name']} игриво улыбается: 'Продолжай...'",
                40: f"{rel['name']} смущенно отводит взгляд",
                20: f"{rel['name']} не понимает, что ты flirt'ишь",
                0: f"{rel['name']} хмурится: 'Не надо так'"
            },
            "confess": {
                80: f"{rel['name']} обнимает тебя: 'Я тоже тебя люблю!'",
                50: f"{rel['name']} в шоке: 'Мне нужно подумать...'",
                20: f"{rel['name']} отворачивается: 'Прости, я не могу'",
                0: f"{rel['name']} в ужасе убегает!"
            }
        }
        
        if action in reactions:
            for threshold in sorted(reactions[action].keys(), reverse=True):
                if rel["affection"] >= threshold:
                    return reactions[action][threshold]
        
        return f"{rel['name']} смотрит на тебя..."
    
    def propose_marriage(self, npc_id):
        """Предложение брака"""
        if npc_id not in self.relationships:
            return "Ты даже не знаком с этим человеком!"
        
        rel = self.relationships[npc_id]
        
        if rel["status"] != "lovers":
            return f"{rel['name']} удивлен: 'Мы даже не встречались!'"
        
        if self.married_to:
            return f"Ты уже женат на {self.relationships[self.married_to]['name']}!"
        
        # Шанс успеха зависит от отношений
        chance = (rel["affection"] + rel["trust"] + rel["passion"]) / 3
        
        if random.random() * 100 < chance:
            self.married_to = npc_id
            rel["status"] = "married"
            return f"{rel['name']} плачет от счастья: 'ДА! Я согласна!'"
        else:
            rel["affection"] -= 20
            return f"{rel['name']} грустно качает головой: 'Я не готова...'"
    
    def have_child(self):
        """Рождение ребенка"""
        if not self.married_to:
            return "У тебя нет семьи"
        
        child = {
            "name": self.generate_child_name(),
            "age": 0,
            "gender": random.choice(["сын", "дочь"]),
            "traits": random.sample(["умный", "сильный", "красивый", "хитрый"], 2)
        }
        
        self.children.append(child)
        return f"У тебя родился {child['gender']}! Назвали {child['name']}"
    
    def generate_child_name(self):
        """Генерация имени ребенка"""
        names_male = ["Иван", "Петр", "Алексей", "Дмитрий", "Николай"]
        names_female = ["Анна", "Мария", "Елена", "Ольга", "Наталья"]
        
        if random.choice([True, False]):
            return random.choice(names_male)
        else:
            return random.choice(names_female)
    
    def jealousy_check(self, npc_id):
        """Проверка ревности"""
        if len(self.lovers) > 1:
            for lover_id in self.lovers:
                if lover_id != npc_id:
                    rel = self.relationships[lover_id]
                    rel["jealousy"] += 20
                    rel["trust"] -= 10
                    
                    if rel["jealousy"] >= 80:
                        return f"{rel['name']} устраивает скандал из-за ревности!"
        return None