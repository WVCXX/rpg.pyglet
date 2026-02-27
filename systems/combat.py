import random
from typing import Dict, List, Optional, Tuple
from entities.enemy import Enemy
from entities.companion import Companion  

class CombatSystem:
    """Улучшенная боевая система"""
    def __init__(self, player, enemies: List[Enemy], companions: List[Companion] = None):
        self.player = player
        self.enemies = enemies
        self.companions = companions or []
        self.allies = [("player", player)] + [(f"companion_{i}", c) for i, c in enumerate(self.companions)]
        
        self.combat_log = []
        self.turn_order = []
        self.current_turn_index = 0
        self.combat_active = True
        self.turn_count = 0
        self.victory = False
        self.defeat = False
        
        # бонусы локации
        self.terrain_bonus = self.calculate_terrain_bonus()
        
        # инициализация
        self.init_combat()
    
    def calculate_terrain_bonus(self) -> Dict:
        """Расчет бонусов местности"""
        bonuses = {
            "player_damage": 1.0,
            "enemy_damage": 1.0,
            "player_defense": 1.0,
            "enemy_defense": 1.0,
            "dodge_chance": 0.0
        }
        
        # бонусы в зависимости от локации
        location = self.player.current_location if hasattr(self.player, 'current_location') else None
        
        terrain_bonuses = {
            "лес": {"player_damage": 0.9, "dodge_chance": 0.1},
            "горы": {"enemy_damage": 0.9, "player_defense": 1.1},
            "болото": {"player_damage": 0.8, "enemy_damage": 0.8},
            "подземелье": {"enemy_damage": 1.1, "player_defense": 0.9},
            "храм": {"player_damage": 1.1, "enemy_damage": 0.9}
        }
        
        if location in terrain_bonuses:
            bonuses.update(terrain_bonuses[location])
        
        return bonuses
    
    def init_combat(self):
        """Инициализация боя"""
        # все участники
        all_combatants = self.allies + [(f"enemy_{i}", e) for i, e in enumerate(self.enemies)]
        
        # сортировка по инициативе
        self.turn_order = sorted(all_combatants,
                                key=lambda x: self.calculate_initiative(x[1]),
                                reverse=True)
        
        self.add_to_log("⚔ НАЧАЛО БОЯ!")
        self.add_to_log(f"Противников: {len(self.enemies)}")
        if self.companions:
            self.add_to_log(f"Союзников: {len(self.companions)}")
        self.add_to_log(f"Порядок ходов: {', '.join([t[0] for t in self.turn_order])}")
    
    def calculate_initiative(self, combatant) -> int:
        """Расчет инициативы"""
        base = 10
        if hasattr(combatant, 'stats'):
            base += combatant.stats.get("ловкость", 0) * 2
        base += random.randint(1, 20)
        return base
    
    def add_to_log(self, message: str):
        """Добавление в лог боя"""
        self.combat_log.append(message)
        print(f"[COMBAT] {message}")
    
    def player_turn(self, action: str, target_index: int = 0) -> Tuple[bool, Dict]:
        """Ход игрока"""
        result = {
            "success": False,
            "damage": 0,
            "message": "",
            "combat_log": []
        }
        
        if not self.combat_active:
            return False, result
        
        if target_index >= len(self.enemies):
            result["message"] = "Нет такой цели!"
            return False, result
        
        target = self.enemies[target_index] if self.enemies else None
        
        if action == "attack":
            if target:
                damage = self.player_attack(target)
                result["damage"] = damage
                result["message"] = f"⚔ Ты атакуешь {target.name} и наносишь {damage} урона!"
                result["success"] = True
                
                if not target.is_alive:
                    self.add_to_log(f"💀 {target.name} повержен!")
                    self.enemies.remove(target)
                    self.player.exp += target.exp_reward
                    self.player.money += target.gold_reward
            else:
                result["message"] = "Нет цели для атаки!"
        
        elif action == "defend":
            self.player_defend()
            result["message"] = "🛡 Ты принимаешь защитную стойку!"
            result["success"] = True
        
        elif action == "flee":
            if self.try_flee():
                self.add_to_log("🏃 Ты сбежал с поля боя!")
                self.combat_active = False
                result["message"] = "Ты успешно сбежал!"
                result["success"] = True
                return True, result
            else:
                result["message"] = "❌ Не удалось сбежать!"
                result["success"] = False
        
        # проверка конца боя
        self.check_combat_end()
        
        return True, result
    
    def player_attack(self, target: Enemy) -> int:
        """Атака игрока с учетом бонусов"""
        # базовый урон
        base_damage = self.player.get_damage()
        
        # бонус местности
        base_damage = int(base_damage * self.terrain_bonus["player_damage"])
        
        # вариация
        damage_variation = random.randint(-3, 3)
        damage = base_damage + damage_variation
        
        # критический удар
        if random.random() < self.player.stats["удача"] / 100:
            damage *= 2
            self.add_to_log("⚡ КРИТИЧЕСКИЙ УДАР!")
        
        # проверка на уклонение врага
        if hasattr(target, 'dodge_chance'):
            if random.random() < target.dodge_chance:
                self.add_to_log("💨 Враг уклонился!")
                return 0
        
        return target.take_damage(damage)
    
    def player_defend(self):
        """Защита игрока"""
        self.player.defense_bonus = 10 * self.terrain_bonus["player_defense"]
    
    def try_flee(self) -> bool:
        """Попытка побега"""
        chance = 0.3 + self.player.stats["ловкость"] * 0.02
        return random.random() < chance
    
    def enemy_turn(self, enemy_data: Tuple[str, Enemy]) -> Dict:
        """Ход врага"""
        result = {
            "damage": 0,
            "message": "",
            "effects": []
        }
        
        enemy = enemy_data[1]
        
        # цель (игрок или компаньон)
        target = self.select_target()
        
        if not target:
            return result
        
        # выбор действия
        if hasattr(enemy, 'special_abilities') and enemy.special_abilities and random.random() < 0.3:
            ability_name = random.choice(list(enemy.special_abilities.keys()))
            ability_result = enemy.use_ability(ability_name, target)
            result["damage"] = ability_result.get("damage", 0)
            result["message"] = ability_result.get("message", f"{enemy.name} использует {ability_name}!")
            result["effects"] = ability_result.get("effects", [])
        else:
            damage = enemy.attack(target)
            result["damage"] = damage
            result["message"] = f"👊 {enemy.name} атакует и наносит {damage} урона!"
        
        # проверка смерти цели
        if hasattr(target, 'health') and target.health <= 0:
            if target == self.player:
                self.add_to_log("💀 Ты повержен...")
                self.defeat = True
                self.combat_active = False
            elif target in self.companions:
                self.add_to_log(f"💔 {target.name} пал в бою!")
                self.companions.remove(target)
        
        return result
    
    def companion_turn(self, companion_data: Tuple[str, Companion]) -> Dict:
        """Ход компаньона"""
        companion = companion_data[1]
        
        # выбор цели (ближайший враг)
        target = self.enemies[0] if self.enemies else None
        
        if not target:
            return {"message": f"{companion.name} не находит цели"}
        
        return companion.in_combat_turn(target)
    
    def select_target(self):
        """Выбор цели для врага"""
        if self.companions and random.random() < 0.3:
            # 30% шанс атаковать компаньона
            return random.choice(self.companions)
        return self.player
    
    def next_turn(self) -> Tuple[str, Dict]:
        """Следующий ход"""
        if not self.combat_active:
            return "combat_end", {}
        
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        self.turn_count += 1
        
        current = self.turn_order[self.current_turn_index]
        result = {}
        
        if current[0] == "player":
            result = {"action": "player_turn"}
            return "player", result
        elif current[0].startswith("companion"):
            result = self.companion_turn(current)
            return "companion", result
        else:
            result = self.enemy_turn(current)
            return "enemy", result
    
    def check_combat_end(self) -> bool:
        """Проверка конца боя"""
        if not self.enemies:
            self.victory = True
            self.combat_active = False
            self.add_to_log("🎉 ПОБЕДА! Все враги повержены.")
            self.give_rewards()
            return True
        
        if self.player.health <= 0:
            self.defeat = True
            self.combat_active = False
            self.add_to_log("💔 ПОРАЖЕНИЕ...")
            return True
        
        return False
    
    def give_rewards(self):
        """Выдача наград"""
        total_exp = 0
        total_gold = 0
        
        for enemy in self.enemies:
            total_exp += enemy.exp_reward
            total_gold += enemy.gold_reward
            
            # лут
            for item in enemy.loot_table:
                if random.random() < 0.7:
                    category = self.get_item_category(item)
                    self.player.inventory.add_item(category, item, 1)
                    self.add_to_log(f"📦 Найден предмет: {item}")
        
        self.player.exp += total_exp
        self.player.money += total_gold
        
        self.add_to_log(f"✨ Получено опыта: {total_exp}")
        self.add_to_log(f"💰 Получено золота: {total_gold}")
        
        # опыт компаньонам
        for companion in self.companions:
            companion.exp += total_exp // 2
    
    def get_item_category(self, item: str) -> str:
        """Определение категории предмета"""
        if "зелье" in item or "эликсир" in item:
            return "potions"
        elif "меч" in item or "клинок" in item or "оружие" in item:
            return "weapons"
        elif "броня" in item or "латы" in item or "плащ" in item:
            return "armor"
        elif "книга" in item or "свиток" in item:
            return "books"
        elif "трава" in item or "ингредиент" in item:
            return "ingredients"
        elif "ключ" in item:
            return "keys"
        else:
            return "misc"
    
    def get_combat_status(self) -> Dict:
        """Получение статуса боя"""
        return {
            "active": self.combat_active,
            "turn": self.turn_count,
            "enemies": len(self.enemies),
            "allies": len(self.companions) + 1,
            "player_health": f"{self.player.health}/{self.player.max_health}",
            "log": self.combat_log[-5:]  # последние 5 сообщений
        }