import random
from typing import Dict, List, Optional

class Enemy:
    """Класс врага"""
    def __init__(self, enemy_id: str, name: str, enemy_type: str, level: int = 1):
        self.id = enemy_id
        self.name = name
        self.type = enemy_type
        self.level = level
        
        # базовые характеристики
        self.health = 50 + level * 10
        self.max_health = self.health
        self.stamina = 50 + level * 5
        self.mana = 0 if enemy_type != "маг" else 30 + level * 10
        
        self.stats = {
            "сила": 5 + level,
            "ловкость": 5 + level,
            "интеллект": 3 + level // 2,
            "мудрость": 3 + level // 2,
            "удача": 5
        }
        
        # боевые характеристики
        self.damage = 5 + level * 2
        self.armor = level
        self.initiative = random.randint(1, 10)
        self.critical_chance = 0.05 + level * 0.01
        self.dodge_chance = 0.05 + self.stats["ловкость"] * 0.005
        
        # награда
        self.exp_reward = 20 * level
        self.gold_reward = random.randint(5, 15) * level
        self.loot_table = self.generate_loot()
        
        # состояние
        self.is_alive = True
        self.agro_range = 10
        self.current_target = None
        self.special_abilities = self.get_abilities()
        self.resistances = self.get_resistances()
        self.weaknesses = self.get_weaknesses()
        
        # описание
        self.description = self.generate_description()
        self.lore = self.generate_lore()
    
    def generate_loot(self) -> List[str]:
        """Генерация лута с шансами"""
        loot = []
        
        # обычный лут (50% шанс)
        if random.random() < 0.5:
            common_items = [
                "зелье_здоровья", "зелье_маны", "бинты",
                "монета", "кость", "шкура"
            ]
            loot.append(random.choice(common_items))
        
        # редкий лут (20% шанс)
        if random.random() < 0.2:
            rare_items = [
                "стальной_меч", "кожаная_броня", "магическое_кольцо",
                "амулет", "редкая_трава", "свиток_заклинания"
            ]
            loot.append(random.choice(rare_items))
        
        # эпический лут (5% шанс)
        if random.random() < 0.05:
            epic_items = [
                "драконий_клык", "проклятый_клинок", "книга_мертвых",
                "золотой_идол", "эликсир_бессмертия"
            ]
            loot.append(random.choice(epic_items))
        # легендарный лут(1% шанс)
        if random.random() < 0.01:
            legendary_items = []
        
        return loot
    
    def get_abilities(self) -> Dict[str, Dict]:
        """Получение способностей в зависимости от типа"""
        abilities = {
            "человек": {
                "attack": {"damage": 1.0, "mana_cost": 0, "cooldown": 0},
                "block": {"damage_reduction": 0.5, "mana_cost": 0, "cooldown": 3}
            },
            "зверь": {
                "bite": {"damage": 1.3, "mana_cost": 0, "cooldown": 2},
                "claw": {"damage": 1.2, "mana_cost": 0, "cooldown": 1}
            },
            "нежить": {
                "life_steal": {"damage": 1.1, "heal": 0.5, "mana_cost": 5, "cooldown": 3},
                "curse": {"damage": 0.8, "debuff": "weakness", "mana_cost": 10, "cooldown": 4}
            },
            "демон": {
                "fire_ball": {"damage": 1.5, "mana_cost": 15, "cooldown": 3},
                "hell_fire": {"damage": 2.0, "mana_cost": 30, "cooldown": 5}
            },
            "дракон": {
                "fire_breath": {"damage": 2.5, "mana_cost": 20, "cooldown": 4},
                "tail_whip": {"damage": 1.8, "mana_cost": 0, "cooldown": 2}
            },
            "голем": {
                "stomp": {"damage": 1.4, "stun": True, "mana_cost": 0, "cooldown": 3},
                "rock_throw": {"damage": 1.6, "mana_cost": 0, "cooldown": 2}
            },
            "маг": {
                "magic_missile": {"damage": 1.2, "mana_cost": 5, "cooldown": 1},
                "frostbolt": {"damage": 1.3, "slow": True, "mana_cost": 10, "cooldown": 2}
            }
        }
        return abilities.get(self.type, abilities["человек"])
    
    def get_resistances(self) -> Dict[str, float]:
        """Получение сопротивлений"""
        resistances = {
            "огонь": 0.0,
            "холод": 0.0,
            "яд": 0.0,
            "магия": 0.0,
            "физический": 0.0
        }
        
        # сопротивления в зависимости от типа
        type_resists = {
            "дракон": {"огонь": 0.5, "магия": 0.3},
            "нежить": {"холод": 0.5, "яд": 1.0, "магия": -0.3},
            "демон": {"огонь": 0.5, "магия": 0.5},
            "голем": {"физический": 0.5, "магия": -0.5}
        }
        
        if self.type in type_resists:
            for resist, value in type_resists[self.type].items():
                resistances[resist] = value
        
        return resistances
    
    def get_weaknesses(self) -> Dict[str, float]:
        """Получение уязвимостей"""
        weaknesses = {}
        
        type_weak = {
            "нежить": {"огонь": 0.5, "святость": 1.0},
            "демон": {"святость": 0.5, "холод": 0.3},
            "дракон": {"холод": 0.3},
            "голем": {"дробящий": 0.5}
        }
        
        if self.type in type_weak:
            weaknesses.update(type_weak[self.type])
        
        return weaknesses
    
    def generate_description(self) -> str:
        """Генерация описания"""
        descriptions = {
            "человек": "Обычный человек, но опасный в бою",
            "зверь": "Дикий зверь с острыми когтями и клыками",
            "нежить": "Мертвец, поднятый темной магией",
            "демон": "Порождение бездны, несущее хаос",
            "дракон": "Древнее создание, извергающее огонь",
            "голем": "Ожившая статуя из камня",
            "маг": "Владеет тайнами магии"
        }
        return descriptions.get(self.type, "Таинственное существо")
    
    def generate_lore(self) -> str:
        """Генерация предыстории"""
        lores = {
            "человек": "Когда-то был обычным путником, но сошел с пути",
            "зверь": "Обитает в темных лесах и охотится на забредших",
            "нежить": "Проклят за свои грехи и обречен на вечные муки",
            "демон": "Призван из бездны безумным колдуном",
            "дракон": "Последний из своего рода, охраняющий сокровища",
            "голем": "Создан древними магами для охраны гробниц",
            "маг": "Изучал запретные знания и был наказан"
        }
        return lores.get(self.type, "История этого существа покрыта тайной")
    
    def take_damage(self, damage: int, damage_type: str = "физический") -> int:
        """Получение урона с учетом сопротивлений"""
        # сопротивление
        resist = self.resistances.get(damage_type, 0.0)
        damage = int(damage * (1 - resist))
        
        # уязвимость
        weakness = self.weaknesses.get(damage_type, 0.0)
        damage = int(damage * (1 + weakness))
        
        # минимальный урон
        damage = max(1, damage)
        
        self.health -= damage
        
        if self.health <= 0:
            self.is_alive = False
            self.health = 0
        
        return damage
    
    def attack(self, target) -> int:
        """Атака цели"""
        # проверка на промах
        if random.random() > self.accuracy:
            return 0
        
        # расчет урона
        damage = self.damage + random.randint(-2, 2)
        
        # критический удар
        if random.random() < self.critical_chance:
            damage *= 2
            print(f"⚡ КРИТИЧЕСКИЙ УДАР от {self.name}!")
        
        return target.take_damage(damage)
    
    def use_ability(self, ability_name: str, target) -> Dict:
        """Использование способности"""
        ability = self.special_abilities.get(ability_name, {})
        
        result = {
            "damage": 0,
            "heal": 0,
            "effects": [],
            "message": ""
        }
        
        # проверка маны
        mana_cost = ability.get("mana_cost", 0)
        if self.mana < mana_cost:
            return result
        
        self.mana -= mana_cost
        
        # урон
        damage_mult = ability.get("damage", 1.0)
        damage = int(self.damage * damage_mult)
        
        if damage > 0:
            actual_damage = target.take_damage(damage)
            result["damage"] = actual_damage
            result["message"] = f"{self.name} использует {ability_name} и наносит {actual_damage} урона!"
        
        # лечение
        heal_mult = ability.get("heal", 0)
        if heal_mult > 0:
            heal_amount = int(damage * heal_mult)
            self.health = min(self.max_health, self.health + heal_amount)
            result["heal"] = heal_amount
            result["message"] += f" И восстанавливает {heal_amount} здоровья!"
        
        # эффекты
        if ability.get("stun", False):
            result["effects"].append("stun")
        
        if ability.get("slow", False):
            result["effects"].append("slow")
        
        return result
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "level": self.level,
            "health": self.health,
            "max_health": self.max_health,
            "stamina": self.stamina,
            "mana": self.mana,
            "stats": self.stats,
            "damage": self.damage,
            "armor": self.armor,
            "is_alive": self.is_alive,
            "loot_table": self.loot_table,
            "exp_reward": self.exp_reward,
            "gold_reward": self.gold_reward,
            "description": self.description,
            "lore": self.lore
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Enemy':
        """Загрузка из словаря"""
        enemy = cls(data["id"], data["name"], data["type"], data["level"])
        enemy.health = data["health"]
        enemy.max_health = data["max_health"]
        enemy.stamina = data["stamina"]
        enemy.mana = data["mana"]
        enemy.stats = data["stats"]
        enemy.damage = data["damage"]
        enemy.armor = data["armor"]
        enemy.is_alive = data["is_alive"]
        enemy.loot_table = data["loot_table"]
        enemy.exp_reward = data["exp_reward"]
        enemy.gold_reward = data["gold_reward"]
        enemy.description = data.get("description", enemy.generate_description())
        enemy.lore = data.get("lore", enemy.generate_lore())
        return enemy


class Boss(Enemy):
    """Класс босса"""
    def __init__(self, enemy_id: str, name: str, boss_type: str, level: int = 10):
        super().__init__(enemy_id, name, boss_type, level)
        
        # боссы сильнее
        self.health *= 5
        self.max_health = self.health
        self.damage *= 3
        self.armor *= 2
        self.critical_chance *= 2
        self.dodge_chance *= 1.5
        
        # фазы боя
        self.current_phase = 1
        self.max_phases = 3
        self.phase_thresholds = [0.66, 0.33, 0.0]
        self.phase_abilities = self.generate_phase_abilities()
        
        # диалоги
        self.intro_dialogue = self.generate_intro()
        self.phase_dialogues = self.generate_phase_dialogues()
        self.death_dialogue = self.generate_death_dialogue()
        
        # уникальные механики
        self.arena_effects = self.generate_arena_effects()
        self.minions = []  # приспешники
        self.enrage_timer = 0
        self.enrage_threshold = 10  # ходов до берсерка
        
        # награда
        self.exp_reward *= 10
        self.gold_reward *= 20
        self.loot_table.extend(["трофей_босса", "легендарный_предмет"])
        self.unique_loot = self.generate_unique_loot()
    
    def generate_phase_abilities(self) -> Dict[int, List[str]]:
        """Генерация способностей по фазам"""
        phases = {}
        
        for phase in range(1, self.max_phases + 1):
            phase_abilities = []
            
            # базовые способности
            if phase >= 1:
                phase_abilities.extend(list(self.special_abilities.keys()))
            
            # новые способности с фазами
            if phase >= 2:
                phase_abilities.extend(["берсерк", "призыв_миньонов"])
            
            if phase >= 3:
                phase_abilities.extend(["ярость", "разрушение"])
            
            phases[phase] = phase_abilities
        
        return phases
    
    def generate_intro(self) -> str:
        """Генерация вступительной речи"""
        intros = [
            f"{self.name}: Ты посмел бросить мне вызов, смертный?",
            f"{self.name}: Еще одна жертва пришла...",
            f"{self.name}: Трепещи, ибо ты встретил свою смерть!",
            f"{self.name}: Наконец-то достойный противник!",
            f"{self.name}: Ты пожалеешь о том, что пришел сюда."
        ]
        return random.choice(intros)
    
    def generate_phase_dialogues(self) -> Dict[int, str]:
        """Генерация диалогов при смене фазы"""
        dialogues = {
            1: f"{self.name}: Это только начало!",
            2: f"{self.name}: Ты разозлил меня!",
            3: f"{self.name}: УМРИ!!!"
        }
        return dialogues
    
    def generate_death_dialogue(self) -> str:
        """Генерация предсмертной речи"""
        deaths = [
            f"{self.name}: Невозможно... я вернусь...",
            f"{self.name}: Проклятие...",
            f"{self.name}: Ты еще пожалеешь...",
            f"{self.name}: Это... не... конец..."
        ]
        return random.choice(deaths)
    
    def generate_arena_effects(self) -> List[str]:
        """Генерация эффектов арены"""
        effects = []
        possible_effects = ["огонь", "тьма", "яд", "святость", "холод"]
        
        for _ in range(random.randint(1, 3)):
            effects.append(random.choice(possible_effects))
        
        return effects
    
    def generate_unique_loot(self) -> List[str]:
        """Генерация уникального лута"""
        unique_items = [
            "корон","корона_властелина", "сердце_дракона", "клинок_тысячи_истин",
            "амулет_бессмертия", "книга_запретных_знаний", "глаз_демона"
        ]
        return random.sample(unique_items, random.randint(1, 3))
    
    def check_phase_change(self) -> bool:
        """Проверка смены фазы"""
        health_percent = self.health / self.max_health
        
        for phase, threshold in enumerate(self.phase_thresholds, 1):
            if health_percent <= threshold and self.current_phase < phase:
                self.current_phase = phase
                
                # усиление при смене фазы
                self.damage *= 1.2
                self.armor *= 1.1
                
                # призыв миньонов
                if phase >= 2:
                    self.summon_minions()
                
                return True
        return False
    
    def summon_minions(self):
        """Призыв приспешников"""
        minion_count = random.randint(2, 4)
        for i in range(minion_count):
            minion = Enemy(
                f"{self.id}_minion_{i}",
                f"Приспешник {self.name}",
                self.type,
                self.level - 2
            )
            self.minions.append(minion)
    
    def enrage_check(self, turn_count: int) -> bool:
        """Проверка берсерка"""
        if turn_count >= self.enrage_threshold and self.current_phase >= 2:
            self.damage *= 2
            self.enrage_timer = turn_count
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        data = super().to_dict()
        data.update({
            "current_phase": self.current_phase,
            "intro_dialogue": self.intro_dialogue,
            "death_dialogue": self.death_dialogue,
            "unique_loot": self.unique_loot,
            "arena_effects": self.arena_effects,
            "phase_dialogues": self.phase_dialogues
        })
        return data