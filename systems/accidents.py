import random
from typing import Dict, List, Optional, Tuple

class AccidentSystem:
    """Система несчастных случаев"""
    def __init__(self):
        self.accidents = {
            "падение": {
                "name": "Падение",
                "chance": 5,
                "damage": (10, 30),
                "injuries": ["перелом_ноги", "растяжение", "ушибы"],
                "texts": [
                    "Ты поскользнулся на гнилых досках и упал!",
                    "Ты споткнулся о камень и полетел кубарем!",
                    "Лестница под тобой сломалась!",
                    "Ты упал в открытый люк!",
                    "Крыша обвалилась под тобой!"
                ]
            },
            "нападение_животного": {
                "name": "Нападение животного",
                "chance": 3,
                "damage": (15, 40),
                "injuries": ["укус", "царапины", "бешенство"],
                "texts": [
                    "Бешеная собака укусила тебя!",
                    "На тебя напал дикий кабан!",
                    "Змея ужалила тебя в ногу!",
                    "Стая крыс атаковала тебя!",
                    "Медведь вышел из берлоги!"
                ]
            },
            "пожар": {
                "name": "Пожар",
                "chance": 2,
                "damage": (20, 50),
                "injuries": ["ожоги", "шрамы", "отравление_дымом"],
                "texts": [
                    "В таверне начался пожар! Ты обжегся!",
                    "Свеча упала и подожгла твою одежду!",
                    "Кузнечный горн взорвался искрами!",
                    "Молния подожгла дерево рядом с тобой!",
                    "Магический эксперимент вызвал возгорание!"
                ]
            },
            "кража": {
                "name": "Кража",
                "chance": 8,
                "damage": (0, 0),
                "money_loss": (5, 50),
                "item_loss": True,
                "texts": [
                    "Карманник украл твой кошелек!",
                    "Ты оставил сумку без присмотра...",
                    "Нищие обчистили твои карманы!",
                    "Воры вскрыли твою комнату!",
                    "Цыгане окружили и обворовали тебя!"
                ]
            },
            "взрыв": {
                "name": "Взрыв",
                "chance": 1,
                "damage": (30, 80),
                "injuries": ["ожоги", "контузия", "глухота"],
                "texts": [
                    "У алхимика взорвалась лаборатория!",
                    "Пороховая бочка рванула!",
                    "Магический эксперимент пошел не так!",
                    "Гроза ударила в башню с порохом!",
                    "Рудник обрушился от взрыва!"
                ]
            },
            "отравление": {
                "name": "Отравление",
                "chance": 4,
                "damage": (10, 25),
                "injuries": ["отравление", "рвота", "слабость"],
                "disease": "отравление",
                "texts": [
                    "Еда в таверне была несвежей!",
                    "Ты выпил отравленное вино!",
                    "Грибы в лесу оказались ядовитыми!",
                    "Кто-то подсыпал яд в твой напиток!",
                    "Вода из колодца оказалась грязной!"
                ]
            },
            "обрушение": {
                "name": "Обрушение",
                "chance": 1,
                "damage": (40, 100),
                "injuries": ["переломы", "травма_головы", "контузия"],
                "texts": [
                    "Старое здание рухнуло прямо на тебя!",
                    "Потолок в шахте обвалился!",
                    "Мост под тобой проломился!",
                    "Башня не выдержала и упала!",
                    "Стена древней гробницы обрушилась!"
                ]
            },
            "случайная_травма": {
                "name": "Случайная травма",
                "chance": 6,
                "damage": (5, 20),
                "injuries": ["порез", "синяк", "растяжение"],
                "texts": [
                    "Ты порезался ржавым гвоздем!",
                    "Ты прищемил палец дверью!",
                    "Ты потянул спину, поднимая тяжелое!",
                    "Молоток соскользнул и ударил по пальцу!",
                    "Ты споткнулся о собственный меч!"
                ]
            },
            "магическая_авария": {
                "name": "Магическая авария",
                "chance": 2,
                "damage": (20, 60),
                "injuries": ["магический_ожог", "трансформация", "проклятие"],
                "texts": [
                    "Твое заклинание вышло из-под контроля!",
                    "Магический артефакт взбесился!",
                    "Портал захлопнулся, отрезав часть тела!",
                    "Ты превратился в жабу на час!",
                    "Древнее заклинание сработало не так как надо!"
                ]
            },
            "нападение_разбойников": {
                "name": "Нападение разбойников",
                "chance": 3,
                "damage": (20, 45),
                "injuries": ["раны", "сотрясение", "перелом"],
                "money_loss": (20, 100),
                "texts": [
                    "На тебя напали разбойники!",
                    "Грабители поджидали в засаде!",
                    "Бандиты окружили тебя!",
                    "Разбойники с большой дороги!",
                    "Ночная стража оказалась бандитами!"
                ]
            }
        }
        
        self.injuries = {
            "перелом_ноги": {
                "name": "Перелом ноги",
                "effect": {"ловкость": -10, "скорость": -20},
                "heal_time": (20, 40),
                "treatment": ["лекарь", "магия", "покой"]
            },
            "перелом_руки": {
                "name": "Перелом руки",
                "effect": {"сила": -8, "ловкость": -5},
                "heal_time": (15, 30),
                "treatment": ["лекарь", "магия"]
            },
            "сотрясение": {
                "name": "Сотрясение мозга",
                "effect": {"интеллект": -10, "мудрость": -10},
                "heal_time": (7, 14),
                "treatment": ["покой", "зелья"]
            },
            "ожоги": {
                "name": "Ожоги",
                "effect": {"здоровье": -10, "харизма": -5},
                "heal_time": (10, 20),
                "treatment": ["мазь", "лекарь"]
            },
            "укус": {
                "name": "Укус",
                "effect": {"выносливость": -5},
                "heal_time": (5, 10),
                "treatment": ["антидот", "перевязка"]
            },
            "отравление": {
                "name": "Отравление",
                "effect": {"здоровье": -5, "выносливость": -10},
                "heal_time": (3, 7),
                "treatment": ["антидот", "жрец"]
            },
            "шрамы": {
                "name": "Шрамы",
                "effect": {"харизма": -5},
                "heal_time": (30, 60),
                "treatment": ["магия", "хирургия"]
            },
            "бешенство": {
                "name": "Бешенство",
                "effect": {"сила": -5, "интеллект": -10, "харизма": -15},
                "heal_time": (40, 80),
                "deadly": True,
                "treatment": ["редкое_зелье", "храм"]
            },
            "рана": {
                "name": "Глубокая рана",
                "effect": {"здоровье": -15, "кровотечение": True},
                "heal_time": (10, 20),
                "treatment": ["перевязка", "хирургия"]
            },
            "травма_головы": {
                "name": "Травма головы",
                "effect": {"интеллект": -15, "мудрость": -15},
                "heal_time": (15, 30),
                "treatment": ["храм", "магия"]
            },
            "магический_ожог": {
                "name": "Магический ожог",
                "effect": {"мана": -20, "интеллект": -5},
                "heal_time": (10, 25),
                "treatment": ["магия", "редкие_травы"]
            },
            "проклятие": {
                "name": "Проклятие",
                "effect": {"удача": -20},
                "heal_time": (50, 100),
                "treatment": ["экзорцизм", "жрец"]
            }
        }
    
    def check_accident(self, location: str = "городская_площадь", 
                      player_luck: int = 8) -> Optional[Dict]:
        """Проверка несчастного случая"""
        # базовая вероятность
        base_chance = random.randint(1, 100)
        
        # модификаторы локации
        location_mods = {
            "таверна": {"отравление": 2, "падение": 0.5, "пожар": 1.5, "кража": 1.5},
            "трущобы": {"кража": 3, "нападение_разбойников": 2, "падение": 2, "отравление": 2},
            "лес": {"нападение_животного": 4, "падение": 2, "отравление": 2},
            "замок": {"падение": 1, "случайная_травма": 0.5, "нападение_разбойников": 0.5},
            "подземелье": {"обрушение": 3, "падение": 3, "магическая_авария": 2, "нападение_животного": 2},
            "порт": {"падение": 3, "кража": 2, "отравление": 1.5},
            "храм": {"магическая_авария": 0.5, "проклятие": 0.5}, 
            "рынок": {"кража": 2.5, "нападение_разбойников": 1, "отравление": 1.5}
        }
        
        # модификатор удачи
        luck_mod = max(0.5, 1.0 - (player_luck * 0.03))
        
        for accident_id, accident in self.accidents.items():
            mod = 1.0 * luck_mod
            
            if location in location_mods and accident_id in location_mods[location]:
                mod *= location_mods[location][accident_id]
            
            # время суток
            hour = self.get_hour() if hasattr(self, 'get_hour') else 12
            if accident_id == "кража" and (hour < 6 or hour > 20):
                mod *= 2  # ночью воров больше
            
            if base_chance <= accident["chance"] * mod:
                return self.trigger_accident(accident_id)
        
        return None
    
    def get_hour(self) -> int:
        """Получение текущего часа (заглушка)"""
        return 12
    
    def trigger_accident(self, accident_id: str) -> Dict:
        """Запуск несчастного случая"""
        accident = self.accidents[accident_id]
        
        result = {
            "type": accident_id,
            "name": accident["name"],
            "text": random.choice(accident["texts"]),
            "damage": 0,
            "money_loss": 0,
            "injuries": [],
            "items_lost": []
        }
        
        # урон
        if "damage" in accident:
            result["damage"] = random.randint(*accident["damage"])
        
        # потеря денег
        if "money_loss" in accident:
            result["money_loss"] = random.randint(*accident["money_loss"])
        
        # потеря предметов
        if accident.get("item_loss", False):
            result["items_lost"] = self.generate_item_loss()
        
        # травмы
        if "injuries" in accident:
            if random.random() < 0.3:  # 30% шанс получить травму
                injury_id = random.choice(accident["injuries"])
                result["injuries"].append(injury_id)
        
        return result
    
    def generate_item_loss(self) -> List[str]:
        """Генерация потери предметов"""
        items = ["зелье_здоровья", "зелье_маны", "факел", "веревка", "еда"]
        lost_count = random.randint(1, 3)
        return random.sample(items, min(lost_count, len(items)))
    
    def apply_accident(self, accident_result: Dict, player) -> str:
        """Применение последствий несчастного случая"""
        messages = [accident_result["text"]]
        
        # урон
        if accident_result["damage"] > 0:
            player.health -= accident_result["damage"]
            messages.append(f"💔 Ты получил {accident_result['damage']} урона!")
        
        # потеря денег
        if accident_result["money_loss"] > 0:
            loss = min(accident_result["money_loss"], player.money)
            player.money -= loss
            messages.append(f"💰 Ты потерял {loss} монет!")
        
        # потеря предметов
        for item in accident_result["items_lost"]:
            for category in ["potions", "misc", "ingredients"]:
                if player.inventory.remove_item(category, item, 1):
                    messages.append(f"📦 Ты потерял: {item}")
                    break
        
        # травмы
        for injury_id in accident_result["injuries"]:
            if injury_id in self.injuries:
                injury = self.injuries[injury_id]
                
                # проверка нет ли уже такой травмы
                has_injury = False
                for existing in player.injuries:
                    if existing["id"] == injury_id:
                        has_injury = True
                        break
                
                if not has_injury:
                    new_injury = {
                        "id": injury_id,
                        "name": injury["name"],
                        "days": 0,
                        "duration": random.randint(*injury["heal_time"]),
                        "effects": injury["effect"],
                        "treatment": injury.get("treatment", [])
                    }
                    
                    player.injuries.append(new_injury)
                    
                    # применение эффекта
                    for stat, effect in injury["effect"].items():
                        if stat in player.stats:
                            player.stats[stat] += effect
                    
                    messages.append(f"🏥 Травма: {injury['name']}!")
        
        return "\n".join(messages)
    
    def daily_healing(self, player) -> Optional[str]:
        """Ежедневное лечение травм"""
        healed = []
        
        for injury in player.injuries[:]:
            injury["days"] += 1
            
            # шанс осложнений
            if injury.get("deadly", False) and random.random() < 0.1:
                player.health -= 10
                return f"⚠ Осложнение от {injury['name']}! Ты теряешь 10 здоровья."
            
            if injury["days"] >= injury["duration"]:

                for stat, effect in injury["effects"].items():
                    if stat in player.stats:
                        player.stats[stat] -= effect
                
                player.injuries.remove(injury)
                healed.append(injury["name"])
        
        if healed:
            return f"✨ Твои травмы зажили: {', '.join(healed)}"
        return None
    
    def get_injury_description(self, player) -> str:
        """Получение описания травм"""
        if not player.injuries:
            return "Ты здоров"
        
        desc = "Травмы:\n"
        for injury in player.injuries:
            days_left = injury["duration"] - injury["days"]
            desc += f"  • {injury['name']} (еще {days_left} дней)\n"
        return desc