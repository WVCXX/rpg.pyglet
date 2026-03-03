import random
from typing import Dict, List, Optional

class SkillSystem:
    """Улучшенная система навыков и прокачки"""
    
    SKILL_TREES = {
        "воин": {
            "name": "🌪 Путь Воина",
            "color": "#ff4444",
            "description": "Мастер ближнего боя, высокий урон и защита",
            "skills": {
                "сильный_удар": {
                    "name": "Сильный удар",
                    "description": "Мощная атака, наносящая 150% урона",
                    "max_level": 5,
                    "cooldown": 2,
                    "mana_cost": 5,
                    "base_damage": 1.5,
                    "requirements": {"сила": 10, "уровень": 2},
                    "effects": {"damage_mult": 0.1},  # +10% урона за уровень
                    "icon": "💪"
                },
                "кровавая_жажда": {
                    "name": "Кровавая жажда",
                    "description": "Восстанавливает 20% от нанесенного урона",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 10,
                    "base_damage": 1.2,
                    "requirements": {"сила": 12, "выносливость": 10, "уровень": 4},
                    "effects": {"lifesteal": 0.05},  # +5% вампиризма за уровень
                    "icon": "🩸"
                },
                "блок_щитом": {
                    "name": "Блок щитом",
                    "description": "Снижает получаемый урон на 50% на 2 хода",
                    "max_level": 3,
                    "cooldown": 3,
                    "mana_cost": 0,
                    "requirements": {"сила": 8, "выносливость": 12, "уровень": 3},
                    "effects": {"block": 0.1},  # +10% блокирования за уровень
                    "icon": "🛡️"
                },
                "ярость": {
                    "name": "Ярость",
                    "description": "Увеличивает урон на 30% на 3 хода",
                    "max_level": 3,
                    "cooldown": 5,
                    "mana_cost": 15,
                    "requirements": {"сила": 15, "удача": 8, "уровень": 5},
                    "effects": {"fury_damage": 0.1},  # +10% урона в ярости
                    "icon": "🔥"
                },
                "рассекающий_удар": {
                    "name": "Рассекающий удар",
                    "description": "Атакует всех врагов",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 20,
                    "base_damage": 0.8,
                    "requirements": {"сила": 14, "ловкость": 10, "уровень": 6},
                    "effects": {"aoe_damage": 0.1},  # +10% урона по площади
                    "icon": "⚔️"
                },
                "берсерк": {
                    "name": "Берсерк",
                    "description": "Чем меньше здоровья, тем больше урон",
                    "max_level": 3,
                    "passive": True,
                    "requirements": {"сила": 18, "выносливость": 15, "уровень": 8},
                    "effects": {"berserk_mult": 0.2},  # +20% урона при низком здоровье
                    "icon": "😤"
                }
            }
        },
        "маг": {
            "name": "🔮 Путь Мага",
            "color": "#4444ff",
            "description": "Повелитель магии, мощные заклинания",
            "skills": {
                "огненный_шар": {
                    "name": "Огненный шар",
                    "description": "Наносит магический урон и поджигает",
                    "max_level": 5,
                    "cooldown": 2,
                    "mana_cost": 15,
                    "base_damage": 1.4,
                    "requirements": {"интеллект": 12, "уровень": 2},
                    "effects": {"fire_damage": 0.1},  # +10% урона огнем
                    "icon": "🔥"
                },
                "ледяная_стрела": {
                    "name": "Ледяная стрела",
                    "description": "Замедляет врага",
                    "max_level": 5,
                    "cooldown": 1,
                    "mana_cost": 10,
                    "base_damage": 1.2,
                    "requirements": {"интеллект": 10, "уровень": 2},
                    "effects": {"slow": 0.1},  # +10% замедления
                    "icon": "❄️"
                },
                "магический_щит": {
                    "name": "Магический щит",
                    "description": "Поглощает урон",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 20,
                    "requirements": {"интеллект": 10, "мудрость": 12, "уровень": 4},
                    "effects": {"shield": 10},  # +10 поглощения за уровень
                    "icon": "🛡️"
                },
                "лечение": {
                    "name": "Лечение",
                    "description": "Восстанавливает здоровье",
                    "max_level": 5,
                    "cooldown": 3,
                    "mana_cost": 15,
                    "base_heal": 1.3,
                    "requirements": {"мудрость": 12, "уровень": 3},
                    "effects": {"heal": 5},  # +5 лечения за уровень
                    "icon": "💚"
                },
                "цепная_молния": {
                    "name": "Цепная молния",
                    "description": "Бьет по нескольким врагам",
                    "max_level": 3,
                    "cooldown": 5,
                    "mana_cost": 25,
                    "base_damage": 1.1,
                    "requirements": {"интеллект": 15, "удача": 10, "уровень": 6},
                    "effects": {"chain_damage": 0.1},  # +10% урона по цепочке
                    "icon": "⚡"
                },
                "телепорт": {
                    "name": "Телепорт",
                    "description": "Мгновенное перемещение",
                    "max_level": 2,
                    "cooldown": 10,
                    "mana_cost": 30,
                    "requirements": {"интеллект": 16, "мудрость": 14, "уровень": 7},
                    "effects": {"range": 50},  # +50 дальности
                    "icon": "🌀"
                }
            }
        },
        "вор": {
            "name": "🗡 Путь Вора",
            "color": "#888888",
            "description": "Мастер теней, критические удары",
            "skills": {
                "удар_в_спину": {
                    "name": "Удар в спину",
                    "description": "Критический удар, игнорирует броню",
                    "max_level": 5,
                    "cooldown": 3,
                    "mana_cost": 5,
                    "base_damage": 2.0,
                    "requirements": {"ловкость": 12, "уровень": 2},
                    "effects": {"crit_damage": 0.1},  # +10% крит урона
                    "icon": "🗡️"
                },
                "ядовитый_клинок": {
                    "name": "Ядовитый клинок",
                    "description": "Отравляет врага",
                    "max_level": 5,
                    "cooldown": 2,
                    "mana_cost": 8,
                    "base_damage": 1.0,
                    "requirements": {"ловкость": 10, "удача": 10, "уровень": 3},
                    "effects": {"poison_damage": 2},  # +2 урона ядом за уровень
                    "icon": "☠️"
                },
                "уворот": {
                    "name": "Уворот",
                    "description": "Уклонение от атаки",
                    "max_level": 3,
                    "cooldown": 2,
                    "mana_cost": 0,
                    "requirements": {"ловкость": 14, "уровень": 3},
                    "effects": {"dodge": 0.05},  # +5% уклонения за уровень
                    "icon": "💨"
                },
                "незаметность": {
                    "name": "Незаметность",
                    "description": "Враг не видит тебя 1 ход",
                    "max_level": 3,
                    "cooldown": 6,
                    "mana_cost": 10,
                    "requirements": {"ловкость": 12, "удача": 12, "уровень": 4},
                    "effects": {"stealth_turns": 1},  # +1 ход скрытности
                    "icon": "👻"
                },
                "воровство": {
                    "name": "Воровство",
                    "description": "Крадет деньги у врага",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 5,
                    "requirements": {"ловкость": 10, "удача": 15, "уровень": 5},
                    "effects": {"steal_mult": 0.5},  # +50% украденного
                    "icon": "💰"
                },
                "ловушки": {
                    "name": "Ловушки",
                    "description": "Устанавливает ловушки в бою",
                    "max_level": 3,
                    "cooldown": 4,
                    "mana_cost": 15,
                    "base_damage": 1.5,
                    "requirements": {"ловкость": 14, "интеллект": 10, "уровень": 6},
                    "effects": {"trap_damage": 10},  # +10 урона ловушек
                    "icon": "⚠️"
                }
            }
        },
        "жрец": {
            "name": "✨ Путь Жреца",
            "color": "#ffff00",
            "description": "Целитель и защитник",
            "skills": {
                "малое_лечение": {
                    "name": "Малое лечение",
                    "description": "Восстанавливает здоровье",
                    "max_level": 5,
                    "cooldown": 1,
                    "mana_cost": 10,
                    "base_heal": 1.2,
                    "requirements": {"мудрость": 10, "уровень": 1},
                    "effects": {"heal": 5},
                    "icon": "💚"
                },
                "благословение": {
                    "name": "Благословение",
                    "description": "Увеличивает характеристики союзника",
                    "max_level": 3,
                    "cooldown": 3,
                    "mana_cost": 20,
                    "requirements": {"мудрость": 12, "харизма": 10, "уровень": 3},
                    "effects": {"buff": 5},  # +5 к характеристикам
                    "icon": "✨"
                },
                "воскрешение": {
                    "name": "Воскрешение",
                    "description": "Возвращает союзника к жизни",
                    "max_level": 2,
                    "cooldown": 20,
                    "mana_cost": 50,
                    "requirements": {"мудрость": 16, "харизма": 14, "уровень": 6},
                    "effects": {"revive_hp": 30},  # 30% здоровья после воскрешения
                    "icon": "♻️"
                },
                "священный_огонь": {
                    "name": "Священный огонь",
                    "description": "Атака светом по нежити",
                    "max_level": 3,
                    "cooldown": 3,
                    "mana_cost": 25,
                    "base_damage": 1.8,
                    "requirements": {"мудрость": 14, "уровень": 4},
                    "effects": {"undead_bonus": 0.5},  # +50% урона по нежити
                    "icon": "🔥"
                }
            }
        },
        "универсальные": {
            "name": "✨ Общие навыки",
            "color": "#ffd700",
            "description": "Навыки, доступные всем",
            "skills": {
                "выносливость": {
                    "name": "Выносливость",
                    "description": "Увеличивает максимальное здоровье",
                    "max_level": 10,
                    "passive": True,
                    "requirements": {"уровень": 1},
                    "effects": {"health_bonus": 10},  # +10 здоровья за уровень
                    "icon": "❤️"
                },
                "концентрация": {
                    "name": "Концентрация",
                    "description": "Увеличивает максимальную ману",
                    "max_level": 10,
                    "passive": True,
                    "requirements": {"мудрость": 8, "уровень": 2},
                    "effects": {"mana_bonus": 5},  # +5 маны за уровень
                    "icon": "🔮"
                },
                "удача": {
                    "name": "Удача",
                    "description": "Шанс найти редкие предметы",
                    "max_level": 5,
                    "passive": True,
                    "requirements": {"уровень": 3},
                    "effects": {"luck_bonus": 2},  # +2 удачи за уровень
                    "icon": "🍀"
                },
                "регенерация": {
                    "name": "Регенерация",
                    "description": "Восстанавливает здоровье каждый ход",
                    "max_level": 5,
                    "passive": True,
                    "requirements": {"выносливость": 10, "уровень": 4},
                    "effects": {"regen": 2},  # +2 регенерации за уровень
                    "icon": "💚"
                },
                "медитация": {
                    "name": "Медитация",
                    "description": "Восстанавливает ману каждый ход",
                    "max_level": 5,
                    "passive": True,
                    "requirements": {"мудрость": 12, "уровень": 4},
                    "effects": {"mana_regen": 1},  # +1 маны за ход
                    "icon": "🧘"
                },
                "скорость": {
                    "name": "Скорость",
                    "description": "Увеличивает шанс первого хода в бою",
                    "max_level": 3,
                    "passive": True,
                    "requirements": {"ловкость": 10, "уровень": 3},
                    "effects": {"initiative": 5},  # +5 к инициативе
                    "icon": "⚡"
                }
            }
        }
    }
    
    def __init__(self, player):
        self.player = player
        self.skills = player.get("skills", {})
        self.skill_points = player.get("skill_points", 0)
        self.class_type = self.determine_class()
        
        # Прогресс изучения навыков
        self.skill_progress = player.get("skill_progress", {})
    
    def determine_class(self) -> str:
        """Определение класса по характеристикам"""
        stats = self.player["stats"]
        
        # Сложная логика определения класса
        if stats["сила"] > stats["интеллект"] and stats["сила"] > stats["ловкость"]:
            if stats["мудрость"] > 10:
                return "паладин"
            return "воин"
        elif stats["интеллект"] > stats["сила"] and stats["интеллект"] > stats["ловкость"]:
            if stats["мудрость"] > 12:
                return "жрец"
            return "маг"
        elif stats["ловкость"] > stats["сила"] and stats["ловкость"] > stats["интеллект"]:
            return "вор"
        else:
            # Гибридные классы
            if stats["сила"] >= 10 and stats["интеллект"] >= 10:
                return "паладин"
            elif stats["ловкость"] >= 10 and stats["интеллект"] >= 10:
                return "охотник"
            else:
                return "универсал"
    
    def get_available_skills(self) -> List[Dict]:
        """Получение доступных для изучения навыков"""
        available = []
        
        # Навыки основного класса
        if self.class_type in self.SKILL_TREES:
            for skill_id, skill in self.SKILL_TREES[self.class_type]["skills"].items():
                if self.can_learn_skill(skill_id):
                    skill_info = self.get_skill_info(skill_id)
                    if skill_info:
                        available.append(skill_info)
        
        # Универсальные навыки
        for skill_id, skill in self.SKILL_TREES["универсальные"]["skills"].items():
            if self.can_learn_skill(skill_id):
                skill_info = self.get_skill_info(skill_id)
                if skill_info:
                    available.append(skill_info)
        
        return available
    
    def can_learn_skill(self, skill_id: str) -> bool:
        """Проверка, можно ли изучить навык"""
        skill_data = self._find_skill(skill_id)
        if not skill_data:
            return False
        
        # Проверка уровня игрока
        if "уровень" in skill_data.get("requirements", {}):
            if self.player["level"] < skill_data["requirements"]["уровень"]:
                return False
        
        # Проверка характеристик
        if "requirements" in skill_data:
            for stat, req in skill_data["requirements"].items():
                if stat == "уровень":
                    continue
                if self.player["stats"].get(stat, 0) < req:
                    return False
        
        # Проверка текущего уровня навыка
        current_level = self.skills.get(skill_id, 0)
        if current_level >= skill_data["max_level"]:
            return False
        
        return True
    
    def _find_skill(self, skill_id: str) -> Optional[Dict]:
        """Поиск навыка по ID"""
        for tree in self.SKILL_TREES.values():
            if skill_id in tree.get("skills", {}):
                return tree["skills"][skill_id]
        return None
    
    def get_skill_info(self, skill_id: str) -> Optional[Dict]:
        """Получение информации о навыке"""
        for tree_name, tree in self.SKILL_TREES.items():
            if skill_id in tree.get("skills", {}):
                skill_data = tree["skills"][skill_id].copy()
                skill_data["id"] = skill_id
                skill_data["current_level"] = self.skills.get(skill_id, 0)
                skill_data["tree"] = tree_name
                skill_data["tree_name"] = tree["name"]
                skill_data["tree_color"] = tree["color"]
                skill_data["progress"] = self.skill_progress.get(skill_id, 0)
                return skill_data
        return None
    
    def learn_skill(self, skill_id: str) -> Dict:
        """Изучение навыка"""
        result = {
            "success": False,
            "message": "",
            "skill": None,
            "exp_gained": 0
        }
        
        if self.skill_points <= 0:
            result["message"] = "❌ Нет очков навыков!"
            return result
        
        if not self.can_learn_skill(skill_id):
            result["message"] = "❌ Нельзя изучить этот навык!"
            return result
        
        skill_data = self._find_skill(skill_id)
        if not skill_data:
            result["message"] = "❌ Навык не найден!"
            return result
        
        # Повышаем уровень
        current_level = self.skills.get(skill_id, 0)
        self.skills[skill_id] = current_level + 1
        self.skill_points -= 1
        
        # Добавляем прогресс
        if skill_id not in self.skill_progress:
            self.skill_progress[skill_id] = 0
        
        # Применяем пассивные эффекты
        if skill_data.get("passive", False):
            self.apply_passive_effect(skill_id, skill_data)
        
        # Добавляем опыт за изучение
        exp_gain = 50 * (current_level + 1)
        self.player["exp"] += exp_gain
        result["exp_gained"] = exp_gain
        
        result["success"] = True
        result["message"] = f"✅ Изучен навык: {skill_data['name']} ур. {self.skills[skill_id]}"
        result["skill"] = self.get_skill_info(skill_id)
        
        return result
    
    def apply_passive_effect(self, skill_id: str, skill_data: Dict):
        """Применение пассивного эффекта"""
        level = self.skills.get(skill_id, 0)
        effects = skill_data.get("effects", {})
        
        for effect, value in effects.items():
            total_value = value * level
            
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
            elif effect == "mana_regen":
                if "mana_regen" not in self.player:
                    self.player["mana_regen"] = 0
                self.player["mana_regen"] += value
            elif effect == "initiative":
                if "initiative" not in self.player:
                    self.player["initiative"] = 0
                self.player["initiative"] += value
    
    def add_skill_progress(self, skill_id: str, amount: int):
        """Добавление прогресса навыка"""
        if skill_id not in self.skill_progress:
            self.skill_progress[skill_id] = 0
        
        self.skill_progress[skill_id] += amount
        
        # Шанс получить очко навыка при достижении порога
        if self.skill_progress[skill_id] >= 100:
            self.skill_progress[skill_id] = 0
            self.skill_points += 1
            return True
        
        return False
    
    def get_damage_bonus(self, skill_id: str) -> float:
        """Бонус к урону от навыка"""
        skill_data = self._find_skill(skill_id)
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
        skill_data = self._find_skill(skill_id)
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
        skill_data = self._find_skill(skill_id)
        if not skill_data:
            return 0
        
        return skill_data.get("cooldown", 1)
    
    def get_mana_cost(self, skill_id: str) -> int:
        """Получение стоимости маны"""
        skill_data = self._find_skill(skill_id)
        if not skill_data:
            return 0
        
        base_cost = skill_data.get("mana_cost", 0)
        level = self.skills.get(skill_id, 0)
        
        # Стоимость маны может уменьшаться с уровнем
        if level > 0:
            reduction = min(base_cost, level * 2)
            return max(0, base_cost - reduction)
        
        return base_cost
    
    def get_skill_tree_info(self) -> Dict:
        """Получение информации о древе навыков"""
        info = {}
        
        for tree_name, tree in self.SKILL_TREES.items():
            tree_skills = []
            total_level = 0
            max_possible = 0
            
            for skill_id, skill in tree["skills"].items():
                current_level = self.skills.get(skill_id, 0)
                tree_skills.append({
                    "id": skill_id,
                    "name": skill["name"],
                    "icon": skill.get("icon", "📚"),
                    "current_level": current_level,
                    "max_level": skill["max_level"],
                    "learned": current_level > 0
                })
                total_level += current_level
                max_possible += skill["max_level"]
            
            info[tree_name] = {
                "name": tree["name"],
                "color": tree["color"],
                "description": tree.get("description", ""),
                "skills": tree_skills,
                "progress": (total_level / max_possible * 100) if max_possible > 0 else 0
            }
        
        return info
    
    def to_dict(self) -> Dict:
        """Сохранение в словарь"""
        return {
            "skills": self.skills,
            "skill_points": self.skill_points,
            "class_type": self.class_type,
            "skill_progress": self.skill_progress
        }
    
    @classmethod
    def from_dict(cls, data: Dict, player) -> 'SkillSystem':
        """Загрузка из словаря"""
        system = cls(player)
        system.skills = data.get("skills", {})
        system.skill_points = data.get("skill_points", 0)
        system.class_type = data.get("class_type", system.determine_class())
        system.skill_progress = data.get("skill_progress", {})
        return system