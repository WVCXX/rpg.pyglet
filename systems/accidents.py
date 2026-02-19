import random

class AccidentSystem:
    """Система несчастных случаев"""
    def __init__(self):
        self.accidents = {
            "fall": {
                "name": "Падение",
                "chance": 5,
                "damage": (10, 30),
                "injuries": ["broken_leg", "sprained_ankle", "bruises"],
                "texts": [
                    "Ты поскользнулся на гнилых досках и упал!",
                    "Ты споткнулся о камень и полетел кубарем!",
                    "Лестница под тобой сломалась!",
                    "Ты упал в открытый люк!"
                ]
            },
            "animal_attack": {
                "name": "Нападение животного",
                "chance": 3,
                "damage": (15, 40),
                "injuries": ["bite", "scratches", "rabies"],
                "texts": [
                    "Бешеная собака укусила тебя!",
                    "На тебя напал дикий кабан!",
                    "Змея ужалила тебя в ногу!",
                    "Стая крыс атаковала тебя!"
                ]
            },
            "fire": {
                "name": "Пожар",
                "chance": 2,
                "damage": (20, 50),
                "injuries": ["burns", "scarring", "smoke_inhalation"],
                "texts": [
                    "В таверне начался пожар! Ты обжегся!",
                    "Свеча упала и подожгла твою одежду!",
                    "Кузнечный горн взорвался искрами!",
                    "Молния подожгла дерево рядом с тобой!"
                ]
            },
            "theft": {
                "name": "Кража",
                "chance": 8,
                "damage": (0, 0),
                "money_loss": (5, 50),
                "texts": [
                    "Карманник украл твой кошелек!",
                    "Ты оставил сумку без присмотра...",
                    "Нищие обчистили твои карманы!",
                    "Воры вскрыли твою комнату!"
                ]
            },
            "explosion": {
                "name": "Взрыв",
                "chance": 1,
                "damage": (30, 80),
                "injuries": ["burns", "concussion", "deafness"],
                "texts": [
                    "У алхимика взорвалась лаборатория!",
                    "Пороховая бочка рванула!",
                    "Магический эксперимент пошел не так!",
                    "Гроза ударила в башню с порохом!"
                ]
            },
            "poisoning": {
                "name": "Отравление",
                "chance": 4,
                "damage": (10, 25),
                "injuries": ["poisoned", "vomiting", "weakness"],
                "texts": [
                    "Еда в таверне была несвежей!",
                    "Ты выпил отравленное вино!",
                    "Грибы в лесу оказались ядовитыми!",
                    "Кто-то подсыпал яд в твой напиток!"
                ]
            },
            "building_collapse": {
                "name": "Обрушение",
                "chance": 1,
                "damage": (40, 100),
                "injuries": ["broken_bones", "crushed", "concussion"],
                "texts": [
                    "Старое здание рухнуло прямо на тебя!",
                    "Потолок в шахте обвалился!",
                    "Мост под тобой проломился!",
                    "Башня не выдержала и упала!"
                ]
            },
            "accidental_injury": {
                "name": "Случайная травма",
                "chance": 6,
                "damage": (5, 20),
                "injuries": ["cut", "bruise", "sprain"],
                "texts": [
                    "Ты порезался ржавым гвоздем!",
                    "Ты прищемил палец дверью!",
                    "Ты потянул спину, поднимая тяжелое!",
                    "Молоток соскользнул и ударил по пальцу!"
                ]
            },
            "magic_accident": {
                "name": "Магическая авария",
                "chance": 2,
                "damage": (20, 60),
                "injuries": ["magic_burn", "transformation", "curse"],
                "texts": [
                    "Твое заклинание вышло из-под контроля!",
                    "Магический артефакт взбесился!",
                    "Портал захлопнулся, отрезав часть тела!",
                    "Ты превратился в жабу на час!"
                ]
            }
        }
        
        self.injuries = {
            "broken_leg": {"name": "Сломанная нога", "effect": {"dexterity": -10}, "heal_time": (20, 40)},
            "broken_arm": {"name": "Сломанная рука", "effect": {"strength": -8}, "heal_time": (15, 30)},
            "concussion": {"name": "Сотрясение", "effect": {"intelligence": -5, "wisdom": -5}, "heal_time": (7, 14)},
            "burns": {"name": "Ожоги", "effect": {"health": -10}, "heal_time": (10, 20)},
            "bite": {"name": "Укус", "effect": {"stamina": -5}, "heal_time": (5, 10)},
            "poisoned": {"name": "Отравление", "effect": {"health": -5, "stamina": -5}, "heal_time": (3, 7)},
            "scarring": {"name": "Шрамы", "effect": {"charisma": -5}, "heal_time": (30, 60)},
            "rabies": {"name": "Бешенство", "effect": {"strength": -5, "intelligence": -10}, "heal_time": (40, 80), "deadly": True}
        }
    
    def check_accident(self, location="generic"):
        """Проверка несчастного случая"""
        # Базовая вероятность
        chance = random.randint(1, 100)
        
        # Модификаторы локации
        location_mods = {
            "tavern": {"poisoning": 2, "fall": 0.5, "fire": 1.5},
            "slums": {"theft": 3, "animal_attack": 2, "fall": 2},
            "forest": {"animal_attack": 4, "fall": 2, "poisoning": 2},
            "castle": {"fall": 1, "accidental_injury": 0.5},
            "dungeon": {"building_collapse": 3, "fall": 3, "magic_accident": 2},
            "port": {"fall": 3, "theft": 2, "poisoning": 1.5}
        }
        
        for accident_id, accident in self.accidents.items():
            mod = 1.0
            if location in location_mods and accident_id in location_mods[location]:
                mod = location_mods[location][accident_id]
            
            if chance <= accident["chance"] * mod:
                return self.trigger_accident(accident_id)
        
        return None
    
    def trigger_accident(self, accident_id):
        """Запуск несчастного случая"""
        accident = self.accidents[accident_id]
        
        result = {
            "type": accident_id,
            "name": accident["name"],
            "text": random.choice(accident["texts"]),
            "damage": 0,
            "money_loss": 0,
            "injuries": []
        }
        
        # Урон
        if "damage" in accident:
            result["damage"] = random.randint(*accident["damage"])
        
        # Потеря денег
        if "money_loss" in accident:
            result["money_loss"] = random.randint(*accident["money_loss"])
        
        # Травмы
        if "injuries" in accident:
            if random.random() < 0.3:  # 30% шанс получить травму
                injury_id = random.choice(accident["injuries"])
                result["injuries"].append(injury_id)
        
        return result
    
    def apply_accident(self, accident_result, player):
        """Применение последствий несчастного случая"""
        messages = [accident_result["text"]]
        
        # Урон
        if accident_result["damage"] > 0:
            player.health -= accident_result["damage"]
            messages.append(f"Ты получил {accident_result['damage']} урона!")
        
        # Потеря денег
        if accident_result["money_loss"] > 0:
            loss = min(accident_result["money_loss"], player.money)
            player.money -= loss
            messages.append(f"Ты потерял {loss} монет!")
        
        # Травмы
        for injury_id in accident_result["injuries"]:
            if injury_id in self.injuries:
                injury = self.injuries[injury_id]
                player.injuries.append({
                    "id": injury_id,
                    "name": injury["name"],
                    "days": 0,
                    "duration": random.randint(*injury["heal_time"]),
                    "effects": injury["effect"]
                })
                
                # эффекты травмы
                for stat, effect in injury["effect"].items():
                    if stat in player.stats:
                        player.stats[stat] += effect
                
                messages.append(f"Травма: {injury['name']}!")
        
        return "\n".join(messages)
    
    def daily_healing(self, player):
        """Ежедневное лечение травм"""
        healed = []
        
        for injury in player.injuries[:]:
            injury["days"] += 1
            
            if injury["days"] >= injury["duration"]:

                for stat, effect in injury["effects"].items():
                    if stat in player.stats:
                        player.stats[stat] -= effect
                
                player.injuries.remove(injury)
                healed.append(injury["name"])
        
        if healed:
            return f"Твои травмы зажили: {', '.join(healed)}"
        return None