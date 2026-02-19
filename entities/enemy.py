import random

class Enemy:
    """Класс врага"""
    def __init__(self, enemy_id, name, enemy_type, level=1):
        self.id = enemy_id
        self.name = name
        self.type = enemy_type 
        self.level = level
        
        # Характеристики
        self.health = 50 + level * 10
        self.max_health = self.health
        self.stamina = 50 + level * 5
        self.mana = 0
        
        self.stats = {
            "strength": 5 + level,
            "dexterity": 5 + level,
            "intelligence": 3 + level // 2,
            "wisdom": 3 + level // 2,
            "luck": 5
        }
        
        # Бой
        self.damage = 5 + level * 2
        self.armor = level
        self.initiative = random.randint(1, 10)
        
        # Награда
        self.exp_reward = 20 * level
        self.gold_reward = random.randint(5, 15) * level
        self.loot_table = self.generate_loot()
        
        # Состояние
        self.is_alive = True
        self.agro_range = 10
        self.current_target = None
        self.special_abilities = self.get_abilities()
    
    def generate_loot(self):
        """Генерация лута"""
        loot = []
        
        # Шанс на обычный лут
        if random.random() < 0.5:
            loot.append("health_potion")
        
        # Шанс на редкий лут
        if random.random() < 0.2:
            loot.append(random.choice(["steel_sword", "leather_armor", "magic_ring"]))
        
        return loot
    
    def get_abilities(self):
        """Получение способностей в зависимости от типа"""
        abilities = {
            "humanoid": ["attack"],
            "beast": ["bite"],
            "undead": ["life_steal"],
            "demon": ["fire_ball"],
            "dragon": ["fire_breath"],
            "golem": ["stomp"]
        }
        
        return abilities.get(self.type, ["attack"])
    
    def take_damage(self, damage):
        """Получение урона"""
        actual_damage = max(1, damage - self.armor)
        self.health -= actual_damage
        
        if self.health <= 0:
            self.is_alive = False
            self.health = 0
        
        return actual_damage
    
    def attack(self, target):
        """Атака цели"""
        hit_chance = 0.8 + self.stats["dexterity"] * 0.01
        if random.random() < hit_chance:
            damage = self.damage + random.randint(-2, 2)
            return target.take_damage(damage)
        return 0
    
    def use_ability(self, ability, target):
        """Использование способности"""
        if ability == "fire_ball":
            damage = self.damage * 2
            return target.take_damage(damage)
        elif ability == "bite":
            damage = self.damage + 5
            return target.take_damage(damage)
        elif ability == "life_steal":
            damage = self.damage
            actual = target.take_damage(damage)
            self.health = min(self.max_health, self.health + actual // 2)
            return actual
        else:
            return self.attack(target)
    
    def to_dict(self):
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
            "gold_reward": self.gold_reward
        }
    
    @classmethod
    def from_dict(cls, data):
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
        return enemy


class Boss(Enemy):
    """Класс босса"""
    def __init__(self, enemy_id, name, boss_type, level=10):
        super().__init__(enemy_id, name, boss_type, level)
        
        # Боссы сильнее
        self.health *= 5
        self.max_health = self.health
        self.damage *= 3
        self.armor *= 2
        
        # Фазы боя
        self.current_phase = 1
        self.phase_thresholds = [0.75, 0.5, 0.25]
        
        # Диалоги
        self.intro_dialogue = f"{name}: Ты посмел бросить мне вызов, смертный?"
        self.death_dialogue = f"{name}: Невозможно... я вернусь..."
        
        # Награда
        self.exp_reward *= 10
        self.gold_reward *= 20
        self.loot_table.append("boss_trophy")
        self.loot_table.append("legendary_item")
    
    def check_phase_change(self):
        """Проверка смены фазы"""
        health_percent = self.health / self.max_health
        
        for i, threshold in enumerate(self.phase_thresholds):
            if health_percent <= threshold and self.current_phase <= i + 1:
                self.current_phase = i + 2
                return True
        return False
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "current_phase": self.current_phase,
            "intro_dialogue": self.intro_dialogue,
            "death_dialogue": self.death_dialogue
        })
        return data