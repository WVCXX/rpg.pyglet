import random
from typing import Dict, List, Optional
from entities.enemy import Enemy, Boss
from systems.combat_system import CombatSystem


class DangerSystem:
    """Система опасных локаций"""
    
    DANGER_ZONES = {
        "лес": {
            "name": "Темный лес",
            "danger_level": 3,
            "enemies": ["волк", "медведь", "кабан", "леший"],
            "boss_chance": 0.05,
            "boss": "лесной_царь",
            "min_level": 1
        },
        "кладбище": {
            "name": "Старое кладбище",
            "danger_level": 4,
            "enemies": ["скелет", "зомби", "призрак", "упырь"],
            "boss_chance": 0.08,
            "boss": "лих",
            "min_level": 2
        },
        "подземелье": {
            "name": "Темные подземелья",
            "danger_level": 5,
            "enemies": ["гоблин", "тролль", "паук", "крыса"],
            "boss_chance": 0.1,
            "boss": "огр",
            "min_level": 3
        },
        "пещеры": {
            "name": "Глубокие пещеры",
            "danger_level": 4,
            "enemies": ["медведь_пещерный", "троглодит", "летучая_мышь"],
            "boss_chance": 0.07,
            "boss": "каменный_голем",
            "min_level": 2
        },
        "руины": {
            "name": "Древние руины",
            "danger_level": 5,
            "enemies": ["мумия", "призрак", "скорпион"],
            "boss_chance": 0.12,
            "boss": "древний_страж",
            "min_level": 3
        },
        "трущобы": {
            "name": "Гнилые трущобы",
            "danger_level": 2,
            "enemies": ["вор", "бандит", "пьяница"],
            "boss_chance": 0.03,
            "boss": "главарь_банды",
            "min_level": 1
        },
        "порт": {
            "name": "Морской порт",
            "danger_level": 2,
            "enemies": ["пират", "контрабандист", "моряк"],
            "boss_chance": 0.04,
            "boss": "капитан",
            "min_level": 1
        },
        "таверна": {
            "name": "Таверна",
            "danger_level": 1,
            "enemies": ["пьяный_драчун"],
            "boss_chance": 0.01,
            "min_level": 1
        }
    }
    
    ENEMY_TEMPLATES = {
        "волк": {"type": "зверь", "level": 1, "health": 40, "damage": 8, "exp": 25, "gold": 5},
        "медведь": {"type": "зверь", "level": 3, "health": 100, "damage": 15, "exp": 60, "gold": 15},
        "кабан": {"type": "зверь", "level": 2, "health": 60, "damage": 10, "exp": 35, "gold": 8},
        "леший": {"type": "дух", "level": 4, "health": 80, "damage": 12, "exp": 70, "gold": 20},
        "скелет": {"type": "нежить", "level": 2, "health": 50, "damage": 9, "exp": 40, "gold": 10},
        "зомби": {"type": "нежить", "level": 3, "health": 70, "damage": 11, "exp": 55, "gold": 12},
        "призрак": {"type": "нежить", "level": 4, "health": 60, "damage": 14, "exp": 80, "gold": 25},
        "упырь": {"type": "нежить", "level": 3, "health": 65, "damage": 12, "exp": 60, "gold": 15},
        "гоблин": {"type": "гуманоид", "level": 1, "health": 35, "damage": 7, "exp": 20, "gold": 4},
        "тролль": {"type": "гуманоид", "level": 4, "health": 120, "damage": 18, "exp": 90, "gold": 30},
        "паук": {"type": "зверь", "level": 2, "health": 45, "damage": 9, "exp": 30, "gold": 6},
        "крыса": {"type": "зверь", "level": 1, "health": 20, "damage": 5, "exp": 15, "gold": 2},
        "вор": {"type": "человек", "level": 1, "health": 30, "damage": 6, "exp": 25, "gold": 10},
        "бандит": {"type": "человек", "level": 2, "health": 45, "damage": 9, "exp": 40, "gold": 15},
        "пьяница": {"type": "человек", "level": 1, "health": 25, "damage": 4, "exp": 15, "gold": 3},
        "пират": {"type": "человек", "level": 2, "health": 50, "damage": 10, "exp": 45, "gold": 20},
        "контрабандист": {"type": "человек", "level": 3, "health": 65, "damage": 12, "exp": 60, "gold": 25},
        "моряк": {"type": "человек", "level": 1, "health": 35, "damage": 7, "exp": 20, "gold": 5},
        "пьяный_драчун": {"type": "человек", "level": 1, "health": 30, "damage": 5, "exp": 15, "gold": 2}
    }
    
    BOSS_TEMPLATES = {
        "лесной_царь": {"type": "дух", "level": 5, "health": 200, "damage": 25, "exp": 200, "gold": 100},
        "лих": {"type": "нежить", "level": 6, "health": 250, "damage": 30, "exp": 250, "gold": 150},
        "огр": {"type": "гуманоид", "level": 5, "health": 300, "damage": 35, "exp": 220, "gold": 120},
        "каменный_голем": {"type": "голем", "level": 6, "health": 350, "damage": 40, "exp": 300, "gold": 200},
        "древний_страж": {"type": "нежить", "level": 7, "health": 400, "damage": 45, "exp": 350, "gold": 250},
        "главарь_банды": {"type": "человек", "level": 4, "health": 150, "damage": 20, "exp": 150, "gold": 80},
        "капитан": {"type": "человек", "level": 4, "health": 140, "damage": 18, "exp": 140, "gold": 70}
    }
    
    def __init__(self, game_window):
        self.game = game_window
        self.last_check = {}
        self.current_enemies = {}  # враги в текущей локации {location: [enemies]}
    
    def check_location(self, location: str) -> Optional[List[Enemy]]:
        """Проверка локации на опасность"""
        # Если в локации уже есть враги, возвращаем их
        if location in self.current_enemies and self.current_enemies[location]:
            # Проверяем, живы ли враги
            alive_enemies = [e for e in self.current_enemies[location] if e.is_alive]
            if alive_enemies:
                return alive_enemies
            else:
                # Удаляем мертвых врагов
                del self.current_enemies[location]
        
        # Если локация не опасная
        if location not in self.DANGER_ZONES:
            return None
        
        zone = self.DANGER_ZONES[location]
        
        # Проверка минимального уровня игрока
        player_level = self.game.game_state.player["level"]
        if player_level < zone.get("min_level", 1):
            return None
        
        # Проверка времени с последней проверки
        current_day = self.game.world.day
        if location in self.last_check:
            days_passed = current_day - self.last_check[location]
            if days_passed < 1:  # Враги появляются не чаще раза в день
                return None
        
        # Шанс встретить врагов
        time_mod = 2.0 if 20 <= self.game.world.hour or self.game.world.hour <= 6 else 1.0  # Ночью больше врагов
        luck_mod = 1.0 - (self.game.game_state.player["stats"]["удача"] * 0.02)  # Удача уменьшает шанс
        
        base_chance = zone["danger_level"] * 0.1  # 10% за уровень опасности
        actual_chance = base_chance * time_mod * luck_mod
        
        # Отладка
        print(f"Проверка локации {location}: шанс {actual_chance:.2f}")
        
        if random.random() < actual_chance:
            # Проверка на босса
            if "boss" in zone and random.random() < zone["boss_chance"]:
                enemies = [self.create_boss(zone["boss"], zone["danger_level"])]
                print(f"⚠️ СОЗДАН БОСС в {location}!")
            else:
                # Случайное количество врагов
                count = random.randint(1, 3)
                enemies = []
                for _ in range(count):
                    enemy_type = random.choice(zone["enemies"])
                    enemy = self.create_enemy(enemy_type)
                    # Уровень врага зависит от локации и игрока
                    enemy.level = max(1, player_level + random.randint(-1, 1))
                    enemies.append(enemy)
                
                print(f"⚠️ СОЗДАНО {count} ВРАГОВ в {location}!")
            
            self.last_check[location] = current_day
            self.current_enemies[location] = enemies
            return enemies
        
        return None
    
    def start_combat(self, enemies):
        """Начать бой с врагами"""
        from ui.combat_screen import CombatScreen
    
        combat = CombatSystem(self.game.game_state.player, enemies, [])
        combat_screen = CombatScreen(self.game.root, combat, self.game)
        combat_screen.show()

    def create_enemy(self, enemy_type: str) -> Enemy:
        """Создание врага"""
        template = self.ENEMY_TEMPLATES.get(enemy_type, self.ENEMY_TEMPLATES["волк"])
        
        enemy = Enemy(
            enemy_id=f"{enemy_type}_{random.randint(1000, 9999)}",
            name=enemy_type.capitalize(),
            enemy_type=template["type"],
            level=template["level"]
        )
        
        # Настройка характеристик
        enemy.health = template["health"]
        enemy.max_health = template["health"]
        enemy.damage = template["damage"]
        enemy.exp_reward = template["exp"]
        enemy.gold_reward = template["gold"]
        
        return enemy
    
    def create_boss(self, boss_type: str, level: int) -> Boss:
        """Создание босса"""
        template = self.BOSS_TEMPLATES.get(boss_type, self.BOSS_TEMPLATES["огр"])
        
        boss = Boss(
            enemy_id=f"boss_{boss_type}_{random.randint(100, 999)}",
            name=boss_type.replace('_', ' ').title(),
            boss_type=boss_type,
            level=level + 2
        )
        
        # Настройка характеристик босса
        boss.health = template["health"]
        boss.max_health = template["health"]
        boss.damage = template["damage"]
        boss.exp_reward = template["exp"]
        boss.gold_reward = template["gold"]
        
        return boss
    
    def clear_location(self, location: str):
        """Очистка локации от врагов (после боя)"""
        if location in self.current_enemies:
            del self.current_enemies[location]
    
    def get_location_status(self, location: str) -> Dict:
        """Получение статуса локации"""
        if location in self.current_enemies and self.current_enemies[location]:
            enemies = self.current_enemies[location]
            alive = [e for e in enemies if e.is_alive]
            return {
            "dangerous": True,
            "enemy_count": len(alive),
            "enemies": alive
        }

        if location in self.DANGER_ZONES:
            return {
            "dangerous": False,
            "type": "potential",
            "level": self.DANGER_ZONES[location]["danger_level"]
        }

        return {
            "dangerous": False,
            "type": "safe"
    }