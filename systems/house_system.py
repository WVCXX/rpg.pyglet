import random
from typing import Dict, List, Optional

class HouseSystem:
    """Система дома с новыми фичами"""
    
    HOUSE_TYPES = {
        "комната": {
            "price": 500,
            "level": 1,
            "rooms": 1,
            "storage_slots": 20,
            "description": "Маленькая комната в таверне",
            "upgrade_to": "маленький_дом",
            "image": "🏠"
        },
        "маленький_дом": {
            "price": 2000,
            "level": 2,
            "rooms": 3,
            "storage_slots": 50,
            "description": "Небольшой дом на окраине",
            "upgrade_to": "дом",
            "image": "🏡"
        },
        "дом": {
            "price": 5000,
            "level": 3,
            "rooms": 5,
            "storage_slots": 100,
            "description": "Дом в центре города",
            "upgrade_to": "особняк",
            "image": "🏘️"
        },
        "особняк": {
            "price": 15000,
            "level": 4,
            "rooms": 10,
            "storage_slots": 200,
            "description": "Роскошный особняк",
            "upgrade_to": "замок",
            "image": "🏰"
        },
        "замок": {
            "price": 50000,
            "level": 5,
            "rooms": 20,
            "storage_slots": 500,
            "description": "Настоящий замок",
            "upgrade_to": None,
            "image": "🏯"
        }
    }
    
    FURNITURE = {
        "кровать": {
            "price": 100,
            "effect": {"rest_bonus": 20, "comfort": 10},
            "description": "Обычная кровать",
            "level_req": 1,
            "image": "🛏️"
        },
        "роскошная_кровать": {
            "price": 500,
            "effect": {"rest_bonus": 50, "comfort": 30, "prestige": 10},
            "description": "Кровать с балдахином",
            "level_req": 2,
            "image": "👑"
        },
        "стол": {
            "price": 50,
            "effect": {"craft_bonus": 5, "comfort": 5},
            "description": "Обычный стол",
            "level_req": 1,
            "image": "🪑"
        },
        "верстак": {
            "price": 300,
            "effect": {"craft_bonus": 20, "comfort": 5},
            "description": "Верстак для крафта",
            "level_req": 2,
            "image": "🔨"
        },
        "сундук": {
            "price": 100,
            "effect": {"storage": 20, "comfort": 5},
            "description": "Дополнительное хранилище",
            "level_req": 1,
            "image": "📦"
        },
        "большой_сундук": {
            "price": 400,
            "effect": {"storage": 50, "comfort": 10},
            "description": "Вместительный сундук",
            "level_req": 2,
            "image": "🗄️"
        },
        "печь": {
            "price": 200,
            "effect": {"cooking_bonus": 15, "comfort": 10},
            "description": "Печь для готовки",
            "level_req": 1,
            "image": "🔥"
        },
        "алхимический_стол": {
            "price": 500,
            "effect": {"alchemy_bonus": 25, "comfort": 15, "prestige": 20},
            "description": "Стол для зелий",
            "level_req": 3,
            "image": "⚗️"
        },
        "кресло": {
            "price": 75,
            "effect": {"comfort": 10},
            "description": "Удобное кресло",
            "level_req": 1,
            "image": "🪑"
        },
        "ковер": {
            "price": 150,
            "effect": {"comfort": 15, "prestige": 5},
            "description": "Красивый ковер",
            "level_req": 1,
            "image": "🧶"
        },
        "картина": {
            "price": 200,
            "effect": {"comfort": 20, "prestige": 10},
            "description": "Картина в раме",
            "level_req": 2,
            "image": "🖼️"
        },
        "люстра": {
            "price": 300,
            "effect": {"comfort": 25, "prestige": 15},
            "description": "Хрустальная люстра",
            "level_req": 3,
            "image": "💡"
        }
    }
    
    # Новые фичи для дома
    GARDEN_ITEMS = {
        "грядка": {
            "price": 100,
            "effect": {"garden_slots": 5},
            "description": "Грядка для выращивания растений",
            "level_req": 2,
            "image": "🌱"
        },
        "теплица": {
            "price": 500,
            "effect": {"garden_slots": 20, "growth_bonus": 20},
            "description": "Теплица для круглогодичного выращивания",
            "level_req": 4,
            "image": "🏗️"
        }
    }
    
    STABLE_ITEMS = {
        "конюшня": {
            "price": 1000,
            "effect": {"horse_slots": 2},
            "description": "Конюшня для лошадей",
            "level_req": 3,
            "image": "🐎"
        },
        "каретный_сарай": {
            "price": 3000,
            "effect": {"horse_slots": 5, "carriage": True},
            "description": "Сарай для карет",
            "level_req": 4,
            "image": "🚐"
        }
    }
    
    SERVANT_ROOMS = {
        "комната_слуг": {
            "price": 200,
            "effect": {"servant_slots": 2},
            "description": "Комната для слуг",
            "level_req": 2,
            "image": "🧹"
        },
        "крыло_слуг": {
            "price": 1000,
            "effect": {"servant_slots": 10},
            "description": "Целое крыло для прислуги",
            "level_req": 4,
            "image": "🏛️"
        }
    }
    
    TREASURY = {
        "сундук_сокровищница": {
            "price": 500,
            "effect": {"treasury_slots": 100, "interest": 1},
            "description": "Сундук для хранения сокровищ (+1% годовых)",
            "level_req": 3,
            "image": "💎"
        },
        "банковское_хранилище": {
            "price": 5000,
            "effect": {"treasury_slots": 1000, "interest": 5},
            "description": "Надежное хранилище (+5% годовых)",
            "level_req": 5,
            "image": "🏦"
        }
    }
    
    THRONE_ROOM = {
        "трон": {
            "price": 5000,
            "effect": {"prestige": 100, "respect": 50},
            "description": "Тронный зал для замка",
            "level_req": 5,
            "image": "👑"
        }
    }
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.house = game_state.house
        self.player = game_state.player
        
        # Новые параметры дома
        if "garden" not in self.house:
            self.house["garden"] = {"slots": 0, "plants": [], "items": []}
        if "stable" not in self.house:
            self.house["stable"] = {"slots": 0, "horses": []}
        if "servants" not in self.house:
            self.house["servants"] = {"slots": 0, "servants": []}
        if "treasury" not in self.house:
            self.house["treasury"] = {"slots": 0, "items": [], "gold": 0}
        if "throne" not in self.house:
            self.house["throne"] = False
    
    def buy_house(self, house_type: str, location: str) -> Dict:
        """Покупка дома"""
        result = {
            "success": False,
            "message": "",
            "house": None
            }
    
        if house_type not in self.HOUSE_TYPES:
            result["message"] = "❌ Такого типа дома не существует"
            return result
    
        house_data = self.HOUSE_TYPES[house_type]
        price = house_data["price"]
    
        if self.player["money"] < price:
            result["message"] = f"❌ Не хватает денег! Нужно {price} золота"
            return result
    
        self.player["money"] -= price

        from core.game_state import Inventory
        storage = Inventory()
    
        new_house = {
            "owned": True,
            "type": house_type,
            "level": house_data["level"],
            "location": location,
            "furniture": [],
            "storage": storage,
            "upgrades": [],
            "comfort": 0,
            "prestige": 0,
            "description": house_data["description"],
            "garden": {"slots": 0, "plants": [], "items": []},
            "stable": {"slots": 0, "horses": []},
            "servants": {"slots": 0, "servants": []},
            "treasury": {"slots": 0, "items": [], "gold": 0},
            "throne": False
            }
    
    # Обновляем и self.house, и game_state.house
        self.house = new_house
        self.game_state.house = new_house
    
        result["success"] = True
        result["message"] = f"✅ Ты купил {house_type}! Осталось {self.player['money']} золота"
        result["house"] = self.house
    
        return result
    
    def upgrade_house(self) -> Dict:
        """Улучшение дома"""
        result = {
            "success": False,
            "message": ""
    }
    
        if not self.house["owned"]:
            result["message"] = "❌ У тебя нет дома"
            return result
    
        current_type = self.house["type"]
        if current_type not in self.HOUSE_TYPES:
            result["message"] = "❌ Ошибка типа дома"
            return result
    
        next_type = self.HOUSE_TYPES[current_type].get("upgrade_to")
        if not next_type:
            result["message"] = "❌ Дом уже максимального уровня"
            return result
    
        next_house = self.HOUSE_TYPES[next_type]
        price = next_house["price"] - self.HOUSE_TYPES[current_type]["price"]
    
        if self.player["money"] < price:
            result["message"] = f"❌ Не хватает денег! Нужно еще {price} золота"
            return result
    
        self.player["money"] -= price
    
        old_furniture = self.house["furniture"]
        old_storage = self.house["storage"]
        old_garden = self.house["garden"]
        old_stable = self.house["stable"]
        old_servants = self.house["servants"]
        old_treasury = self.house["treasury"]
        old_comfort = self.house["comfort"]
        old_prestige = self.house["prestige"]
        old_upgrades = self.house["upgrades"]
        old_throne = self.house["throne"]
    
        upgraded_house = {
        "owned": True,
        "type": next_type,
        "level": next_house["level"],
        "location": self.house["location"],
        "furniture": old_furniture,
        "storage": old_storage,
        "upgrades": old_upgrades,
        "comfort": old_comfort,
        "prestige": old_prestige,
        "description": next_house["description"],
        "garden": old_garden,
        "stable": old_stable,
        "servants": old_servants,
        "treasury": old_treasury,
        "throne": old_throne
    }
    
    # Обновляем и self.house, и game_state.house
        self.house = upgraded_house
        self.game_state.house = upgraded_house
    
        result["success"] = True
        result["message"] = f"✅ Дом улучшен до {next_type}!"
    
        return result

    def buy_furniture(self, furniture_id: str) -> Dict:
        """Покупка мебели"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"]:
            result["message"] = "❌ У тебя нет дома"
            return result
        
        if furniture_id not in self.FURNITURE:
            result["message"] = "❌ Такой мебели нет"
            return result
        
        furniture = self.FURNITURE[furniture_id]
        
        # Проверка уровня дома
        if furniture["level_req"] > self.house["level"]:
            result["message"] = f"❌ Нужен дом {furniture['level_req']} уровня"
            return result
        
        # Проверка денег
        if self.player["money"] < furniture["price"]:
            result["message"] = f"❌ Не хватает денег! Нужно {furniture['price']} золота"
            return result
        
        self.player["money"] -= furniture["price"]
        
        # Добавляем мебель
        new_furniture = {
            "id": furniture_id,
            "name": furniture_id.replace('_', ' ').title(),
            "effect": furniture["effect"],
            "description": furniture["description"],
            "image": furniture["image"]
        }
        
        self.house["furniture"].append(new_furniture)
        
        # Обновляем комфорт и престиж
        if "comfort" in furniture["effect"]:
            self.house["comfort"] += furniture["effect"]["comfort"]
        if "prestige" in furniture["effect"]:
            self.house["prestige"] += furniture["effect"]["prestige"]
        
        result["success"] = True
        result["message"] = f"✅ Куплено: {new_furniture['name']}"
        
        return result
    
    def rest(self) -> Dict:
        """Отдых в доме"""
        result = {
            "health_restored": 0,
            "mana_restored": 0,
            "message": ""
        }
        
        if not self.house["owned"]:
            result["message"] = "❌ У тебя нет дома"
            return result
        
        # Базовое восстановление
        base_rest = 30
        
        # Бонус от мебели
        rest_bonus = 0
        for furniture in self.house["furniture"]:
            if "rest_bonus" in furniture["effect"]:
                rest_bonus += furniture["effect"]["rest_bonus"]
        
        total_rest = base_rest + rest_bonus
        
        # Восстановление
        old_health = self.player["health"]
        old_mana = self.player["mana"]
        
        self.player["health"] = min(self.player["max_health"], self.player["health"] + total_rest)
        self.player["mana"] = min(self.player["max_mana"], self.player["mana"] + total_rest)
        
        health_restored = self.player["health"] - old_health
        mana_restored = self.player["mana"] - old_mana
        
        result["health_restored"] = health_restored
        result["mana_restored"] = mana_restored
        result["message"] = f"💤 Отдых в доме восстановил {health_restored} здоровья и {mana_restored} маны"
        
        return result
    
    def get_storage_items(self) -> Dict:
        """Получение предметов в хранилище"""
        if not self.house["owned"]:
            return {}
        return self.house["storage"].get_all_items()
    
    def move_to_storage(self, category: str, item: str, count: int = 1) -> bool:
        """Переместить предмет в хранилище"""
        if not self.house["owned"]:
            return False
        
        # Проверяем, есть ли предмет у игрока
        if self.player["inventory"].remove_item(category, item, count):
            # Добавляем в хранилище
            self.house["storage"].add_item(category, item, count)
            return True
        return False
    
    def take_from_storage(self, category: str, item: str, count: int = 1) -> bool:
        """Взять предмет из хранилища"""
        if not self.house["owned"]:
            return False
        
        # Проверяем, есть ли предмет в хранилище
        if self.house["storage"].remove_item(category, item, count):
            # Добавляем игроку
            self.player["inventory"].add_item(category, item, count)
            return True
        return False
    
    def buy_garden_item(self, item_id: str) -> Dict:
        """Покупка садовых принадлежностей"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"]:
            result["message"] = "❌ У тебя нет дома"
            return result
        
        if item_id not in self.GARDEN_ITEMS:
            result["message"] = "❌ Такого предмета нет"
            return result
        
        item = self.GARDEN_ITEMS[item_id]
        
        if item["level_req"] > self.house["level"]:
            result["message"] = f"❌ Нужен дом {item['level_req']} уровня"
            return result
        
        if self.player["money"] < item["price"]:
            result["message"] = f"❌ Не хватает денег! Нужно {item['price']} золота"
            return result
        
        self.player["money"] -= item["price"]
        
        # Применяем эффект
        if "garden_slots" in item["effect"]:
            self.house["garden"]["slots"] += item["effect"]["garden_slots"]
        
        self.house["garden"]["items"] = self.house["garden"].get("items", [])
        self.house["garden"]["items"].append({
            "id": item_id,
            "name": item_id.replace('_', ' ').title(),
            "image": item["image"]
        })
        
        result["success"] = True
        result["message"] = f"✅ Куплено: {item['description']}"
        
        return result
    
    def buy_stable_item(self, item_id: str) -> Dict:
        """Покупка конюшни"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"]:
            result["message"] = "❌ У тебя нет дома"
            return result
        
        if item_id not in self.STABLE_ITEMS:
            result["message"] = "❌ Такого предмета нет"
            return result
        
        item = self.STABLE_ITEMS[item_id]
        
        if item["level_req"] > self.house["level"]:
            result["message"] = f"❌ Нужен дом {item['level_req']} уровня"
            return result
        
        if self.player["money"] < item["price"]:
            result["message"] = f"❌ Не хватает денег! Нужно {item['price']} золота"
            return result
        
        self.player["money"] -= item["price"]
        
        if "horse_slots" in item["effect"]:
            self.house["stable"]["slots"] += item["effect"]["horse_slots"]
        
        result["success"] = True
        result["message"] = f"✅ Куплено: {item['description']}"
        
        return result
    
    def buy_horse(self, horse_type: str) -> Dict:
        """Покупка лошади"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"] or self.house["stable"]["slots"] == 0:
            result["message"] = "❌ Нет конюшни"
            return result
        
        horses = {
            "рабочая_лошадь": {"price": 200, "speed": 1.2, "carry": 50},
            "верховая_лошадь": {"price": 500, "speed": 1.5, "carry": 30},
            "боевой_конь": {"price": 1000, "speed": 1.3, "carry": 80, "combat": True},
            "скакун": {"price": 2000, "speed": 2.0, "carry": 40}
        }
        
        if horse_type not in horses:
            result["message"] = "❌ Такой лошади нет"
            return result
        
        horse = horses[horse_type]
        
        if len(self.house["stable"]["horses"]) >= self.house["stable"]["slots"]:
            result["message"] = "❌ Нет мест в конюшне"
            return result
        
        if self.player["money"] < horse["price"]:
            result["message"] = f"❌ Не хватает денег! Нужно {horse['price']} золота"
            return result
        
        self.player["money"] -= horse["price"]
        
        new_horse = {
            "type": horse_type,
            "name": f"{horse_type} #{len(self.house['stable']['horses'])+1}",
            "speed": horse["speed"],
            "carry": horse["carry"],
            "health": 100,
            "combat": horse.get("combat", False)
        }
        
        self.house["stable"]["horses"].append(new_horse)
        
        result["success"] = True
        result["message"] = f"✅ Куплена {horse_type.replace('_', ' ')}!"
        result["horse"] = new_horse
        
        return result
    
    def buy_servant_room(self, item_id: str) -> Dict:
        """Покупка комнаты для слуг"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"]:
            result["message"] = "❌ У тебя нет дома"
            return result
        
        if item_id not in self.SERVANT_ROOMS:
            result["message"] = "❌ Такого предмета нет"
            return result
        
        item = self.SERVANT_ROOMS[item_id]
        
        if item["level_req"] > self.house["level"]:
            result["message"] = f"❌ Нужен дом {item['level_req']} уровня"
            return result
        
        if self.player["money"] < item["price"]:
            result["message"] = f"❌ Не хватает денег! Нужно {item['price']} золота"
            return result
        
        self.player["money"] -= item["price"]
        
        if "servant_slots" in item["effect"]:
            self.house["servants"]["slots"] += item["effect"]["servant_slots"]
        
        result["success"] = True
        result["message"] = f"✅ Куплено: {item['description']}"
        
        return result
    
    def hire_servant(self, servant_type: str) -> Dict:
        """Нанять слугу"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"] or self.house["servants"]["slots"] == 0:
            result["message"] = "❌ Нет комнат для слуг"
            return result
        
        servants = {
            "уборщик": {"salary": 10, "skill": "clean", "effect": {"comfort": 5}},
            "повар": {"salary": 30, "skill": "cook", "effect": {"food_quality": 20}},
            "садовник": {"salary": 20, "skill": "garden", "effect": {"growth_bonus": 10}},
            "конюх": {"salary": 15, "skill": "stable", "effect": {"horse_health": 10}},
            "казначей": {"salary": 50, "skill": "treasury", "effect": {"interest": 2}},
            "телохранитель": {"salary": 100, "skill": "combat", "effect": {"protection": 20}}
        }
        
        if servant_type not in servants:
            result["message"] = "❌ Такой профессии нет"
            return result
        
        servant = servants[servant_type]
        
        if len(self.house["servants"]["servants"]) >= self.house["servants"]["slots"]:
            result["message"] = "❌ Нет мест для слуг"
            return result
        
        # Проверка, можем ли мы платить зарплату
        if self.player["money"] < servant["salary"] * 7:  # Недельная зарплата
            result["message"] = "❌ Не хватает денег на зарплату"
            return result
        
        new_servant = {
            "type": servant_type,
            "name": self.generate_servant_name(),
            "salary": servant["salary"],
            "skill": servant["skill"],
            "effect": servant["effect"],
            "loyalty": 50
        }
        
        self.house["servants"]["servants"].append(new_servant)
        
        result["success"] = True
        result["message"] = f"✅ Нанят {servant_type}: {new_servant['name']}"
        result["servant"] = new_servant
        
        return result
    
    def generate_servant_name(self) -> str:
        """Генерация имени слуги"""
        first_names = ["Иван", "Петр", "Сидор", "Матвей", "Кузьма", "Федор", "Егор"]
        last_names = ["Петров", "Сидоров", "Кузнецов", "Попов", "Смирнов"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def buy_treasury_item(self, item_id: str) -> Dict:
        """Покупка сокровищницы"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"]:
            result["message"] = "❌ У тебя нет дома"
            return result
        
        if item_id not in self.TREASURY:
            result["message"] = "❌ Такого предмета нет"
            return result
        
        item = self.TREASURY[item_id]
        
        if item["level_req"] > self.house["level"]:
            result["message"] = f"❌ Нужен дом {item['level_req']} уровня"
            return result
        
        if self.player["money"] < item["price"]:
            result["message"] = f"❌ Не хватает денег! Нужно {item['price']} золота"
            return result
        
        self.player["money"] -= item["price"]
        
        if "treasury_slots" in item["effect"]:
            self.house["treasury"]["slots"] += item["effect"]["treasury_slots"]
        
        result["success"] = True
        result["message"] = f"✅ Куплено: {item['description']}"
        
        return result
    
    def buy_throne(self) -> Dict:
        """Покупка трона"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"]:
            result["message"] = "❌ У тебя нет дома"
            return result
        
        if self.house["type"] != "замок":
            result["message"] = "❌ Трон можно поставить только в замке"
            return result
        
        item = self.THRONE_ROOM["трон"]
        
        if self.player["money"] < item["price"]:
            result["message"] = f"❌ Не хватает денег! Нужно {item['price']} золота"
            return result
        
        self.player["money"] -= item["price"]
        
        self.house["throne"] = True
        self.house["prestige"] += item["effect"]["prestige"]
        
        result["success"] = True
        result["message"] = "✅ Трон установлен! Теперь ты настоящий правитель!"
        
        return result
    
    def daily_update(self) -> List[str]:
        """Ежедневное обновление дома"""
        messages = []
        
        if not self.house["owned"]:
            return messages
        
        # Платим зарплату слугам
        total_salary = sum(s["salary"] for s in self.house["servants"]["servants"])
        if self.player["money"] >= total_salary:
            self.player["money"] -= total_salary
            # Повышаем лояльность
            for servant in self.house["servants"]["servants"]:
                servant["loyalty"] = min(100, servant["loyalty"] + 1)
        else:
            messages.append("⚠️ Не хватает денег на зарплату слугам!")
            for servant in self.house["servants"]["servants"]:
                servant["loyalty"] = max(0, servant["loyalty"] - 10)
                if servant["loyalty"] <= 0:
                    messages.append(f"❌ {servant['name']} уволился!")
                    self.house["servants"]["servants"].remove(servant)
        
        # Проценты по вкладам
        if self.house["treasury"]["slots"] > 0:
            interest_items = [f for f in self.house["furniture"] 
                            if "interest" in f.get("effect", {})]
            for item in interest_items:
                interest = item["effect"]["interest"]
                bonus = int(self.house["treasury"]["gold"] * interest / 100)
                self.house["treasury"]["gold"] += bonus
                if bonus > 0:
                    messages.append(f"💰 Проценты по вкладу: +{bonus} золота")
        
        # Рост растений в саду
        if self.house["garden"]["plants"]:
            for plant in self.house["garden"]["plants"]:
                plant["growth"] += 1
                if plant["growth"] >= plant["max_growth"]:
                    messages.append(f"🌱 {plant['name']} созрел!")
        
        return messages
    
    def plant_seed(self, seed_type: str) -> Dict:
        """Посадка семян"""
        result = {
            "success": False,
            "message": ""
        }
        
        if not self.house["owned"] or self.house["garden"]["slots"] == 0:
            result["message"] = "❌ Нет сада"
            return result
        
        seeds = {
            "морковь": {"growth_time": 5, "yield": 3, "price": 10},
            "картошка": {"growth_time": 7, "yield": 5, "price": 15},
            "помидор": {"growth_time": 6, "yield": 4, "price": 20},
            "пшеница": {"growth_time": 10, "yield": 10, "price": 5},
            "лечебная_трава": {"growth_time": 8, "yield": 2, "price": 50}
        }
        
        if seed_type not in seeds:
            result["message"] = "❌ Нет таких семян"
            return result
        
        seed = seeds[seed_type]
        
        # Проверяем, есть ли семена в инвентаре
        if self.player["inventory"].get_item_count("seeds", seed_type) == 0:
            result["message"] = "❌ Нет семян в инвентаре"
            return result
        
        self.player["inventory"].remove_item("seeds", seed_type, 1)
        
        plant = {
            "type": seed_type,
            "name": seed_type.capitalize(),
            "growth": 0,
            "max_growth": seed["growth_time"],
            "yield": seed["yield"]
        }
        
        self.house["garden"]["plants"].append(plant)
        
        result["success"] = True
        result["message"] = f"🌱 Посажено: {seed_type}"
        
        return result
    
    def harvest_garden(self) -> Dict:
        """Сбор урожая"""
        result = {
            "success": False,
            "message": "",
            "harvest": []
        }
        
        if not self.house["owned"] or not self.house["garden"]["plants"]:
            result["message"] = "❌ Нечего собирать"
            return result
        
        harvested = []
        for plant in self.house["garden"]["plants"][:]:
            if plant["growth"] >= plant["max_growth"]:
                harvested.append(plant)
                self.house["garden"]["plants"].remove(plant)
                
                # Добавляем урожай в инвентарь
                self.player["inventory"].add_item("food", plant["type"], plant["yield"])
        
        if harvested:
            result["success"] = True
            result["message"] = f"✅ Собрано {len(harvested)} растений"
            result["harvest"] = harvested
        else:
            result["message"] = "❌ Ничего не созрело"
        
        return result
    
    def get_house_info(self) -> Dict:
        """Получение информации о доме"""
        if not self.house["owned"]:
            return {"owned": False}
        
        return {
            "owned": True,
            "type": self.house["type"],
            "level": self.house["level"],
            "location": self.house["location"],
            "description": self.house["description"],
            "image": self.HOUSE_TYPES[self.house["type"]]["image"],
            "furniture_count": len(self.house["furniture"]),
            "comfort": self.house["comfort"],
            "prestige": self.house["prestige"],
            "storage_used": sum(count for _, count in self.house["storage"].get_all_items().get("misc", [])),
            "storage_max": self.HOUSE_TYPES[self.house["type"]]["storage_slots"],
            "furniture_list": [f["name"] for f in self.house["furniture"]],
            
            # Новые параметры
            "garden": {
                "slots": self.house["garden"]["slots"],
                "plants": len(self.house["garden"]["plants"]),
                "items": self.house["garden"].get("items", [])
            },
            "stable": {
                "slots": self.house["stable"]["slots"],
                "horses": len(self.house["stable"]["horses"]),
                "horse_list": self.house["stable"]["horses"]
            },
            "servants": {
                "slots": self.house["servants"]["slots"],
                "servants": len(self.house["servants"]["servants"]),
                "servant_list": self.house["servants"]["servants"]
            },
            "treasury": {
                "slots": self.house["treasury"]["slots"],
                "gold": self.house["treasury"]["gold"],
                "items": len(self.house["treasury"]["items"])
            },
            "throne": self.house["throne"]
        }