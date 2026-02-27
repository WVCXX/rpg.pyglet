# systems/romance_system.py
import random
from typing import Dict, List, Optional, Tuple

class RomanceSystem:
    """Система романтических отношений"""
    def __init__(self):
        self.relationships = {}  # id персонажа -> объект отношений
        self.married_to = None
        self.lovers = []
        self.children = []
        self.affairs = []  # тайные связи
        self.exes = []  # бывшие партнеры
        
        # типы отношений
        self.relation_types = {
            "acquainted": "Знакомы",
            "friends": "Друзья",
            "close_friends": "Близкие друзья",
            "lovers": "Любовники",
            "engaged": "Помолвлены",
            "married": "В браке",
            "enemies": "Враги",
            "ex_lovers": "Бывшие"
        }
        
        # действия и их эффекты
        self.actions = {
            "комплимент": {
                "name": "Сделать комплимент",
                "effects": {"affection": 5, "passion": 2, "trust": 1},
                "cost": 0,
                "cooldown": 1,
                "description": "Сказать что-то приятное"
            },
            "подарок": {
                "name": "Подарить подарок",
                "effects": {"affection": 10, "jealousy": -5, "trust": 3},
                "cost": 20,
                "cooldown": 3,
                "description": "Вручить ценный подарок"
            },
            "флирт": {
                "name": "Флиртовать",
                "effects": {"affection": 3, "passion": 8, "trust": -1, "jealousy": 2},
                "cost": 0,
                "cooldown": 1,
                "description": "Игриво пообщаться"
            },
            "признание": {
                "name": "Признаться в любви",
                "effects": {"trust": 15, "affection": 20, "passion": 15},
                "cost": 0,
                "cooldown": 10,
                "description": "Открыть свои чувства"
            },
            "ревность": {
                "name": "Приревновать",
                "effects": {"jealousy": 20, "trust": -10, "affection": -5},
                "cost": 0,
                "cooldown": 5,
                "description": "Выразить ревность"
            },
            "игнорирование": {
                "name": "Игнорировать",
                "effects": {"affection": -5, "trust": -3, "passion": -2},
                "cost": 0,
                "cooldown": 0,
                "description": "Не обращать внимания"
            },
            "оскорбление": {
                "name": "Оскорбить",
                "effects": {"affection": -20, "trust": -15, "passion": -10},
                "cost": 0,
                "cooldown": 10,
                "description": "Сказать грубость"
            },
            "защита": {
                "name": "Защитить",
                "effects": {"affection": 15, "trust": 10, "passion": 5},
                "cost": 0,
                "cooldown": 5,
                "description": "Вступиться за честь"
            },
            "совет": {
                "name": "Дать совет",
                "effects": {"trust": 5, "affection": 2},
                "cost": 0,
                "cooldown": 2,
                "description": "Помочь мудрым словом"
            },
            "прогулка": {
                "name": "Пойти на прогулку",
                "effects": {"affection": 8, "passion": 5, "trust": 5},
                "cost": 10,
                "cooldown": 3,
                "description": "Провести время вместе"
            },
            "ужин": {
                "name": "Пригласить на ужин",
                "effects": {"affection": 12, "passion": 8, "trust": 5},
                "cost": 30,
                "cooldown": 2,
                "description": "Разделить трапезу"
            },
            "танец": {
                "name": "Пригласить танцевать",
                "effects": {"passion": 12, "affection": 8},
                "cost": 0,
                "cooldown": 2,
                "description": "Потанцевать вместе"
            },
            "обещание": {
                "name": "Дать обещание",
                "effects": {"trust": 20, "affection": 10},
                "cost": 0,
                "cooldown": 7,
                "description": "Пообещать что-то важное"
            }
        }
    
    def add_relationship(self, npc_id: str, npc_name: str, npc_gender: str = "муж"):
        """Добавление новых отношений"""
        self.relationships[npc_id] = {
            "id": npc_id,
            "name": npc_name,
            "gender": npc_gender,
            "affection": 0,      # 0-100, симпатия
            "jealousy": 0,        # 0-100, ревность
            "trust": 50,          # 0-100, доверие
            "passion": 0,         # 0-100, страсть
            "respect": 50,        # 0-100, уважение
            "status": "acquainted",  # статус отношений
            "gifts_given": [],    # подаренные подарки
            "dates": 0,           # количество свиданий
            "secrets_shared": [], # раскрытые секреты
            "last_interaction": None,  # время последнего общения
            "interaction_count": 0,     # количество взаимодействий
            "promises": [],        # данные обещания
            "mood": "neutral",     # настроение
            "type_preference": self.get_type_preference(npc_gender)  # предпочтения
        }
    
    def get_type_preference(self, gender: str) -> str:
        """Получение предпочтений по типу отношений"""
        if gender == "муж":
            return random.choice(["нежный", "страстный", "романтичный", "дружеский"])
        else:
            return random.choice(["внимательный", "щедрый", "сильный", "заботливый"])
    
    def interact(self, npc_id: str, action: str, player_gender: str = "муж") -> Dict:
        """Взаимодействие с персонажем"""
        result = {
            "success": False,
            "message": "",
            "effects": {},
            "status_change": None,
            "special_event": None
        }
        
        if npc_id not in self.relationships:
            result["message"] = "Ты не знаком с этим человеком"
            return result
        
        if action not in self.actions:
            result["message"] = "Неизвестное действие"
            return result
        
        rel = self.relationships[npc_id]
        action_data = self.actions[action]
        
        # проверка на кд (если нужно)
        if action_data["cooldown"] > 0:
            if rel.get("last_action", {}).get(action, 0) > 0:
                result["message"] = "Это действие еще нельзя повторить"
                return result
        
        # проверка денег
        if action_data["cost"] > 0:
            # здесь должна быть проверка денег игрока
            pass
        
        # применение эффектов с учетом совместимости
        effects = self.calculate_effects(action_data["effects"], rel, player_gender, npc_id)
        
        # применяем эффекты
        for stat, change in effects.items():
            if stat in rel:
                old_value = rel[stat]
                rel[stat] = max(0, min(100, rel[stat] + change))
                result["effects"][stat] = rel[stat] - old_value
        
        # обновляем счетчики
        rel["interaction_count"] += 1
        rel["last_interaction"] = action
        if "last_action" not in rel:
            rel["last_action"] = {}
        rel["last_action"][action] = action_data["cooldown"]
        
        # уменьшаем cooldown для всех действий
        for act in list(rel.get("last_action", {}).keys()):
            rel["last_action"][act] = max(0, rel["last_action"][act] - 1)
            if rel["last_action"][act] == 0:
                del rel["last_action"][act]
        
        # проверка смены статуса
        status_change = self.check_status_change(npc_id)
        if status_change:
            result["status_change"] = status_change
        
        # реакция персонажа
        result["message"] = self.get_reaction(npc_id, action, effects)
        result["success"] = True
        
        # особые события
        special = self.check_special_events(npc_id)
        if special:
            result["special_event"] = special
        
        return result
    
    def calculate_effects(self, base_effects: Dict, rel: Dict, 
                         player_gender: str, npc_id: str) -> Dict:
        """Расчет эффектов с учетом совместимости"""
        effects = base_effects.copy()
        
        # модификатор совместимости характеров
        compatibility = self.check_compatibility(rel.get("type_preference", ""), 
                                                player_gender)
        for stat in effects:
            effects[stat] = int(effects[stat] * compatibility)
        
        # модификатор от текущих отношений
        if rel["affection"] > 70:
            for stat in effects:
                if effects[stat] > 0:
                    effects[stat] = int(effects[stat] * 1.2)
        
        # модификатор ревности
        if len(self.lovers) > 1 and npc_id in self.lovers:
            effects["jealousy"] = effects.get("jealousy", 0) + 10
            effects["trust"] = effects.get("trust", 0) - 5
        
        return effects
    
    def check_compatibility(self, preference: str, player_gender: str) -> float:
        """Проверка совместимости"""
        compatibilities = {
            "нежный": {"муж": 0.9, "жен": 1.1},
            "страстный": {"муж": 1.1, "жен": 0.9},
            "романтичный": {"муж": 1.0, "жен": 1.0},
            "дружеский": {"муж": 0.8, "жен": 1.2},
            "внимательный": {"муж": 1.1, "жен": 0.9},
            "щедрый": {"муж": 1.0, "жен": 1.0},
            "сильный": {"муж": 1.2, "жен": 0.8},
            "заботливый": {"муж": 0.9, "жен": 1.1}
        }
        
        return compatibilities.get(preference, {}).get(player_gender, 1.0)
    
    def check_status_change(self, npc_id: str) -> Optional[str]:
        """Проверка смены статуса отношений"""
        rel = self.relationships[npc_id]
        old_status = rel["status"]
        
        # расчет общего индекса отношений
        relation_index = (rel["affection"] + rel["trust"] + rel["passion"]) / 3
        
        # определение нового статуса
        if rel["affection"] >= 90 and rel["trust"] >= 85 and rel["passion"] >= 80:
            if rel["status"] == "lovers" and self.married_to is None:
                if random.random() < 0.2:  # 20% шанс предложения
                    rel["status"] = "engaged"
        
        elif rel["affection"] >= 75 and rel["passion"] >= 70 and rel["trust"] >= 70:
            if rel["status"] in ["friends", "close_friends"]:
                rel["status"] = "lovers"
                if npc_id not in self.lovers:
                    self.lovers.append(npc_id)
        
        elif rel["affection"] >= 60 and rel["trust"] >= 60:
            if rel["status"] == "friends":
                rel["status"] = "close_friends"
        
        elif rel["affection"] >= 40:
            if rel["status"] == "acquainted":
                rel["status"] = "friends"
        
        elif rel["affection"] <= -30:
            rel["status"] = "enemies"
            if npc_id in self.lovers:
                self.lovers.remove(npc_id)
                self.exes.append(npc_id)
        
        # проверка на разрыв
        elif rel["affection"] < 20 and rel["status"] in ["lovers", "engaged", "married"]:
            rel["status"] = "ex_lovers"
            if npc_id in self.lovers:
                self.lovers.remove(npc_id)
                self.exes.append(npc_id)
        
        if rel["status"] != old_status:
            return f"Статус отношений изменен: {self.relation_types[old_status]} -> {self.relation_types[rel['status']]}"
        
        return None
    
    def check_special_events(self, npc_id: str) -> Optional[Dict]:
        """Проверка особых событий"""
        rel = self.relationships[npc_id]
        
        # случайные события
        events = []
        
        # ревность
        if rel["jealousy"] > 70 and len(self.lovers) > 1:
            events.append({
                "type": "jealousy",
                "message": f"{rel['name']} устраивает сцену ревности!"
            })
        
        # признание
        if rel["affection"] > 80 and rel["status"] == "friends" and random.random() < 0.1:
            events.append({
                "type": "confession",
                "message": f"{rel['name']} признается тебе в любви!"
            })
        
        # подарок
        if rel["affection"] > 60 and random.random() < 0.05:
            events.append({
                "type": "gift",
                "message": f"{rel['name']} дарит тебе подарок!",
                "gift": random.choice(["цветы", "кольцо", "амулет"])
            })
        
        return random.choice(events) if events else None
    
    def get_reaction(self, npc_id: str, action: str, effects: Dict) -> str:
        """Получение реакции персонажа"""
        rel = self.relationships[npc_id]
        
        # базовые реакции на действия
        reactions = {
            "комплимент": {
                80: f"{rel['name']} краснеет: 'Ты такой милый...'",
                50: f"{rel['name']}: 'Спасибо, приятно слышать'",
                20: f"{rel['name']}: 'Эм... спасибо'",
                0: f"{rel['name']} игнорирует комплимент"
            },
            "флирт": {
                80: f"{rel['name']} игриво улыбается: 'Продолжай...'",
                50: f"{rel['name']} смущенно отводит взгляд",
                20: f"{rel['name']} не понимает, что ты flirt'ишь",
                0: f"{rel['name']} хмурится: 'Не надо так'"
            },
            "признание": {
                80: f"{rel['name']} обнимает тебя: 'Я тоже тебя люблю!'",
                50: f"{rel['name']} в шоке: 'Мне нужно подумать...'",
                20: f"{rel['name']} отворачивается: 'Прости, я не могу'",
                0: f"{rel['name']} в ужасе убегает!"
            },
            "подарок": {
                80: f"{rel['name']} в восторге: 'Какая прелесть!'",
                50: f"{rel['name']}: 'Спасибо, очень мило'",
                20: f"{rel['name']}: 'Зачем это?'",
                0: f"{rel['name']} отказывается от подарка"
            },
            "прогулка": {
                80: f"{rel['name']} с радостью соглашается",
                50: f"{rel['name']}: 'Почему бы и нет'",
                20: f"{rel['name']}: 'Может в другой раз'",
                0: f"{rel['name']} отказывается"
            }
        }
        
        if action in reactions:
            # ищем подходящую реакцию по уровню симпатии
            for threshold in sorted(reactions[action].keys(), reverse=True):
                if rel["affection"] >= threshold:
                    return reactions[action][threshold]
        
        # реакция на изменение отношений
        total_effect = sum(effects.values())
        if total_effect > 10:
            return f"{rel['name']} очень довольно проведенным временем!"
        elif total_effect > 0:
            return f"{rel['name']} улыбается тебе"
        elif total_effect < -10:
            return f"{rel['name']} расстроено отворачивается"
        elif total_effect < 0:
            return f"{rel['name']} хмурится"
        
        return f"{rel['name']} смотрит на тебя..."
    
    def propose_marriage(self, npc_id: str) -> Dict:
        """Предложение брака"""
        result = {
            "success": False,
            "message": "",
            "effects": {}
        }
        
        if npc_id not in self.relationships:
            result["message"] = "Ты даже не знаком с этим человеком!"
            return result
        
        rel = self.relationships[npc_id]
        
        if rel["status"] not in ["lovers", "engaged"]:
            result["message"] = f"{rel['name']} удивлен: 'Мы даже не встречались!'"
            return result
        
        if self.married_to:
            spouse_name = self.relationships[self.married_to]["name"]
            result["message"] = f"Ты уже женат на {spouse_name}!"
            return result
        
        # расчет шанса
        chance = (rel["affection"] + rel["trust"] + rel["passion"]) / 3
        
        if random.random() * 100 < chance:
            self.married_to = npc_id
            rel["status"] = "married"
            result["success"] = True
            result["message"] = f"{rel['name']} плачет от счастья: 'ДА! Я согласна!'"
            result["effects"]["affection"] = 20
        else:
            rel["affection"] -= 20
            rel["trust"] -= 10
            result["message"] = f"{rel['name']} грустно качает головой: 'Я не готова...'"
            result["effects"]["affection"] = -20
        
        return result
    
    def have_child(self) -> Dict:
        """Рождение ребенка"""
        result = {
            "success": False,
            "message": "",
            "child": None
        }
        
        if not self.married_to:
            result["message"] = "У тебя нет семьи"
            return result
        
        # шанс зачатия
        if random.random() < 0.1:  # 10% шанс
            child = {
                "name": self.generate_child_name(),
                "age": 0,
                "gender": random.choice(["сын", "дочь"]),
                "traits": random.sample(["умный", "сильный", "красивый", "хитрый", 
                                        "добрый", "смелый", "талантливый"], 2),
                "mother": self.married_to,
                "birth_day": 0
            }
            
            self.children.append(child)
            result["success"] = True
            result["child"] = child
            result["message"] = f"🎉 У тебя родился {child['gender']}! Назвали {child['name']}"
        
        return result
    
    def generate_child_name(self) -> str:
        """Генерация имени ребенка"""
        names_male = ["Иван", "Петр", "Алексей", "Дмитрий", "Николай", 
                     "Александр", "Михаил", "Андрей", "Владимир"]
        names_female = ["Анна", "Мария", "Елена", "Ольга", "Наталья",
                       "Екатерина", "Татьяна", "София", "Анастасия"]
        
        if random.choice([True, False]):
            return random.choice(names_male)
        else:
            return random.choice(names_female)
    
    def daily_update(self) -> List[str]:
        """Ежедневное обновление отношений"""
        messages = []
        
        for npc_id, rel in self.relationships.items():
            # естественное изменение отношений
            if rel["status"] == "married":
                rel["affection"] = min(100, rel["affection"] + 1)
                rel["trust"] = min(100, rel["trust"] + 1)
            
            elif rel["status"] == "lovers":
                if random.random() < 0.3:
                    rel["affection"] = max(0, rel["affection"] - 1)
            
            # ревность уменьшается со временем
            rel["jealousy"] = max(0, rel["jealousy"] - 2)
            
            # проверка на измену
            if self.married_to and len(self.lovers) > 1:
                if npc_id != self.married_to and npc_id in self.lovers:
                    if random.random() < 0.01:  # 1% шанс быть пойманным
                        messages.append(f"⚡ {rel['name']} узнал о твоей измене!")
                        spouse_rel = self.relationships[self.married_to]
                        spouse_rel["affection"] -= 30
                        spouse_rel["trust"] -= 40
                        spouse_rel["jealousy"] += 50
        
        # взросление детей
        for child in self.children[:]:
            child["age"] += 1
            if child["age"] >= 18:
                messages.append(f"👨‍🎓 Твой ребенок {child['name']} стал взрослым!")
                self.children.remove(child)
        
        return messages
    
    def get_relationship_status(self, npc_id: str) -> Dict:
        """Получение статуса отношений"""
        if npc_id not in self.relationships:
            return None
        
        rel = self.relationships[npc_id]
        return {
            "name": rel["name"],
            "status": self.relation_types[rel["status"]],
            "affection": rel["affection"],
            "trust": rel["trust"],
            "passion": rel["passion"],
            "jealousy": rel["jealousy"],
            "dates": rel["dates"],
            "mood": rel["mood"]
        }
    
    def get_family_status(self) -> Dict:
        """Получение статуса семьи"""
        status = {
            "married": None,
            "lovers": [],
            "children": [],
            "exes": []
        }
        
        if self.married_to and self.married_to in self.relationships:
            status["married"] = self.relationships[self.married_to]["name"]
        
        for lover_id in self.lovers:
            if lover_id in self.relationships:
                status["lovers"].append(self.relationships[lover_id]["name"])
        
        for child in self.children:
            status["children"].append(f"{child['name']} ({child['age']} лет)")
        
        for ex_id in self.exes:
            if ex_id in self.relationships:
                status["exes"].append(self.relationships[ex_id]["name"])
        
        return status
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            "relationships": self.relationships,
            "married_to": self.married_to,
            "lovers": self.lovers,
            "children": self.children,
            "affairs": self.affairs,
            "exes": self.exes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'RomanceSystem':
        """Загрузка из словаря"""
        system = cls()
        system.relationships = data.get("relationships", {})
        system.married_to = data.get("married_to")
        system.lovers = data.get("lovers", [])
        system.children = data.get("children", [])
        system.affairs = data.get("affairs", [])
        system.exes = data.get("exes", [])
        return system