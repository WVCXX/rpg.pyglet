import tkinter as tk
from tkinter import ttk
from core.game_state import GameState

class CharacterCreation:
    """Окно создания персонажа"""
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.window = None
        
        self.races = {
            "человек": {
                "desc": "Универсальная раса. +2 к удаче и харизме",
                "bonuses": {"удача": 2, "харизма": 2}
            },
            "эльф": {
                "desc": "Изящные и мудрые. +3 ловкость, +3 интеллект, -2 выносливость",
                "bonuses": {"ловкость": 3, "интеллект": 3, "выносливость": -2}
            },
            "гном": {
                "desc": "Крепкие и выносливые. +3 сила, +3 выносливость, -2 ловкость",
                "bonuses": {"сила": 3, "выносливость": 3, "ловкость": -2}
            },
            "орк": {
                "desc": "Мощные воины. +5 сила, +3 выносливость, -3 интеллект, -3 мудрость",
                "bonuses": {"сила": 5, "выносливость": 3, "интеллект": -3, "мудрость": -3}
            },
            "демон": {
                "desc": "Порождения тьмы. +2 сила, +2 интеллект, -2 харизма, -2 удача",
                "bonuses": {"сила": 2, "интеллект": 2, "харизма": -2, "удача": -2}
            },
            "зверолюд": {
                "desc": "Дети природы. +2 сила, +2 ловкость, -2 интеллект, -2 харизма",
                "bonuses": {"сила": 2, "ловкость": 2, "интеллект": -2, "харизма": -2}
            }
        }
        
        self.classes = {
            "воин": {
                "desc": "Мастер ближнего боя. Высокий урон и защита",
                "stats": {"сила": 3, "выносливость": 3},
                "weapon": "ржавый_меч",
                "color": "#ff4444"
            },
            "маг": {
                "desc": "Повелитель магии. Мощные заклинания, но слабая защита",
                "stats": {"интеллект": 4, "мудрость": 2},
                "weapon": "посох_ученика",
                "color": "#4444ff"
            },
            "вор": {
                "desc": "Мастер теней. Высокая ловкость, критические удары",
                "stats": {"ловкость": 4, "удача": 2},
                "weapon": "острый_клинок",
                "color": "#888888"
            },
            "жрец": {
                "desc": "Служитель богов. Лечение и поддержка",
                "stats": {"мудрость": 3, "харизма": 3},
                "weapon": "священный_символ",
                "color": "#ffff00"
            },
            "паладин": {
                "desc": "Святой воин. Баланс атаки и защиты",
                "stats": {"сила": 2, "выносливость": 2, "мудрость": 2},
                "weapon": "стальной_меч",
                "color": "#ffaa00"
            },
            "охотник": {
                "desc": "Следопыт. Дальний бой и ловушки",
                "stats": {"ловкость": 3, "выносливость": 2, "удача": 1},
                "weapon": "короткий_лук",
                "color": "#00aa00"
            }
        }
        
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2a2a2a',
            'fg_green': '#00ff00',
            'fg_red': '#ff4444',
            'fg_blue': '#4444ff',
            'fg_gold': '#ffd700',
            'fg_white': '#ffffff',
            'fg_gray': '#888888'
        }
    
    def show(self):
        """Показать окно создания персонажа"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Создание персонажа")
        self.window.geometry("900x700")
        self.window.configure(bg=self.colors['bg_dark'])
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Заголовок
        title = tk.Label(self.window, text="⚔ СОЗДАНИЕ ПЕРСОНАЖА ⚔",
                        bg=self.colors['bg_dark'],
                        fg=self.colors['fg_gold'],
                        font=('Cinzel', 20, 'bold'))
        title.pack(pady=20)
        
        # Имя персонажа
        name_frame = tk.Frame(self.window, bg=self.colors['bg_medium'])
        name_frame.pack(fill=tk.X, padx=50, pady=10)
        
        tk.Label(name_frame, text="Имя персонажа:",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_white'],
                font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        self.name_var = tk.StringVar(value="Джериан")
        name_entry = tk.Entry(name_frame, textvariable=self.name_var,
                             bg=self.colors['bg_light'],
                             fg=self.colors['fg_green'],
                             font=('Arial', 12),
                             width=20)
        name_entry.pack(side=tk.LEFT, padx=10)
        
        # Основной контейнер
        main_frame = tk.Frame(self.window, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Левая панель - выбор расы
        left_frame = tk.LabelFrame(main_frame, text="🌍 ВЫБОР РАСЫ",
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['fg_gold'],
                                   font=('Arial', 12, 'bold'))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.create_race_selection(left_frame)
        
        # Правая панель - выбор класса
        right_frame = tk.LabelFrame(main_frame, text="⚔ ВЫБОР КЛАССА",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_gold'],
                                    font=('Arial', 12, 'bold'))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.create_class_selection(right_frame)
        
        # Кнопки
        button_frame = tk.Frame(self.window, bg=self.colors['bg_dark'])
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(button_frame, text="❌ Отмена",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_red'],
                 command=self.window.destroy,
                 font=('Arial', 12),
                 width=15).pack(side=tk.LEFT, padx=20, expand=True)
        
        tk.Button(button_frame, text="✅ Начать игру",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_green'],
                 command=self.create_character,
                 font=('Arial', 12, 'bold'),
                 width=15).pack(side=tk.RIGHT, padx=20, expand=True)
    
    def create_race_selection(self, parent):
        """Создание выбора расы"""
        self.race_var = tk.StringVar(value="человек")
        
        # Список рас
        list_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(list_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for race_id, race_data in self.races.items():
            frame = tk.Frame(scrollable_frame, bg=self.colors['bg_light'],
                            relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, pady=5)
            
            # Радио-кнопка
            rb = tk.Radiobutton(frame, text=race_id.capitalize(),
                                variable=self.race_var, value=race_id,
                                bg=self.colors['bg_light'],
                                fg=self.colors['fg_gold'],
                                font=('Arial', 11, 'bold'),
                                selectcolor=self.colors['bg_dark'])
            rb.pack(anchor='w', padx=5, pady=2)
            
            # Описание
            desc_label = tk.Label(frame, text=race_data["desc"],
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['fg_white'],
                                  font=('Arial', 9),
                                  wraplength=350,
                                  justify=tk.LEFT)
            desc_label.pack(anchor='w', padx=20, pady=2)
            
            # Бонусы
            bonuses_text = "Бонусы: " + ", ".join([f"{stat}+{bonus}" if bonus > 0 else f"{stat}{bonus}" 
                                                   for stat, bonus in race_data["bonuses"].items()])
            bonus_label = tk.Label(frame, text=bonuses_text,
                                   bg=self.colors['bg_light'],
                                   fg=self.colors['fg_green'],
                                   font=('Arial', 8))
            bonus_label.pack(anchor='w', padx=20, pady=2)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_class_selection(self, parent):
        """Создание выбора класса"""
        self.class_var = tk.StringVar(value="воин")
        
        # Список классов
        list_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(list_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for class_id, class_data in self.classes.items():
            frame = tk.Frame(scrollable_frame, bg=class_data["color"],
                            relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, pady=5)
            
            # Радио-кнопка
            rb = tk.Radiobutton(frame, text=class_id.capitalize(),
                                variable=self.class_var, value=class_id,
                                bg=class_data["color"],
                                fg='black' if class_data["color"] != "#000000" else 'white',
                                font=('Arial', 11, 'bold'),
                                selectcolor=self.colors['bg_dark'])
            rb.pack(anchor='w', padx=5, pady=2)
            
            # Описание
            desc_label = tk.Label(frame, text=class_data["desc"],
                                  bg=class_data["color"],
                                  fg='black',
                                  font=('Arial', 9),
                                  wraplength=350,
                                  justify=tk.LEFT)
            desc_label.pack(anchor='w', padx=20, pady=2)
            
            # Статы
            stats_text = "Бонусы: " + ", ".join([f"{stat}+{bonus}" for stat, bonus in class_data["stats"].items()])
            stats_label = tk.Label(frame, text=stats_text,
                                   bg=class_data["color"],
                                   fg='black',
                                   font=('Arial', 8))
            stats_label.pack(anchor='w', padx=20, pady=2)
            
            # Оружие
            weapon_label = tk.Label(frame, text=f"Начальное оружие: {class_data['weapon']}",
                                    bg=class_data["color"],
                                    fg='black',
                                    font=('Arial', 8))
            weapon_label.pack(anchor='w', padx=20, pady=2)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_character(self):
        """Создание персонажа и запуск игры"""
        name = self.name_var.get().strip()
        if not name:
            name = "Джериан"
        
        race = self.race_var.get()
        player_class = self.class_var.get()
        
        # Создаем состояние игры
        game_state = GameState(name, race, player_class)
        
        # Закрываем окно создания
        self.window.destroy()
        
        # Запускаем игру с созданным персонажем
        self.callback(game_state)