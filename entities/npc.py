# entities/npc.py
import random

class NPC:
    def __init__(self, npc_id, name, race, gender, profession, personality):
        self.id = npc_id
        self.name = name
        self.race = race
        self.gender = gender
        self.profession = profession
        self.personality = personality
        self.relationship = 0
        self.location = "town_square"
        self.money = random.randint(10, 100)
        self.is_merchant = random.random() < 0.3
        self.inventory = self.generate_inventory()
        self.is_alive = True
        self.dialog = self.generate_dialog()
    
    def generate_inventory(self):
        if not self.is_merchant:
            return []
        items = []
        for _ in range(random.randint(1, 5)):
            items.append(random.choice([
                "health_potion", "bread", "water", "torch"
            ]))
        return items
    
    def generate_dialog(self):
        dialogs = {
            "трактирщик": "Заходи, путник! Пиво свежее!",
            "кузнец": "Нужен меч? Или подковать коня?",
            "стражник": "Проходи, не задерживайся.",
            "жрец": "Да хранит тебя Единый.",
            "торговец": "Лучшие товары только у меня!"
        }
        return dialogs.get(self.profession, "Здравствуй, путник.")