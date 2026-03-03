import random
from typing import Dict, List, Optional, Tuple
from entities.enemy import Enemy, Boss
from systems.skill_system import SkillSystem
from systems.animation_system import AnimationSystem
from systems.sound_system import SoundSystem

class CombatSystem:
    """Полноценная боевая система с анимациями и звуками"""
    
    def __init__(self, player, enemies: List[Enemy], companions: List = None, 
                 animation_system=None, sound_system=None):
        self.player = player
        self.enemies = enemies
        self.companions = companions or []
        
        # Системы
        self.skill_system = SkillSystem(player)
        self.anim = animation_system
        self.sound = sound_system
        
        # Состояние боя
        self.combat_log = []
        self.turn_order = []
        self.current_turn_index = 0
        self.combat_active = True
        self.turn_count = 0
        self.victory = False
        self.defeat = False
        
        # Эффекты
        self.active_effects = {
            "player": {},
            "enemies": {},
            "companions": {}
        }
        
        # Кулдауны
        self.cooldowns = {
            "player": {},
            "enemies": {},
            "companions": {}
        }
        
        # Инициализация боя
        self.init_combat()
        
        # Воспроизводим музыку боя
        if self.sound:
            self.sound.play_music("battle", loop=True)
    
    def init_combat(self):
        """Инициализация боя"""
        # Все участники
        all_combatants = [("player", self.player)]
        for i, comp in enumerate(self.companions):
            all_combatants.append((f"companion_{i}", comp))
        for i, enemy in enumerate(self.enemies):
            all_combatants.append((f"enemy_{i}", enemy))
        
        # Расчет инициативы с учетом навыков
        self.turn_order = sorted(
            all_combatants,
            key=lambda x: self.calculate_initiative(x[1]),
            reverse=True
        )
        
        self.add_to_log("⚔ НАЧАЛО БОЯ!")
        self.add_to_log(f"Противников: {len(self.enemies)}")
        if self.companions:
            self.add_to_log(f"Союзников: {len(self.companions)}")
        
        # Звук начала боя
        if self.sound:
            self.sound.play_sound("sword")
    
    def calculate_initiative(self, combatant) -> int:
        """Расчет инициативы"""
        if hasattr(combatant, 'stats'):
            base = 10 + combatant.stats.get("ловкость", 0) * 2
        else:
            base = 10 + combatant.get("stats", {}).get("ловкость", 0) * 2
        
        # Бонус от навыков
        if "initiative" in combatant:
            base += combatant["initiative"]
        
        return base + random.randint(1, 20)
    
    def add_to_log(self, message: str):
        """Добавление в лог"""
        self.combat_log.append(message)
        print(f"[COMBAT] {message}")
    
    def player_turn(self, action: str, target_index: int = 0, skill_id: str = None, x=None, y=None) -> Dict:
        """Ход игрока"""
        result = {
            "success": False,
            "damage": 0,
            "heal": 0,
            "message": "",
            "effects": [],
            "combat_log": []
        }
        
        if not self.combat_active or not self.enemies:
            return result
        
        if target_index >= len(self.enemies):
            result["message"] = "❌ Нет такой цели!"
            if self.sound:
                self.sound.play_error()
            return result
        
        target = self.enemies[target_index]
        
        # Выполнение действия
        if action == "attack":
            result = self.player_attack(target, x, y)
        elif action == "skill":
            if skill_id:
                result = self.player_use_skill(skill_id, target, x, y)
            else:
                result["message"] = "❌ Не выбрано умение!"
                if self.sound:
                    self.sound.play_error()
        elif action == "defend":
            result = self.player_defend()
        elif action == "flee":
            result = self.player_flee()
        
        # Проверка смерти цели
        if target and not target.is_alive:
            self.add_to_log(f"💀 {target.name} повержен!")
            self.enemies.remove(target)
            
            # Анимация смерти
            if self.anim and x and y:
                self.anim.explosion_animation(x, y, "#440000")
            
            # Звук смерти
            if self.sound:
                self.sound.play_death()
            
            # Награда
            self.player["exp"] += target.exp_reward
            self.player["money"] += target.gold_reward
            
            # Обновляем статистику
            if "врагов_убито" in self.player:
                self.player["врагов_убито"] += 1
            
            # Шанс на лут
            self.drop_loot(target)
        
        # Проверка конца боя
        self.check_combat_end()
        
        # Уменьшение кулдаунов
        self.reduce_cooldowns()
        
        # Применение регенерации
        self.apply_regen()
        
        result["success"] = True
        return result
    
    def player_attack(self, target: Enemy, x=None, y=None) -> Dict:
        """Обычная атака"""
        result = {
            "damage": 0,
            "message": "",
            "effects": []
        }
        
        # Базовый урон
        base_damage = 5 + self.player["stats"]["сила"] * 2
        
        # Бонус от оружия
        if self.player["inventory"].get_item_count("weapons", "ржавый_меч") > 0:
            base_damage += 3
        
        # Вариация
        damage = base_damage + random.randint(-2, 2)
        
        # Критический удар
        crit_chance = self.player["stats"]["удача"] / 100
        is_critical = random.random() < crit_chance
        
        if is_critical:
            damage *= 2
            self.add_to_log("⚡ КРИТИЧЕСКИЙ УДАР!")
            result["effects"].append("critical")
            
            # Звук крита
            if self.sound:
                self.sound.play_critical()
            
            # Анимация крита
            if self.anim and x and y:
                self.anim.floating_text(x, y-50, "КРИТ!", "#ff8800")
        else:
            # Звук атаки
            if self.sound:
                self.sound.play_attack()
        
        # Проверка на уклонение
        if hasattr(target, 'dodge_chance'):
            if random.random() < target.dodge_chance:
                result["message"] = f"💨 {target.name} уклонился!"
                
                # Анимация уклонения
                if self.anim and x and y:
                    self.anim.floating_text(x, y, "УКЛОН", "#88ff88")
                
                return result
        
        actual_damage = target.take_damage(damage)
        result["damage"] = actual_damage
        result["message"] = f"⚔ Ты атакуешь {target.name} и наносишь {actual_damage} урона!"
        
        # Анимация урона
        if self.anim and x and y:
            self.anim.damage_text(x, y, actual_damage, is_critical)
        
        self.add_to_log(result["message"])
        return result
    
    def player_use_skill(self, skill_id: str, target: Enemy, x=None, y=None) -> Dict:
        """Использование навыка"""
        result = {
            "damage": 0,
            "heal": 0,
            "message": "",
            "effects": []
        }
        
        # Проверка кулдауна
        if skill_id in self.cooldowns["player"]:
            result["message"] = f"⏳ Навык еще перезаряжается ({self.cooldowns['player'][skill_id]} ходов)"
            if self.sound:
                self.sound.play_error()
            return result
        
        # Получение информации о навыке
        skill_info = self.skill_system.get_skill_info(skill_id)
        if not skill_info:
            result["message"] = "❌ Навык не найден!"
            return result
        
        # Проверка маны
        mana_cost = skill_info.get("mana_cost", 0)
        if self.player["mana"] < mana_cost:
            result["message"] = f"❌ Недостаточно маны! Нужно {mana_cost}"
            if self.sound:
                self.sound.play_error()
            return result
        
        self.player["mana"] -= mana_cost
        
        # Анимация в зависимости от навыка
        if self.anim and x and y:
            if "огонь" in skill_info["name"].lower() or "fire" in skill_id:
                self.anim.fireball_animation(x, y)
                if self.sound:
                    self.sound.play_sound("fireball")
            elif "лед" in skill_info["name"].lower() or "ice" in skill_id:
                self.anim.magic_animation(x, y, "#88ccff", "ice")
                if self.sound:
                    self.sound.play_sound("magic")
            elif "лечение" in skill_info["name"].lower() or "heal" in skill_id:
                self.anim.heal_animation(x, y)
                if self.sound:
                    self.sound.play_heal()
            elif "щит" in skill_info["name"].lower() or "shield" in skill_id:
                self.anim.shield_animation(x, y)
                if self.sound:
                    self.sound.play_block()
            else:
                self.anim.magic_animation(x, y, skill_info.get("tree_color", "#4444ff"))
                if self.sound:
                    self.sound.play_sound("magic")
        
        # Применение эффектов навыка
        if "base_damage" in skill_info:
            # Атакующий навык
            damage_mult = self.skill_system.get_damage_bonus(skill_id)
            base_damage = 5 + self.player["stats"]["сила"] * 2
            damage = int(base_damage * damage_mult)
            
            actual_damage = target.take_damage(damage)
            result["damage"] = actual_damage
            result["message"] = f"✨ {skill_info['name']} наносит {actual_damage} урона!"
            
            # Анимация урона
            if self.anim and x and y:
                self.anim.damage_text(x, y, actual_damage)
            
            # Дополнительные эффекты
            if "fire_damage" in skill_info.get("effects", {}):
                result["effects"].append("burn")
                self.add_to_log(f"🔥 {target.name} горит!")
                if self.anim:
                    self.anim.floating_text(x, y, "ГОРИТ!", "#ff4400")
            
            if "slow" in skill_info.get("effects", {}):
                result["effects"].append("slow")
                self.add_to_log(f"❄️ {target.name} замедлен!")
            
            if "lifesteal" in skill_info.get("effects", {}):
                heal = int(actual_damage * 0.2)
                self.player["health"] = min(self.player["max_health"], self.player["health"] + heal)
                result["heal"] = heal
                self.add_to_log(f"❤️ Ты восстанавливаешь {heal} здоровья!")
                if self.anim:
                    self.anim.heal_text(x, y, heal)
        
        elif "base_heal" in skill_info:
            # Лечащий навык
            heal_mult = self.skill_system.get_heal_bonus(skill_id)
            heal = int(30 * heal_mult)
            
            self.player["health"] = min(self.player["max_health"], self.player["health"] + heal)
            result["heal"] = heal
            result["message"] = f"💚 {skill_info['name']} восстанавливает {heal} здоровья!"
            
            if self.anim:
                self.anim.heal_text(x, y, heal)
        
        # Установка кулдауна
        cooldown = skill_info.get("cooldown", 1)
        self.cooldowns["player"][skill_id] = cooldown
        
        # Добавляем прогресс навыка
        self.skill_system.add_skill_progress(skill_id, 10)
        
        self.add_to_log(result["message"])
        return result
    
    def player_defend(self) -> Dict:
        """Защита"""
        self.player["defense_bonus"] = 10
        self.active_effects["player"]["defending"] = 2  # Длится 2 хода
        
        result = {
            "damage": 0,
            "message": "🛡 Ты принимаешь защитную стойку! Получаемый урон снижен на 50%"
        }
        
        # Анимация щита
        if self.anim:
            self.anim.shield_animation(400, 300)
        
        # Звук блока
        if self.sound:
            self.sound.play_block()
        
        self.add_to_log(result["message"])
        return result
    
    def player_flee(self) -> Dict:
        """Попытка побега"""
        chance = 0.3 + self.player["stats"]["ловкость"] * 0.02
        
        if random.random() < chance:
            self.combat_active = False
            result = {
                "damage": 0,
                "message": "🏃 Ты успешно сбежал с поля боя!"
            }
            # Звук побега
            if self.sound:
                self.sound.play_sound("click")
        else:
            result = {
                "damage": 0,
                "message": "❌ Не удалось сбежать!"
            }
            if self.sound:
                self.sound.play_error()
        
        self.add_to_log(result["message"])
        return result
    
    def enemy_turn(self, enemy_data: Tuple[str, Enemy]) -> Dict:
        """Ход врага"""
        enemy = enemy_data[1]
        
        if not enemy.is_alive:
            return {"message": f"{enemy.name} мертв"}
        
        # Выбор цели
        target = self.select_target()
        
        # Получаем координаты для анимации (примерные)
        target_x = 400
        target_y = 300
        enemy_x = 100
        enemy_y = 100
        
        # Анимация атаки врага
        if self.anim:
            self.anim.attack_animation(enemy_x, enemy_y, target_x, target_y, "#ff0000")
        
        # Выбор действия
        action_result = {"damage": 0, "message": ""}
        
        if hasattr(enemy, 'special_abilities') and enemy.special_abilities and random.random() < 0.3:
            # Использование способности
            ability_name = random.choice(list(enemy.special_abilities.keys()))
            ability_result = enemy.use_ability(ability_name, target)
            action_result["damage"] = ability_result.get("damage", 0)
            action_result["message"] = ability_result.get("message", f"{enemy.name} использует {ability_name}!")
            
            # Анимация способности врага
            if self.anim:
                self.anim.magic_animation(target_x, target_y, "#ff0000")
        else:
            # Обычная атака
            damage = enemy.attack(target)
            action_result["damage"] = damage
            action_result["message"] = f"👊 {enemy.name} атакует и наносит {damage} урона!"
        
        # Применение защиты
        if "defending" in self.active_effects["player"]:
            action_result["damage"] //= 2
        
        # Урон игроку
        if target == self.player:
            self.player["health"] -= action_result["damage"]
            
            # Анимация получения урона
            if self.anim and action_result["damage"] > 0:
                self.anim.damage_text(target_x, target_y, action_result["damage"])
            
            if self.player["health"] <= 0:
                self.player["health"] = 0
                self.defeat = True
                self.combat_active = False
                action_result["message"] += " 💀 Ты повержен!"
                
                # Анимация смерти
                if self.anim:
                    self.anim.explosion_animation(target_x, target_y, "#ff0000")
        
        self.add_to_log(action_result["message"])
        return action_result
    
    def select_target(self):
        """Выбор цели для врага"""
        if self.companions and random.random() < 0.3:
            # 30% шанс атаковать компаньона
            if self.companions:
                return random.choice(self.companions)
        return self.player
    
    def reduce_cooldowns(self):
        """Уменьшение кулдаунов"""
        for entity in ["player", "enemies", "companions"]:
            for skill in list(self.cooldowns[entity].keys()):
                self.cooldowns[entity][skill] -= 1
                if self.cooldowns[entity][skill] <= 0:
                    del self.cooldowns[entity][skill]
    
    def apply_regen(self):
        """Применение регенерации"""
        if "regen" in self.player:
            regen = self.player["regen"]
            self.player["health"] = min(self.player["max_health"], self.player["health"] + regen)
            if regen > 0:
                self.add_to_log(f"💚 Регенерация восстанавливает {regen} здоровья")
        
        if "mana_regen" in self.player:
            mana_regen = self.player["mana_regen"]
            self.player["mana"] = min(self.player["max_mana"], self.player["mana"] + mana_regen)
    
    def drop_loot(self, enemy: Enemy):
        """Выпадение лута"""
        if hasattr(enemy, 'loot_table') and enemy.loot_table:
            for item in enemy.loot_table:
                if random.random() < 0.5:  # 50% шанс
                    category = self.get_item_category(item)
                    self.player["inventory"].add_item(category, item, 1)
                    self.add_to_log(f"📦 Найден предмет: {item}")
                    
                    # Анимация лута
                    if self.anim:
                        self.anim.floating_text(400, 300, f"+{item}", "#ffd700")
    
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
    
    def next_turn(self) -> Tuple[str, Dict]:
        """Следующий ход"""
        if not self.combat_active:
            # Останавливаем музыку боя при завершении
            if self.sound:
                self.sound.stop_music()
            return "combat_end", {}
        
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        self.turn_count += 1
        
        current = self.turn_order[self.current_turn_index]
        
        if current[0] == "player":
            return "player", {"available_skills": self.skill_system.get_available_skills()}
        elif current[0].startswith("enemy"):
            result = self.enemy_turn(current)
            return "enemy", result
        else:
            # Ход компаньона (пока заглушка)
            return "companion", {"message": f"{current[1].name} готовится к атаке"}
    
    def check_combat_end(self) -> bool:
        """Проверка конца боя"""
        if not self.enemies:
            self.victory = True
            self.combat_active = False
            self.add_to_log("🎉 ПОБЕДА! Все враги повержены.")
            
            # Бонус за победу
            bonus_exp = 50 + len(self.enemies) * 10
            self.player["exp"] += bonus_exp
            self.add_to_log(f"✨ Бонус: +{bonus_exp} опыта")
            
            # Победная музыка
            if self.sound:
                self.sound.stop_music()
                self.sound.play_music("victory", loop=False)
            
            # Анимация победы
            if self.anim:
                self.anim.level_up_animation(400, 300)
            
            return True
        
        if self.player["health"] <= 0:
            self.defeat = True
            self.combat_active = False
            self.add_to_log("💔 ПОРАЖЕНИЕ...")
            
            if self.sound:
                self.sound.stop_music()
                self.sound.play_death()
            
            return True
        
        return False
    
    def get_combat_status(self) -> Dict:
        """Получение статуса боя"""
        return {
            "active": self.combat_active,
            "turn": self.turn_count,
            "enemies": len(self.enemies),
            "allies": len(self.companions) + 1,
            "player_health": f"{self.player['health']}/{self.player['max_health']}",
            "player_mana": f"{self.player['mana']}/{self.player['max_mana']}",
            "log": self.combat_log[-5:],
            "cooldowns": self.cooldowns["player"]
        }