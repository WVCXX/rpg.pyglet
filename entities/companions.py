from entities.npc import NPC
import random
from typing import Dict, List, Optional

class Companion(NPC):
    """Класс компаньона"""
    def __init__(self, npc_id: str, name: str, race: str, gender: str, 
                 profession: str, personality: str):
        super().__init__(npc_id, name, race, gender, profession, personality)
        
        self.loyalty = 50  # 0-100
        self.morale = 50   # 0-100
        self.combat_skill = random.randint(30, 70)
        self.specialization = self.generate_specialization()
        
        self.health = 80
        self.max_health = 80
        self.stamina = 80
        self.mana = 30 if profession == "маг" else 0
        
        self.stats = {
            "сила": 5 + self.combat_skill // 10,
            "ловкость": 5 + self.combat_skill // 10,
            "интеллект": 5 + self.combat_skill // 10,
            "мудрость": 5 + self.combat_skill // 10,
            "удача": 5
        }
        
        # боевое поведение
        self.combat_role = self.determine_role()
        self.abilities = self.generate_abilities()
        self.equipment = self.generate_equipment()
        
        # отношения
        self.friendship_level = 0
        self.personal_quest = None
        self.secrets = self.generate_secrets()
        
        # состояние
        self.is_following = False
        self.inventory = {}  
        self.money = random.randint(20, 200)
    
    def generate_specialization(self) -> str:
        """Генерация специализации"""
        specs = {
            "воин": ["танк", "дд", "берсерк"],
            "лучник": ["снайпер", "стрелок", "разведчик"],
            "маг": ["огонь", "лед", "тайны"],
            "жрец": ["лекарь", "защитник", "экзорцист"],
            "вор": ["разбойник", "ассасин", "ловкач"]
        }
        
        prof_specs = specs.get(self.profession, ["универсал"])
        return random.choice(prof_specs)
    
    def determine_role(self) -> str:
        """Определение роли в бою"""
        role_map = {
            "воин": "танк",
            "лучник": "дд",
            "маг": "дд",
            "жрец": "хил",
            "вор": "дд"
        }
        return role_map.get(self.profession, "универсал")
    
    def generate_abilities(self) -> Dict[str, Dict]:
        """Генерация способностей"""
        abilities = {}
        
        # способности в зависимости от роли
        if self.combat_role == "танк":
            abilities = {
                "провокация": {"cooldown": 3, "effect": "taunt"},
                "щит": {"cooldown": 2, "effect": "block"},
                "удар_щитом": {"damage": 1.2, "cooldown": 2}
            }
        elif self.combat_role == "дд":
            abilities = {
                "сильный_удар": {"damage": 1.5, "cooldown": 2},
                "быстрая_атака": {"damage": 0.8, "cooldown": 1},
                "критический_удар": {"damage": 2.0, "cooldown": 4}
            }
        elif self.combat_role == "хил":
            abilities = {
                "лечение": {"heal": 1.3, "cooldown": 2},
                "массовое_лечение": {"heal": 0.8, "cooldown": 4},
                "защита": {"effect": "shield", "cooldown": 3}
            }
        
        return abilities
    
    def generate_equipment(self) -> Dict[str, str]:
        """Генерация экипировки"""
        equipment = {}
        
        # оружие
        weapons = {
            "воин": "стальной_меч",
            "лучник": "длинный_лук",
            "маг": "посох_мага",
            "жрец": "священный_символ",
            "вор": "отравленный_клинок"
        }
        equipment["weapon"] = weapons.get(self.profession, "обычное_оружие")
        
        # броня
        armors = {
            "воин": "латы",
            "лучник": "кожаная_броня",
            "маг": "мантия",
            "жрец": "ряса",
            "вор": "темный_плащ"
        }
        equipment["armor"] = armors.get(self.profession, "обычная_одежда")
        
        # аксессуары
        accessories = ["кольцо", "амулет", "браслет"]
        equipment["accessory"] = random.choice(accessories)
        
        return equipment
    
    def generate_secrets(self) -> List[str]:
        """Генерация секретов компаньона"""
        secrets = [
            "Боится пауков",
            "Должен деньги опасным людям",
            "Ищет пропавшего брата",
            "На самом деле дворянин",
            "Совершил преступление в прошлом",
            "Влюблен в трактирщицу",
            "Знает древнее заклинание",
            "Хранит семейную реликвию"
        ]
        return random.sample(secrets, random.randint(1, 3))
    
    def increase_loyalty(self, amount: int) -> str:
        """Увеличение лояльности"""
        old_loyalty = self.loyalty
        self.loyalty = min(100, self.loyalty + amount)
        
        messages = []
        if self.loyalty >= 80 and old_loyalty < 80:
            messages.append(f"{self.name} готов умереть за тебя!")
        elif self.loyalty >= 50 and old_loyalty < 50:
            messages.append(f"{self.name} доверяет тебе")
        
        return "\n".join(messages)
    
    def decrease_loyalty(self, amount: int) -> str:
        """Уменьшение лояльности"""
        old_loyalty = self.loyalty
        self.loyalty = max(0, self.loyalty - amount)
        
        messages = []
        if self.loyalty <= 20 and old_loyalty > 20:
            messages.append(f"{self.name} разочарован в тебе")
        elif self.loyalty <= 0:
            messages.append(f"{self.name} покидает тебя!")
            self.is_following = False
        
        return "\n".join(messages)
    
    def change_morale(self, amount: int) -> str:
        """Изменение морали"""
        self.morale = max(0, min(100, self.morale + amount))
        
        if amount > 0:
            return f"{self.name} воодушевлен!"
        elif amount < 0:
            return f"{self.name} подавлен"
        return ""
    
    def in_combat_turn(self, enemy) -> Dict:
        """Действие в бою"""
        result = {
            "action": "",
            "damage": 0,
            "heal": 0,
            "message": ""
        }
        
        # выбор действия в зависимости от роли
        if self.combat_role == "хил" and self.health < self.max_health * 0.5:
            # лечение себя
            heal_amount = int(self.max_health * 0.2)
            self.health = min(self.max_health, self.health + heal_amount)
            result["action"] = "heal_self"
            result["heal"] = heal_amount
            result["message"] = f"{self.name} лечит себя на {heal_amount}"
        
        elif self.combat_role == "танк" and enemy.target != self:
            # провокация
            enemy.target = self
            result["action"] = "taunt"
            result["message"] = f"{self.name} провоцирует врага!"
        
        else:
            # атака
            damage = self.calculate_damage()
            actual_damage = enemy.take_damage(damage)
            result["action"] = "attack"
            result["damage"] = actual_damage
            result["message"] = f"{self.name} атакует и наносит {actual_damage} урона!"
        
        return result
    
    def calculate_damage(self) -> int:
        """Расчет урона"""
        base_damage = 5 + self.stats["сила"] * 2
        weapon_bonus = 3 if self.equipment.get("weapon") else 0
        skill_bonus = self.combat_skill // 10
        
        damage = base_damage + weapon_bonus + skill_bonus
        variation = random.randint(-3, 3)
        
        return max(1, damage + variation)
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        data = super().to_dict()
        data.update({
            "loyalty": self.loyalty,
            "morale": self.morale,
            "combat_skill": self.combat_skill,
            "specialization": self.specialization,
            "combat_role": self.combat_role,
            "abilities": self.abilities,
            "equipment": self.equipment,
            "friendship_level": self.friendship_level,
            "is_following": self.is_following,
            "secrets": self.secrets,
            "health": self.health,
            "max_health": self.max_health,
            "stamina": self.stamina,
            "mana": self.mana
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Companion':
        """Загрузка из словаря"""
        companion = cls(
            data["id"],
            data["name"],
            data["race"],
            data["gender"],
            data["profession"],
            data["personality"]
        )
        
        # загрузка дополнительных полей
        companion.loyalty = data.get("loyalty", 50)
        companion.morale = data.get("morale", 50)
        companion.combat_skill = data.get("combat_skill", 50)
        companion.specialization = data.get("specialization", companion.generate_specialization())  
        companion.combat_role = data.get("combat_role", companion.determine_role())
        companion.abilities = data.get("abilities", companion.abilities)
        companion.equipment = data.get("equipment", companion.generate_equipment())
        companion.friendship_level = data.get("friendship_level", 0)
        companion.is_following = data.get("is_following", False)
        companion.secrets = data.get("secrets", companion.secrets)
        companion.health = data.get("health", 80)
        companion.max_health = data.get("max_health", 80)
        companion.stamina = data.get("stamina", 80)
        companion.mana = data.get("mana", 30 if companion.profession == "маг" else 0)
        
        return companion