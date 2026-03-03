import random
from typing import Dict, List, Optional

class CraftSystem:
    """Система крафта"""
    
    RECIPES = {
        # Оружие
        "деревянный_меч": {
            "name": "Деревянный меч",
            "category": "weapons",
            "materials": {"дерево": 2},
            "skill": "кузнечное_дело",
            "skill_req": 1,
            "time": 2,
            "result": {"damage": 5, "durability": 20},
            "description": "Простой деревянный меч для тренировок"
        },
        "каменный_топор": {
            "name": "Каменный топор",
            "category": "weapons",
            "materials": {"камень": 3, "дерево": 1},
            "skill": "кузнечное_дело",
            "skill_req": 2,
            "time": 3,
            "result": {"damage": 8, "durability": 30},
            "description": "Топор из камня"
        },
        "стальной_меч": {
            "name": "Стальной меч",
            "category": "weapons",
            "materials": {"железо": 5, "уголь": 3},
            "skill": "кузнечное_дело",
            "skill_req": 5,
            "time": 5,
            "result": {"damage": 15, "durability": 50},
            "description": "Качественный стальной меч"
        },
        
        # Броня
        "кожаная_броня": {
            "name": "Кожаная броня",
            "category": "armor",
            "materials": {"кожа": 4, "нитка": 2},
            "skill": "кожевничество",
            "skill_req": 2,
            "time": 3,
            "result": {"defense": 5, "durability": 25},
            "description": "Легкая кожаная броня"
        },
        "кольчуга": {
            "name": "Кольчуга",
            "category": "armor",
            "materials": {"железо": 8, "уголь": 5},
            "skill": "кузнечное_дело",
            "skill_req": 4,
            "time": 6,
            "result": {"defense": 10, "durability": 40},
            "description": "Надежная кольчуга"
        },
        
        # Зелья
        "зелье_здоровья": {
            "name": "Зелье здоровья",
            "category": "potions",
            "materials": {"лечебная_трава": 2, "вода": 1},
            "skill": "алхимия",
            "skill_req": 1,
            "time": 1,
            "result": {"heal": 30},
            "description": "Восстанавливает 30 здоровья"
        },
        "зелье_маны": {
            "name": "Зелье маны",
            "category": "potions",
            "materials": {"магическая_трава": 2, "вода": 1},
            "skill": "алхимия",
            "skill_req": 2,
            "time": 1,
            "result": {"mana": 25},
            "description": "Восстанавливает 25 маны"
        },
        "противоядие": {
            "name": "Противоядие",
            "category": "potions",
            "materials": {"редкая_трава": 2, "спирт": 1},
            "skill": "алхимия",
            "skill_req": 3,
            "time": 2,
            "result": {"cure": "отравление"},
            "description": "Лечит от отравления"
        },
        
        # Еда
        "хлеб": {
            "name": "Хлеб",
            "category": "food",
            "materials": {"мука": 2, "вода": 1},
            "skill": "кулинария",
            "skill_req": 1,
            "time": 1,
            "result": {"food": 20, "heal": 5},
            "description": "Свежеиспеченный хлеб"
        },
        "мясной_пирог": {
            "name": "Мясной пирог",
            "category": "food",
            "materials": {"мука": 3, "мясо": 2, "масло": 1},
            "skill": "кулинария",
            "skill_req": 3,
            "time": 2,
            "result": {"food": 50, "heal": 15, "buff": "сытость"},
            "description": "Сытный мясной пирог"
        },
        
        # Стрелы и боеприпасы
        "стрела": {
            "name": "Стрела",
            "category": "ammo",
            "materials": {"дерево": 1, "перо": 1, "железо": 1},
            "skill": "ремесло",
            "skill_req": 2,
            "time": 1,
            "result": {"count": 10},
            "description": "10 стрел"
        },
        
        # Ключи и инструменты
        "отмычка": {
            "name": "Отмычка",
            "category": "tools",
            "materials": {"железо": 1},
            "skill": "воровство",
            "skill_req": 2,
            "time": 1,
            "result": {"uses": 5},
            "description": "Инструмент для взлома замков"
        }
    }
    
    SKILLS = {
        "кузнечное_дело": {
            "name": "⚒️ Кузнечное дело",
            "description": "Создание оружия и брони",
            "base_chance": 0.7
        },
        "алхимия": {
            "name": "⚗️ Алхимия",
            "description": "Варка зелий и эликсиров",
            "base_chance": 0.8
        },
        "кулинария": {
            "name": "🍳 Кулинария",
            "description": "Приготовление еды",
            "base_chance": 0.9
        },
        "кожевничество": {
            "name": "🧵 Кожевничество",
            "description": "Работа с кожей",
            "base_chance": 0.75
        },
        "ремесло": {
            "name": "🔨 Ремесло",
            "description": "Общее ремесло",
            "base_chance": 0.8
        },
        "воровство": {
            "name": "🗝️ Воровство",
            "description": "Создание воровских инструментов",
            "base_chance": 0.6
        }
    }
    
    def __init__(self, player):
        self.player = player
        self.crafting_queue = []
        self.skill_levels = player.get("craft_skills", {})
        
        # Инициализация навыков
        for skill in self.SKILLS:
            if skill not in self.skill_levels:
                self.skill_levels[skill] = 0
    
    def get_available_recipes(self) -> List[Dict]:
        """Получение доступных рецептов"""
        available = []
        
        for recipe_id, recipe in self.RECIPES.items():
            # Проверка уровня навыка
            if self.skill_levels[recipe["skill"]] >= recipe["skill_req"]:
                # Проверка наличия материалов
                if self.has_materials(recipe["materials"]):
                    available.append({
                        "id": recipe_id,
                        **recipe
                    })
        
        return available
    
    def has_materials(self, materials: Dict[str, int]) -> bool:
        """Проверка наличия материалов"""
        for mat, count in materials.items():
            found = False
            for cat in ["misc", "ingredients", "food"]:
                if self.player["inventory"].get_item_count(cat, mat) >= count:
                    found = True
                    break
            if not found:
                return False
        return True
    
    def consume_materials(self, materials: Dict[str, int]) -> bool:
        """Потребление материалов"""
        for mat, count in materials.items():
            consumed = False
            for cat in ["misc", "ingredients", "food"]:
                if self.player["inventory"].get_item_count(cat, mat) >= count:
                    if self.player["inventory"].remove_item(cat, mat, count):
                        consumed = True
                        break
            if not consumed:
                return False
        return True
    
    def craft(self, recipe_id: str, count: int = 1) -> Dict:
        """Создание предмета"""
        result = {
            "success": False,
            "message": "",
            "items": []
        }
        
        if recipe_id not in self.RECIPES:
            result["message"] = "❌ Рецепт не найден"
            return result
        
        recipe = self.RECIPES[recipe_id]
        
        # Проверка навыка
        if self.skill_levels[recipe["skill"]] < recipe["skill_req"]:
            result["message"] = f"❌ Нужен уровень {recipe['skill_req']} навыка {self.SKILLS[recipe['skill']]['name']}"
            return result
        
        # Проверка материалов
        if not self.has_materials(recipe["materials"]):
            result["message"] = "❌ Не хватает материалов"
            return result
        
        # Шанс успеха
        base_chance = self.SKILLS[recipe["skill"]]["base_chance"]
        skill_bonus = self.skill_levels[recipe["skill"]] * 0.05
        luck_bonus = self.player["stats"]["удача"] * 0.01
        total_chance = min(0.95, base_chance + skill_bonus + luck_bonus)
        
        crafted_count = 0
        failed_count = 0
        
        for i in range(count):
            if random.random() < total_chance:
                # Успех
                self.consume_materials(recipe["materials"])
                
                item_count = 1
                if "result" in recipe and "count" in recipe["result"]:
                    item_count = recipe["result"]["count"]
                
                self.player["inventory"].add_item(recipe["category"], recipe_id, item_count)
                
                # Повышение навыка
                self.skill_levels[recipe["skill"]] += 0.1
                if random.random() < 0.1:  # 10% шанс повысить уровень
                    self.skill_levels[recipe["skill"]] += 1
                
                crafted_count += 1
                result["items"].append(recipe_id)
            else:
                # Неудача - материалы теряются
                self.consume_materials(recipe["materials"])
                failed_count += 1
        
        if crafted_count > 0:
            result["success"] = True
            result["message"] = f"✅ Создано {crafted_count} {recipe['name']}"
            if failed_count > 0:
                result["message"] += f" (неудач: {failed_count})"
            
            exp_gain = crafted_count * 10
            self.player["exp"] += exp_gain
        else:
            result["message"] = f"❌ Все попытки ({failed_count}) провалились"
        
        return result
    
    def get_skill_info(self) -> Dict:
        """Получение информации о навыках"""
        info = {}
        for skill_id, skill_data in self.SKILLS.items():
            info[skill_id] = {
                "name": skill_data["name"],
                "description": skill_data["description"],
                "level": self.skill_levels[skill_id],
                "chance": self.SKILLS[skill_id]["base_chance"] + self.skill_levels[skill_id] * 0.05
            }
        return info
    
    def learn_recipe(self, recipe_id: str) -> bool:
        """Изучение нового рецепта"""
        # В будущем можно добавить изучение рецептов из книг/учителей
        return False