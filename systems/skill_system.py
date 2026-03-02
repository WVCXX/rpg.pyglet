import random
import json
from typing import Dict, List, Optional

class SkillSystem:
    """Система навыков и прокачки"""
    
    SKILL_TREES = {
        "воин": {
            "name": "🌪 Путь Воина",
            "color": "#ff4444",
            "skills": {
                "сильный_удар": {
                    "name": "Сильный удар",
                    "description": "Мощная атака, наносящая 150% урона",
                    "max_level": 5,
                    "cooldown": 2,
                    "mana_cost": 5,
                    "base_damage": 1.5,
                    "requirements": {"сила": 10},
                    "effects": {"damage_mult": 0.1}  # +10% урона за уровень
                },
                "кровавая_жажда": {
                    "name": "Кровавая жажда",
                    "description": "Восстанавливает 20% от нанесенного урона",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 10,
                    "base_damage": 1.2,
                    "requirements": {"сила": 12, "выносливость": 10},
                    "effects": {"lifesteal": 0.05}  # +5% вампиризма за уровень
                },
                "блок_щитом": {
                    "name": "Блок щитом",
                    "description": "Снижает получаемый урон на 50% на 2 хода",
                    "max_level": 3,
                    "cooldown": 3,
                    "mana_cost": 0,
                    "requirements": {"сила": 8, "выносливость": 12},
                    "effects": {"block": 0.1}  # +10% блокирования за уровень
                },
                "ярость": {
                    "name": "Ярость",
                    "description": "Увеличивает урон на 30% на 3 хода",
                    "max_level": 3,
                    "cooldown": 5,
                    "mana_cost": 15,
                    "requirements": {"сила": 15, "удача": 8},
                    "effects": {"fury_damage": 0.1}  # +10% урона в ярости
                },
                "рассекающий_удар": {
                    "name": "Рассекающий удар",
                    "description": "Атакует всех врагов",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 20,
                    "base_damage": 0.8,
                    "requirements": {"сила": 14, "ловкость": 10},
                    "effects": {"aoe_damage": 0.1}  # +10% урона по площади
                }
            }
        },
        "маг": {
            "name": "🔮 Путь Мага",
            "color": "#4444ff",
            "skills": {
                "огненный_шар": {
                    "name": "Огненный шар",
                    "description": "Наносит магический урон и поджигает",
                    "max_level": 5,
                    "cooldown": 2,
                    "mana_cost": 15,
                    "base_damage": 1.4,
                    "requirements": {"интеллект": 12},
                    "effects": {"fire_damage": 0.1}  # +10% урона огнем
                },
                "ледяная_стрела": {
                    "name": "Ледяная стрела",
                    "description": "Замедляет врага",
                    "max_level": 5,
                    "cooldown": 1,
                    "mana_cost": 10,
                    "base_damage": 1.2,
                    "requirements": {"интеллект": 10},
                    "effects": {"slow": 0.1}  # +10% замедления
                },
                "магический_щит": {
                    "name": "Магический щит",
                    "description": "Поглощает урон",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 20,
                    "requirements": {"интеллект": 10, "мудрость": 12},
                    "effects": {"shield": 10}  # +10 поглощения за уровень
                },
                "лечение": {
                    "name": "Лечение",
                    "description": "Восстанавливает здоровье",
                    "max_level": 5,
                    "cooldown": 3,
                    "mana_cost": 15,
                    "base_heal": 1.3,
                    "requirements": {"мудрость": 12},
                    "effects": {"heal": 5}  # +5 лечения за уровень
                },
                "цепная_молния": {
                    "name": "Цепная молния",
                    "description": "Бьет по нескольким врагам",
                    "max_level": 3,
                    "cooldown": 5,
                    "mana_cost": 25,
                    "base_damage": 1.1,
                    "requirements": {"интеллект": 15, "удача": 10},
                    "effects": {"chain_damage": 0.1}  # +10% урона по цепочке
                }
            }
        },
        "вор": {
            "name": "🗡 Путь Вора",
            "color": "#888888",
            "skills": {
                "удар_в_спину": {
                    "name": "Удар в спину",
                    "description": "Критический удар, игнорирует броню",
                    "max_level": 5,
                    "cooldown": 3,
                    "mana_cost": 5,
                    "base_damage": 2.0,
                    "requirements": {"ловкость": 12},
                    "effects": {"crit_damage": 0.1}  # +10% крит урона
                },
                "ядовитый_клинок": {
                    "name": "Ядовитый клинок",
                    "description": "Отравляет врага",
                    "max_level": 5,
                    "cooldown": 2,
                    "mana_cost": 8,
                    "base_damage": 1.0,
                    "requirements": {"ловкость": 10, "удача": 10},
                    "effects": {"poison_damage": 2}  # +2 урона ядом за уровень
                },
                "уворот": {
                    "name": "Уворот",
                    "description": "Уклонение от атаки",
                    "max_level": 3,
                    "cooldown": 2,
                    "mana_cost": 0,
                    "requirements": {"ловкость": 14},
                    "effects": {"dodge": 0.05}  # +5% уклонения за уровень
                },
                "незаметность": {
                    "name": "Незаметность",
                    "description": "Враг не видит тебя 1 ход",
                    "max_level": 3,
                    "cooldown": 6,
                    "mana_cost": 10,
                    "requirements": {"ловкость": 12, "удача": 12},
                    "effects": {"stealth_turns": 1}  # +1 ход скрытности
                },
                "воровство": {
                    "name": "Воровство",
                    "description": "Крадет деньги у врага",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 5,
                    "requirements": {"ловкость": 10, "удача": 15},
                    "effects": {"steal_mult": 0.5}  # +50% украденного
                }
            }
        },
        "универсальные": {
            "name": "✨ Общие навыки",
            "color": "#ffd700",
            "skills": {
                "выносливость": {
                    "name": "Выносливость",
                    "description": "Увеличивает максимальное здоровье",
                    "max_level": 10,
                    "passive": True,
                    "effects": {"health_bonus": 10}  # +10 здоровья за уровень
                },
                "концентрация": {
                    "name": "Концентрация",
                    "description": "Увеличивает максимальную ману",
                    "max_level": 10,
                    "passive": True,
                    "requirements": {"мудрость": 8},
                    "effects": {"mana_bonus": 5}  # +5 маны за уровень
                },
                "удача": {
                    "name": "Удача",
                    "description": "Шанс найти редкие предметы",
                    "max_level": 5,
                    "passive": True,
                    "effects": {"luck_bonus": 2}  # +2 удачи за уровень
                },
                "регенерация": {
                    "name": "Регенерация",
                    "description": "Восстанавливает здоровье каждый ход",
                    "max_level": 5,
                    "passive": True,
                    "requirements": {"выносливость": 10},
                    "effects": {"regen": 2}  # +2 регенерации за уровень
                }
            }
        }
    }
    
    def __init__(self, player):
        self.player = player
        self.skills = player.get("skills", {})
        self.skill_points = player.get("skill_points", 0)
        self.class_type = self.determine_class()
        
    def determine_class(self) -> str:
        """Определение класса по характеристикам"""
        stats = self.player["stats"]
        
        if stats["сила"] > stats["интеллект"] and stats["сила"] > stats["ловкость"]:
            return "воин"
        elif stats["интеллект"] > stats["сила"] and stats["интеллект"] > stats["ловкость"]:
            return "маг"
        elif stats["ловкость"] > stats["сила"] and stats["ловкость"] > stats["интеллект"]:
            return "вор"
        else:
            return "универсал"
    
    def get_available_skills(self) -> List[Dict]:
        """Получение доступных для изучения навыков"""
        available = []
        
        # Навыки класса
        if self.class_type in self.SKILL_TREES:
            for skill_id, skill in self.SKILL_TREES[self.class_type]["skills"].items():
                if self.can_learn_skill(skill_id):
                    available.append({
                        "id": skill_id,
                        "tree": self.class_type,
                        **skill
                    })
        
        # Универсальные навыки
        for skill_id, skill in self.SKILL_TREES["универсальные"]["skills"].items():
            if self.can_learn_skill(skill_id):
                available.append({
                    "id": skill_id,
                    "tree": "универсальные",
                    **skill
                })
        
        return available
    
    def can_learn_skill(self, skill_id: str) -> bool:
        """Проверка, можно ли изучить навык"""
        # Ищем навык во всех деревьях
        skill_data = None
        for tree in self.SKILL_TREES.values():
            if skill_id in tree.get("skills", {}):
                skill_data = tree["skills"][skill_id]
                break
        
        if not skill_data:
            return False
        
        # Проверка требований
        if "requirements" in skill_data:
            for stat, req in skill_data["requirements"].items():
                if self.player["stats"].get(stat, 0) < req:
                    return False
        
        # Проверка текущего уровня
        current_level = self.skills.get(skill_id, 0)
        if current_level >= skill_data["max_level"]:
            return False
        
        return True
    
    def learn_skill(self, skill_id: str) -> Dict:
        """Изучение навыка"""
        result = {
            "success": False,
            "message": "",
            "skill": None
        }
        
        if self.skill_points <= 0:
            result["message"] = "❌ Нет очков навыков!"
            return result
        
        if not self.can_learn_skill(skill_id):
            result["message"] = "❌ Нельзя изучить этот навык!"
            return result
        
        # Ищем навык
        for tree in self.SKILL_TREES.values():
            if skill_id in tree.get("skills", {}):
                skill_data = tree["skills"][skill_id]
                break
        else:
            result["message"] = "❌ Навык не найден!"
            return result
        
        # Повышаем уровень
        current_level = self.skills.get(skill_id, 0)
        self.skills[skill_id] = current_level + 1
        self.skill_points -= 1
        
        # Применяем пассивные эффекты
        if skill_data.get("passive", False):
            self.apply_passive_effect(skill_id, skill_data)
        
        result["success"] = True
        result["message"] = f"✅ Изучен навык: {skill_data['name']} ур. {self.skills[skill_id]}"
        result["skill"] = {
            "id": skill_id,
            "name": skill_data["name"],
            "level": self.skills[skill_id],
            "max_level": skill_data["max_level"],
            "description": skill_data["description"]
        }
        
        return result
    
    def apply_passive_effect(self, skill_id: str, skill_data: Dict):
        """Применение пассивного эффекта"""
        effects = skill_data.get("effects", {})
        
        for effect, value in effects.items():
            if effect == "health_bonus":
                self.player["max_health"] += value
                self.player["health"] += value
            elif effect == "mana_bonus":
                self.player["max_mana"] += value
                self.player["mana"] += value
            elif effect == "luck_bonus":
                self.player["stats"]["удача"] += value
            elif effect == "regen":
                if "regen" not in self.player:
                    self.player["regen"] = 0
                self.player["regen"] += value
    
    def get_skill_info(self, skill_id: str) -> Optional[Dict]:
        """Получение информации о навыке"""
        for tree in self.SKILL_TREES.values():
            if skill_id in tree.get("skills", {}):
                skill_data = tree["skills"][skill_id].copy()
                skill_data["current_level"] = self.skills.get(skill_id, 0)
                skill_data["tree_name"] = tree["name"]
                skill_data["tree_color"] = tree["color"]
                return skill_data
        return None
    
    def get_damage_bonus(self, skill_id: str) -> float:
        """Бонус к урону от навыка"""
        skill_data = self.get_skill_info(skill_id)
        if not skill_data:
            return 1.0
        
        level = self.skills.get(skill_id, 0)
        base = skill_data.get("base_damage", 1.0)
        effects = skill_data.get("effects", {})
        
        bonus = 1.0
        for effect, value in effects.items():
            if "damage" in effect:
                bonus += value * level
        
        return base * bonus
    
    def get_heal_bonus(self, skill_id: str) -> float:
        """Бонус к лечению от навыка"""
        skill_data = self.get_skill_info(skill_id)
        if not skill_data:
            return 1.0
        
        level = self.skills.get(skill_id, 0)
        base = skill_data.get("base_heal", 1.0)
        effects = skill_data.get("effects", {})
        
        bonus = 1.0
        for effect, value in effects.items():
            if "heal" in effect:
                bonus += value * level / 100
        
        return base * bonus
    
    def get_cooldown(self, skill_id: str) -> int:
        """Получение кулдауна навыка"""
        skill_data = self.get_skill_info(skill_id)
        if not skill_data:
            return 0
        
        return skill_data.get("cooldown", 1)
    
    def get_mana_cost(self, skill_id: str) -> int:
        """Получение стоимости маны"""
        skill_data = self.get_skill_info(skill_id)
        if not skill_data:
            return 0
        
        return skill_data.get("mana_cost", 0)
    
    def to_dict(self) -> Dict:
        """Сохранение в словарь"""
        return {
            "skills": self.skills,
            "skill_points": self.skill_points,
            "class_type": self.class_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict, player) -> 'SkillSystem':
        """Загрузка из словаря"""
        system = cls(player)
        system.skills = data.get("skills", {})
        system.skill_points = data.get("skill_points", 0)
        system.class_type = data.get("class_type", system.determine_class())
        return system