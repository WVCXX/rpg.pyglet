import tkinter as tk
from tkinter import ttk, scrolledtext
from systems.combat_system import CombatSystem

class CombatScreen:
    """Экран боя"""
    
    def __init__(self, parent, combat_system: CombatSystem, game_window):
        self.parent = parent
        self.combat = combat_system
        self.game = game_window
        self.window = None
        
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2a2a2a',
            'fg_green': '#00ff00',
            'fg_red': '#ff4444',
            'fg_blue': '#4444ff',
            'fg_gold': '#ffd700',
            'fg_white': '#ffffff'
        }
    
    def show(self):
        """Показать окно боя"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("⚔ БОЙ ⚔")
        self.window.geometry("900x700")
        self.window.configure(bg=self.colors['bg_dark'])
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Основной контейнер
        main_frame = tk.Frame(self.window, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Верхняя панель с информацией о врагах
        self.create_enemy_panel(main_frame)
        
        # Центральная панель с логом боя
        self.create_log_panel(main_frame)
        
        # Нижняя панель с действиями
        self.create_action_panel(main_frame)
        
        # Информация об игроке
        self.create_player_info(main_frame)
        
        # Запуск первого хода
        self.process_turn()
    
    def create_enemy_panel(self, parent):
        """Панель с врагами"""
        enemy_frame = tk.LabelFrame(parent, text="👾 ВРАГИ",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_red'],
                                    font=('Arial', 12, 'bold'))
        enemy_frame.pack(fill=tk.X, pady=5)
        
        self.enemy_labels = []
        enemy_container = tk.Frame(enemy_frame, bg=self.colors['bg_medium'])
        enemy_container.pack(fill=tk.X, padx=10, pady=10)
        
        for i, enemy in enumerate(self.combat.enemies):
            frame = tk.Frame(enemy_container, bg=self.colors['bg_light'],
                            relief=tk.RAISED, bd=2)
            frame.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.BOTH)
            
            # Имя
            tk.Label(frame, text=enemy.name,
                    bg=self.colors['bg_light'],
                    fg=self.colors['fg_red'],
                    font=('Arial', 11, 'bold')).pack()
            
            # Уровень
            tk.Label(frame, text=f"Ур. {enemy.level}",
                    bg=self.colors['bg_light'],
                    fg=self.colors['fg_white']).pack()
            
            # Здоровье
            health_frame = tk.Frame(frame, bg=self.colors['bg_light'])
            health_frame.pack(pady=5)
            
            tk.Label(health_frame, text="❤️",
                    bg=self.colors['bg_light'],
                    fg=self.colors['fg_red']).pack(side=tk.LEFT)
            
            health_label = tk.Label(health_frame,
                                   text=f"{enemy.health}/{enemy.max_health}",
                                   bg=self.colors['bg_light'],
                                   fg=self.colors['fg_white'])
            health_label.pack(side=tk.LEFT, padx=5)
            
            self.enemy_labels.append({
                "frame": frame,
                "health": health_label,
                "enemy": enemy,
                "index": i
            })
            
            # Кнопка выбора цели
            tk.Button(frame, text="🎯 Выбрать",
                     bg=self.colors['bg_medium'],
                     fg=self.colors['fg_gold'],
                     command=lambda idx=i: self.select_target(idx)).pack(pady=5)
    
    def create_log_panel(self, parent):
        """Панель с логом боя"""
        log_frame = tk.LabelFrame(parent, text="📜 ЛОГ БОЯ",
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['fg_green'],
                                  font=('Arial', 12, 'bold'))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                  wrap=tk.WORD,
                                                  bg='#000000',
                                                  fg=self.colors['fg_green'],
                                                  font=('Consolas', 10),
                                                  height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)
    
    def create_action_panel(self, parent):
        """Панель с действиями"""
        action_frame = tk.LabelFrame(parent, text="⚡ ДЕЙСТВИЯ",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['fg_gold'],
                                     font=('Arial', 12, 'bold'))
        action_frame.pack(fill=tk.X, pady=5)
        
        # Базовые действия
        basic_frame = tk.Frame(action_frame, bg=self.colors['bg_medium'])
        basic_frame.pack(fill=tk.X, padx=10, pady=5)
        
        actions = [
            ("⚔ Атака", self.basic_attack, self.colors['fg_red']),
            ("🛡 Защита", self.defend, self.colors['fg_blue']),
            ("🏃 Бегство", self.flee, self.colors['fg_gray'])
        ]
        
        for text, cmd, color in actions:
            btn = tk.Button(basic_frame, text=text, command=cmd,
                           bg=self.colors['bg_light'],
                           fg=color,
                           width=15)
            btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # Навыки
        skills_frame = tk.LabelFrame(action_frame, text="✨ НАВЫКИ",
                                      bg=self.colors['bg_medium'],
                                      fg=self.colors['fg_gold'])
        skills_frame.pack(fill=tk.X, padx=10, pady=5)
        
        skills_container = tk.Frame(skills_frame, bg=self.colors['bg_medium'])
        skills_container.pack(fill=tk.X, padx=5, pady=5)
        
        available_skills = self.combat.skill_system.get_available_skills()
        
        if available_skills:
            row = 0
            col = 0
            for skill in available_skills[:6]:  # Показываем первые 6 навыков
                skill_id = skill["id"]
                current_level = self.combat.skill_system.skills.get(skill_id, 0)
                
                # Проверка кулдауна
                cooldown = self.combat.cooldowns["player"].get(skill_id, 0)
                
                btn_text = f"{skill['name']}\n{current_level}/{skill['max_level']}"
                if cooldown > 0:
                    btn_text = f"{skill['name']}\n⏳ {cooldown}"
                
                btn = tk.Button(skills_container, text=btn_text,
                               bg=self.colors['bg_light'],
                               fg=self.colors['fg_green'] if cooldown == 0 else self.colors['fg_gray'],
                               command=lambda sid=skill_id: self.use_skill(sid),
                               width=12, height=2)
                btn.grid(row=row, column=col, padx=2, pady=2)
                
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
        else:
            tk.Label(skills_container, text="Нет доступных навыков",
                    bg=self.colors['bg_medium'],
                    fg=self.colors['fg_gray']).pack()
    
    def create_player_info(self, parent):
        """Информация об игроке"""
        info_frame = tk.Frame(parent, bg=self.colors['bg_medium'],
                              relief=tk.SUNKEN, bd=2)
        info_frame.pack(fill=tk.X, pady=5)
        
        # Здоровье
        health_frame = tk.Frame(info_frame, bg=self.colors['bg_medium'])
        health_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(health_frame, text="❤️",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_red'],
                font=('Arial', 14)).pack(side=tk.LEFT)
        
        self.player_health = tk.Label(health_frame,
                                      text=f"{self.combat.player['health']}/{self.combat.player['max_health']}",
                                      bg=self.colors['bg_medium'],
                                      fg=self.colors['fg_white'],
                                      font=('Arial', 12))
        self.player_health.pack(side=tk.LEFT, padx=5)
        
        # Мана
        mana_frame = tk.Frame(info_frame, bg=self.colors['bg_medium'])
        mana_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(mana_frame, text="🔮",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_blue'],
                font=('Arial', 14)).pack(side=tk.LEFT)
        
        self.player_mana = tk.Label(mana_frame,
                                    text=f"{self.combat.player['mana']}/{self.combat.player['max_mana']}",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_white'],
                                    font=('Arial', 12))
        self.player_mana.pack(side=tk.LEFT, padx=5)
        
        # Выбранная цель
        self.target_label = tk.Label(info_frame,
                                     text="Цель: не выбрана",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['fg_gray'])
        self.target_label.pack(side=tk.RIGHT, padx=10)
    
    def select_target(self, index):
        """Выбор цели"""
        self.selected_target = index
        enemy = self.combat.enemies[index]
        self.target_label.config(text=f"Цель: {enemy.name}",
                                fg=self.colors['fg_gold'])
    
    def basic_attack(self):
        """Обычная атака"""
        if not hasattr(self, 'selected_target'):
            self.add_to_log("❌ Выбери цель!")
            return
        
        result = self.combat.player_turn("attack", self.selected_target)
        self.process_turn_result(result)
    
    def use_skill(self, skill_id):
        """Использование навыка"""
        if not hasattr(self, 'selected_target'):
            self.add_to_log("❌ Выбери цель!")
            return
        
        result = self.combat.player_turn("skill", self.selected_target, skill_id)
        self.process_turn_result(result)
    
    def defend(self):
        """Защита"""
        result = self.combat.player_turn("defend")
        self.process_turn_result(result)
    
    def flee(self):
        """Бегство"""
        result = self.combat.player_turn("flee")
        if "успешно" in result["message"]:
            self.window.destroy()
        else:
            self.add_to_log(result["message"])
            self.process_turn()
    
    def process_turn_result(self, result):
        """Обработка результата хода"""
        if result.get("message"):
            self.add_to_log(result["message"])
        
        self.update_ui()
        
        if not self.combat.combat_active:
            self.end_combat()
            return
        
        # Ход врагов
        self.window.after(1000, self.process_enemy_turns)
    
    def process_enemy_turns(self):
        """Обработка ходов врагов"""
        for _ in range(len(self.combat.enemies)):
            turn_type, result = self.combat.next_turn()
            if turn_type == "enemy" and result.get("message"):
                self.add_to_log(result["message"])
            
            self.update_ui()
            
            if not self.combat.combat_active:
                self.end_combat()
                return
        
        # Возвращаем ход игроку
        self.process_turn()
    
    def process_turn(self):
        """Обработка хода"""
        status = self.combat.get_combat_status()
        if status["active"]:
            self.add_to_log(f"\n--- ХОД {status['turn']} ---")
    
    def update_ui(self):
        """Обновление интерфейса"""
        # Обновление здоровья врагов
        for label_info in self.enemy_labels:
            enemy = label_info["enemy"]
            if enemy.is_alive:
                label_info["health"].config(text=f"{enemy.health}/{enemy.max_health}")
                label_info["frame"].config(bg=self.colors['bg_light'])
            else:
                label_info["health"].config(text="ПОВЕРЖЕН")
                label_info["frame"].config(bg=self.colors['bg_dark'])
        
        # Обновление здоровья игрока
        self.player_health.config(text=f"{self.combat.player['health']}/{self.combat.player['max_health']}")
        self.player_mana.config(text=f"{self.combat.player['mana']}/{self.combat.player['max_mana']}")
    
    def add_to_log(self, text):
        """Добавление в лог"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def end_combat(self):
        """Завершение боя"""
        if self.combat.victory:
            self.add_to_log("\n🎉 ПОБЕДА!")
            self.add_to_log(f"✨ Получено опыта: {sum(e.exp_reward for e in self.combat.enemies)}")
            self.add_to_log(f"💰 Получено золота: {sum(e.gold_reward for e in self.combat.enemies)}")
            
            # Обновление интерфейса игры
            self.game.update_ui()
            
            # Закрытие окна боя через 2 секунды
            self.window.after(2000, self.window.destroy)
        
        elif self.combat.defeat:
            self.add_to_log("\n💔 ПОРАЖЕНИЕ...")
            self.window.after(2000, lambda: self.game.death("Ты пал в бою"))