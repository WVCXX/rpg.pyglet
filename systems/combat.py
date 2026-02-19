import random

class CombatSystem:
    """Боевая система"""
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies  # список врагов
        self.combat_log = []
        self.turn_order = []
        self.current_turn_index = 0
        self.combat_active = True
        self.turn_count = 0
        
        self.init_combat()
    
    def init_combat(self):
        """Инициализация боя"""
        # Определяем порядок ходов (игрок + все враги)
        all_combatants = [("player", self.player)] + [(f"enemy_{i}", e) for i, e in enumerate(self.enemies)]
        
        # Сортируем по инициативе
        self.turn_order = sorted(all_combatants, 
                                key=lambda x: x[1].stats["dexterity"] + random.randint(1, 20), 
                                reverse=True)
        
        self.add_to_log("⚔ Начинается бой!")
        self.add_to_log(f"Порядок ходов: {', '.join([t[0] for t in self.turn_order])}")
    
    def add_to_log(self, message):
        """Добавление в лог боя"""
        self.combat_log.append(message)
        print(f"[COMBAT] {message}")
    
    def player_turn(self, action, target_index=0):
        """Ход игрока"""
        if not self.combat_active:
            return False
        
        if target_index >= len(self.enemies):
            self.add_to_log("Нет такой цели!")
            return False
        
        target = self.enemies[target_index] if self.enemies else None
        
        if action == "attack":
            if target:
                damage = self.player_attack(target)
                self.add_to_log(f"⚔ Ты атакуешь {target.name} и наносишь {damage} урона!")
                
                if not target.is_alive:
                    self.add_to_log(f"💀 {target.name} повержен!")
                    self.enemies.remove(target)
            else:
                self.add_to_log("Нет цели для атаки!")
        
        elif action == "defend":
            self.player_defend()
            self.add_to_log("🛡 Ты принимаешь защитную стойку!")
        
        elif action == "use_item":
            self.add_to_log("📦 Использовать предмет")
            # TODO: реализовать
        
        elif action == "flee":
            if self.try_flee():
                self.add_to_log("🏃 Ты сбежал с поля боя!")
                self.combat_active = False
                return True
            else:
                self.add_to_log("❌ Не удалось сбежать!")
        
        # Проверка конца боя
        self.check_combat_end()
        
        # Следующий ход
        if self.combat_active:
            self.next_turn()
        return True
    
    def enemy_turn(self, enemy_data):
        """Ход врага"""
        if not self.combat_active:
            return
        
        enemy = enemy_data[1]
        
        # Выбор действия
        if enemy.special_abilities and random.random() < 0.3:
            action = random.choice(enemy.special_abilities)
            damage = enemy.use_ability(action, self.player)
            self.add_to_log(f"🔥 {enemy.name} использует {action} и наносит {damage} урона!")
        else:
            damage = enemy.attack(self.player)
            self.add_to_log(f"👊 {enemy.name} атакует и наносит {damage} урона!")
        
        # Проверка смерти игрока
        if self.player.health <= 0:
            self.add_to_log("💀 Ты повержен...")
            self.combat_active = False
    
    def next_turn(self):
        """Следующий ход"""
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        self.turn_count += 1
        
        current = self.turn_order[self.current_turn_index]
        
        if current[0] == "player":
            return "player_turn"
        else:
            # Ход врага
            self.enemy_turn(current)
            return "enemy_turn"
    
    def player_attack(self, target):
        """Атака игрока"""
        if not target:
            return 0
        
        # Расчет урона
        base_damage = self.player.get_damage()
        damage_variation = random.randint(-3, 3)
        damage = base_damage + damage_variation
        
        # Критический удар
        if random.random() < self.player.stats["luck"] / 100:
            damage *= 2
            self.add_to_log("⚡ КРИТИЧЕСКИЙ УДАР!")
        
        return target.take_damage(damage)
    
    def player_defend(self):
        """Защита игрока"""
        self.player.armor_bonus = 10
    
    def try_flee(self):
        """Попытка побега"""
        chance = 0.3 + self.player.stats["dexterity"] * 0.02
        return random.random() < chance
    
    def check_combat_end(self):
        """Проверка конца боя"""
        if not self.enemies:
            self.add_to_log("🎉 Победа! Все враги повержены.")
            self.combat_active = False
            self.give_rewards()
            return True
        
        if self.player.health <= 0:
            self.add_to_log("💔 Поражение...")
            self.combat_active = False
            return True
        
        return False
    
    def give_rewards(self):
        """Выдача наград"""
        total_exp = sum(e.exp_reward for e in self.enemies)
        total_gold = sum(e.gold_reward for e in self.enemies)
        
        self.player.exp += total_exp
        self.player.money += total_gold
        
        # Лут
        for enemy in self.enemies:
            for item in enemy.loot_table:
                if random.random() < 0.7:  # 70% шанс получить лут
                    category = "misc"
                    if "potion" in item:
                        category = "potions"
                    elif "sword" in item or "weapon" in item:
                        category = "weapons"
                    elif "armor" in item:
                        category = "armor"
                    
                    self.player.add_item(category, item)
                    self.add_to_log(f"📦 Ты нашел: {item}")
        
        self.add_to_log(f"✨ Получено опыта: {total_exp}")
        self.add_to_log(f"💰 Получено золота: {total_gold}")
        
        # Проверка уровня
        self.check_level_up()
    
    def check_level_up(self):
        """Проверка повышения уровня"""
        exp_needed = self.player.level * 100
        
        if self.player.exp >= exp_needed:
            self.player.level += 1
            self.player.exp -= exp_needed
            self.player.max_health += 10
            self.player.health = self.player.max_health
            self.player.stats["strength"] += 1
            self.player.stats["dexterity"] += 1
            
            self.add_to_log(f"⬆ УРОВЕНЬ ПОВЫШЕН! Теперь ты {self.player.level} уровня!")
            self.add_to_log("❤ Здоровье +10, 💪 сила +1, 🏃 ловкость +1")