import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import traceback
import sys
import os
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game_state import GameState
from core.world import DynamicWorld
from core.save_system import SaveSystem
from core.cheats import CheatSystem
from systems.economy import MarketSystem
from systems.quests import QuestSystem
from systems.events import RandomEventGenerator
from entities.npc import NPC
from ui.character_screen import CharacterScreen
from ui.map_screen import MapScreen
from ui.inventory_screen import InventoryScreen
from ui.death_screen import DeathScreen
from ui.save_load_screen import SaveLoadScreen


class RPGameWindow:
    """Главное окно игры"""
    
    def __init__(self, root):
        print("\n🔧 ИНИЦИАЛИЗАЦИЯ RPGameWindow")
        print("-" * 40)
        
        self.root = root
        self.root.title("The Life and Suffering of Prince Jerian - Кровь и Пепел")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        self.colors = self.setup_colors()
        
        print("   Создание game_state...")
        self.game_state = GameState("Джериан")
        
        print("   Создание world...")
        self.world = DynamicWorld()
        
        print("   Создание market...")
        self.market = MarketSystem()
        
        print("   Создание quest_system...")
        self.quest_system = QuestSystem()
        
        print("   Создание event_gen...")
        self.event_gen = RandomEventGenerator()
        
        print("   Инициализация stats...")
        self.stats = self.init_stats()
        
        print("   Генерация NPC...")
        self.npcs = self.generate_npcs(30)
        
        print("   Создание cheat_system...")
        self.cheat_system = CheatSystem(self)
        
        # Режим бога
        self.godmode = False
        
        print("   Создание интерфейса...")
        self.setup_ui()
        
        print("   Показ вступления...")
        self.show_intro()
        
        print("   Обновление UI...")
        self.update_ui()
        
        print("   Настройка горячих клавиш...")
        self.setup_hotkeys()
        
        print("✅ RPGameWindow инициализирован успешно!\n")
    
    def setup_colors(self):
        """Настройка цветов"""
        return {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2a2a2a',
            'fg_green': '#00ff00',
            'fg_red': '#ff4444',
            'fg_blue': '#4444ff',
            'fg_gold': '#ffd700',
            'fg_white': '#ffffff',
            'fg_gray': '#888888',
            'accent': '#4a90e2',
            'accent_hover': '#5aa0f2'
        }
    
    def init_stats(self):
        """Инициализация статистики"""
        return {
            "игр_сыграно": 1,
            "часов_сыграно": 0,
            "врагов_убито": 0,
            "квестов_выполнено": 0,
            "смертей": 0,
            "шагов_сделано": 0,
            "золота_собрано": 0,
            "предметов_найдено": 0,
            "диалогов_проведено": 0,
            "зелий_выпито": 0
        }
    
    def generate_npcs(self, count: int) -> Dict[str, NPC]:
        """Генерация NPC"""
        npcs = {}
        races = ["человек", "эльф", "гном", "полурослик", "орк"]
        professions = [
            "крестьянин", "торговец", "стражник", "жрец", "кузнец",
            "трактирщик", "алхимик", "лекарь", "вор", "наемник"
        ]
        personalities = [
            "добрый", "злой", "хитрый", "честный", "грубый",
            "веселый", "угрюмый", "болтливый", "молчаливый"
        ]
        
        male_names = [
            "Иван", "Петр", "Алексей", "Дмитрий", "Сергей",
            "Владимир", "Михаил", "Андрей", "Павел", "Артем"
        ]
        
        female_names = [
            "Анна", "Мария", "Елена", "Ольга", "Наталья",
            "Светлана", "Ирина", "Екатерина", "Дарья", "София"
        ]
        
        print(f"      👥 Генерация {count} NPC...")
        
        for i in range(count):
            gender = random.choice(["муж", "жен"])
            name = random.choice(male_names) if gender == "муж" else random.choice(female_names)
            
            if random.random() < 0.3:
                nicknames = ["Хитрый", "Сильный", "Мудрый", "Быстрый"]
                name += f" {random.choice(nicknames)}"
            
            npc = NPC(
                f"npc_{i}",
                name,
                random.choice(races),
                gender,
                random.choice(professions),
                random.choice(personalities)
            )
            
            npc.location = random.choice([
                "городская_площадь", "таверна", "храм", "рынок",
                "трущобы", "порт", "кузница"
            ])
            
            npcs[npc.id] = npc
        
        print(f"      ✅ Сгенерировано {len(npcs)} NPC")
        return npcs
    
    def setup_ui(self):
        """Создание интерфейса"""
        self.main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        self.create_header()
        self.create_content_area()
        self.create_footer()
    
    def create_header(self):
        """Создание шапки"""
        header = tk.Frame(self.main_container, bg=self.colors['bg_medium'], height=80)
        header.pack(fill=tk.X, pady=(0, 2))
        header.pack_propagate(False)
        
        left_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        
        self.name_label = tk.Label(left_frame, 
                                   text=self.game_state.player["name"],
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['fg_gold'],
                                   font=('Cinzel', 18, 'bold'))
        self.name_label.pack(anchor='w')
        
        self.level_label = tk.Label(left_frame,
                                    text=f"Уровень {self.game_state.player['level']}",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_green'],
                                    font=('Arial', 12))
        self.level_label.pack(anchor='w')

        center_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        self.time_label = tk.Label(center_frame,
                                   text=self.get_time_string(),
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['fg_white'],
                                   font=('Arial', 14))
        self.time_label.pack(expand=True)
        
        self.weather_label = tk.Label(center_frame,
                                      text=f"🌤 {self.world.weather}",
                                      bg=self.colors['bg_medium'],
                                      fg=self.colors['fg_blue'],
                                      font=('Arial', 12))
        self.weather_label.pack()
        
        right_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        

        health_frame = tk.Frame(right_frame, bg=self.colors['bg_medium'])
        health_frame.pack(anchor='e', pady=2)
        
        tk.Label(health_frame, text="❤", bg=self.colors['bg_medium'],
                fg=self.colors['fg_red'], font=('Arial', 14)).pack(side=tk.LEFT)
        
        self.health_label = tk.Label(health_frame,
                                     text=f"{self.game_state.player['health']}/{self.game_state.player['max_health']}",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['fg_white'])
        self.health_label.pack(side=tk.LEFT, padx=5)
        
        # Мана
        mana_frame = tk.Frame(right_frame, bg=self.colors['bg_medium'])
        mana_frame.pack(anchor='e', pady=2)
        
        tk.Label(mana_frame, text="🔮", bg=self.colors['bg_medium'],
                fg=self.colors['fg_blue'], font=('Arial', 14)).pack(side=tk.LEFT)
        
        self.mana_label = tk.Label(mana_frame,
                                   text=f"{self.game_state.player['mana']}/{self.game_state.player['max_mana']}",
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['fg_white'])
        self.mana_label.pack(side=tk.LEFT, padx=5)
        
        # Деньги
        money_frame = tk.Frame(right_frame, bg=self.colors['bg_medium'])
        money_frame.pack(anchor='e', pady=2)
        
        tk.Label(money_frame, text="💰", bg=self.colors['bg_medium'],
                fg=self.colors['fg_gold'], font=('Arial', 14)).pack(side=tk.LEFT)
        
        self.money_label = tk.Label(money_frame,
                                    text=str(self.game_state.player['money']),
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_white'])
        self.money_label.pack(side=tk.LEFT, padx=5)
    
    def create_content_area(self):
        """Создание основной области"""
        content = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        content.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # Левая панель (инвентарь)
        self.create_inventory_panel(content)
        
        # Центральная панель (текст игры)
        self.create_game_panel(content)
        
        # Правая панель (NPC и квесты)
        self.create_info_panel(content)
    
    def create_inventory_panel(self, parent):
        """Создание панели инвентаря"""
        panel = tk.Frame(parent, bg=self.colors['bg_medium'], width=250)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))
        panel.pack_propagate(False)
        
        # Заголовок
        title_frame = tk.Frame(panel, bg=self.colors['bg_medium'])
        title_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(title_frame, text="📦 ИНВЕНТАРЬ",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_gold'],
                font=('Arial', 12, 'bold')).pack()
        
        # Канвас с прокруткой
        canvas = tk.Canvas(panel, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        self.inv_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        self.inv_frame.bind("<Configure>", 
                           lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inv_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка полного инвентаря
        tk.Button(panel, text="Полный инвентарь",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=self.show_inventory_screen,
                 relief=tk.FLAT).pack(fill=tk.X, padx=5, pady=5)
    
    def create_game_panel(self, parent):
        """Создание панели с текстом"""
        panel = tk.Frame(parent, bg=self.colors['bg_medium'])
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        
        # Заголовок локации
        title_frame = tk.Frame(panel, bg=self.colors['bg_medium'])
        title_frame.pack(fill=tk.X, pady=5)
        
        location_name = self.get_location_display(self.game_state.current_location)
        tk.Label(title_frame, text=f"📍 {location_name}",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_white'],
                font=('Arial', 14, 'bold')).pack()
        
        # Текстовое поле
        text_frame = tk.Frame(panel, bg=self.colors['bg_light'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.game_text = scrolledtext.ScrolledText(text_frame,
                                                   wrap=tk.WORD,
                                                   bg='#000000',
                                                   fg=self.colors['fg_green'],
                                                   font=('Consolas', 11),
                                                   insertbackground=self.colors['fg_green'],
                                                   height=20)
        self.game_text.pack(fill=tk.BOTH, expand=True)
        self.game_text.config(state=tk.DISABLED)
        
        # Панель действий
        self.create_action_panel(panel)
    
    def create_action_panel(self, parent):
        """Создание панели действий"""
        panel = tk.Frame(parent, bg=self.colors['bg_medium'])
        panel.pack(fill=tk.X, pady=5)
        
        actions = [
            ("🔍 Осмотреть", self.examine),
            ("🗺 Карта", self.show_map),
            ("📊 Характеристики", self.show_character),
            ("💾 Сохранить", self.save_game),
            ("📂 Загрузить", self.load_game)
        ]
        
        for text, cmd in actions:
            btn = tk.Button(panel, text=text,
                           bg=self.colors['bg_light'],
                           fg=self.colors['fg_white'],
                           command=cmd,
                           relief=tk.FLAT,
                           padx=10)
            btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Кнопки локаций
        loc_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        loc_frame.pack(fill=tk.X, pady=5)
        
        locations = [
            ("🏛 Площадь", "городская_площадь"),
            ("🍺 Таверна", "таверна"),
            ("🏪 Рынок", "рынок"),
            ("🏚 Трущобы", "трущобы"),
            ("⛪ Храм", "храм"),
            ("🏰 Замок", "замок")
        ]
        
        for text, loc in locations:
            btn = tk.Button(loc_frame, text=text,
                           bg=self.colors['bg_light'],
                           fg=self.colors['fg_white'],
                           command=lambda l=loc: self.move_to_location(l),
                           relief=tk.FLAT)
            btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
    
    def create_info_panel(self, parent):
        """Создание информационной панели"""
        panel = tk.Frame(parent, bg=self.colors['bg_medium'], width=300)
        panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 0))
        panel.pack_propagate(False)
        
        # Вкладки
        notebook = ttk.Notebook(panel)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка NPC
        npc_frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(npc_frame, text="👥 Персонажи")
        
        list_frame = tk.Frame(npc_frame, bg=self.colors['bg_light'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.npc_list = tk.Listbox(list_frame,
                                   bg=self.colors['bg_light'],
                                   fg=self.colors['fg_green'],
                                   selectbackground=self.colors['accent'],
                                   font=('Arial', 10),
                                   height=15)
        self.npc_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        npc_scroll = tk.Scrollbar(list_frame)
        npc_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.npc_list.config(yscrollcommand=npc_scroll.set)
        npc_scroll.config(command=self.npc_list.yview)
        
        self.npc_list.bind('<Double-Button-1>', self.on_npc_select)
        
        # Вкладка квестов
        quest_frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(quest_frame, text="⚔ Квесты")
        
        self.quest_text = tk.Text(quest_frame,
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['fg_gold'],
                                  font=('Arial', 10),
                                  wrap=tk.WORD,
                                  height=15)
        self.quest_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.quest_text.config(state=tk.DISABLED)
        
        # Вкладка репутации
        rep_frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(rep_frame, text="📈 Репутация")
        
        self.rep_text = tk.Text(rep_frame,
                                bg=self.colors['bg_light'],
                                fg=self.colors['fg_white'],
                                font=('Arial', 10),
                                wrap=tk.WORD,
                                height=15)
        self.rep_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.rep_text.config(state=tk.DISABLED)
    
    def create_footer(self):
        """Создание нижней панели"""
        footer = tk.Frame(self.main_container, bg=self.colors['bg_medium'], height=30)
        footer.pack(fill=tk.X, pady=(2, 0))
        footer.pack_propagate(False)
        
        stats_text = f"Врагов: {self.stats['врагов_убито']} | Квестов: {self.stats['квестов_выполнено']} | Смертей: {self.stats['смертей']}"
        
        self.stats_label = tk.Label(footer,
                                    text=stats_text,
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_gray'],
                                    font=('Arial', 9))
        self.stats_label.pack(side=tk.LEFT, padx=10)
        
        tk.Label(footer,
                text="v1.0.0",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_gray'],
                font=('Arial', 9)).pack(side=tk.RIGHT, padx=10)
    
    def setup_hotkeys(self):
        """Настройка горячих клавиш"""
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<F2>', lambda e: self.show_character())
        self.root.bind('<F3>', lambda e: self.show_inventory_screen())
        self.root.bind('<F4>', lambda e: self.show_map())
        self.root.bind('<F5>', lambda e: self.save_game())
        self.root.bind('<F9>', lambda e: self.load_game())
        self.root.bind('<F12>', lambda e: self.show_cheat_console())
        self.root.bind('<Escape>', lambda e: self.quit_game())
    
    def get_time_string(self) -> str:
        """Получение строки времени"""
        hour = self.world.hour
        minute = self.world.minute
        
        if 6 <= hour < 12:
            period = "🌅 Утро"
        elif 12 <= hour < 18:
            period = "☀ День"
        elif 18 <= hour < 22:
            period = "🌆 Вечер"
        else:
            period = "🌙 Ночь"
        
        return f"День {self.world.day}, {period} ({hour:02d}:{minute:02d})"
    
    def get_location_display(self, location: str) -> str:
        """Получение названия локации"""
        locations = {
            "городская_площадь": "Городская площадь",
            "таверна": "Таверна 'Гнилой Зуб'",
            "рынок": "Торговая площадь",
            "трущобы": "Гнилые трущобы",
            "храм": "Храм Единого",
            "замок": "Княжеский замок",
            "порт": "Морской порт",
            "кузница": "Кузница гномов",
            "гильдия": "Гильдия искателей",
            "кладбище": "Старое кладбище",
            "подземелье": "Темные подземелья"
        }
        return locations.get(location, location.replace('_', ' ').title())
    
    def add_text(self, text: str, text_type: str = "normal"):
        """Добавление текста"""
        self.game_text.config(state=tk.NORMAL)
        
        colors = {
            "normal": self.colors['fg_green'],
            "warning": self.colors['fg_red'],
            "success": "#00ff00",
            "info": self.colors['fg_blue'],
            "gold": self.colors['fg_gold'],
            "system": self.colors['fg_gray']
        }
        
        self.game_text.insert(tk.END, text + "\n", text_type)
        self.game_text.tag_config(text_type, 
                                 foreground=colors.get(text_type, self.colors['fg_green']))
        self.game_text.see(tk.END)
        self.game_text.config(state=tk.DISABLED)
    
    def update_ui(self):
        """Обновление интерфейса"""
        self.time_label.config(text=self.get_time_string())
        self.weather_label.config(text=f"🌤 {self.world.weather}")
        self.health_label.config(text=f"{self.game_state.player['health']}/{self.game_state.player['max_health']}")
        self.mana_label.config(text=f"{self.game_state.player['mana']}/{self.game_state.player['max_mana']}")
        self.money_label.config(text=str(self.game_state.player['money']))
        self.level_label.config(text=f"Уровень {self.game_state.player['level']}")
        
        self.update_inventory_display()
        self.update_npc_list()
        self.update_quest_display()
        self.update_reputation_display()
        
        stats_text = f"Врагов: {self.stats['врагов_убито']} | Квестов: {self.stats['квестов_выполнено']} | Смертей: {self.stats['смертей']}"
        self.stats_label.config(text=stats_text)
    
    def update_inventory_display(self):
        """Обновление инвентаря"""
        for widget in self.inv_frame.winfo_children():
            widget.destroy()
        
        inventory = self.game_state.player["inventory"]
        items = inventory.get_all_items()
        
        category_names = {
            "weapons": "⚔ Оружие",
            "armor": "🛡 Броня",
            "potions": "🧪 Зелья",
            "books": "📚 Книги",
            "ingredients": "🌿 Ингредиенты",
            "keys": "🔑 Ключи",
            "misc": "📦 Разное"
        }
        
        row = 0
        for cat_key, cat_name in category_names.items():
            if cat_key in items and items[cat_key]:
                tk.Label(self.inv_frame,
                        text=cat_name,
                        bg=self.colors['bg_light'],
                        fg=self.colors['fg_gold'],
                        font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', pady=(5,0))
                row += 1
                
                for item_name, count in items[cat_key]:
                    display_name = item_name.replace('_', ' ').title()
                    if count > 1:
                        text = f"  • {display_name} x{count}"
                    else:
                        text = f"  • {display_name}"
                    
                    tk.Label(self.inv_frame,
                            text=text,
                            bg=self.colors['bg_light'],
                            fg=self.colors['fg_green'],
                            font=('Arial', 9)).grid(row=row, column=0, sticky='w')
                    row += 1
    
    def update_npc_list(self):
        """Обновление списка NPC"""
        self.npc_list.delete(0, tk.END)
        
        for npc in self.npcs.values():
            if npc.location == self.game_state.current_location and npc.is_alive:
                rel = self.game_state.player["relationships"].get(npc.id, 0)
                rel_symbol = "❤" if rel > 50 else "💔" if rel < 0 else "●"
                
                display_text = f"{rel_symbol} {npc.name} ({npc.profession})"
                self.npc_list.insert(tk.END, display_text)
        
        if self.npc_list.size() == 0:
            self.npc_list.insert(tk.END, "Никого нет")
    
    def update_quest_display(self):
        """Обновление квестов"""
        self.quest_text.config(state=tk.NORMAL)
        self.quest_text.delete(1.0, tk.END)
        
        if self.quest_system.active_quests:
            for quest in self.quest_system.active_quests:
                self.quest_text.insert(tk.END, f"⚔ {quest['name']}\n")
                self.quest_text.insert(tk.END, f"   {quest['description']}\n")
                self.quest_text.insert(tk.END, f"   Награда: {quest['reward']}💰\n\n")
        else:
            self.quest_text.insert(tk.END, "Нет активных квестов")
        
        self.quest_text.config(state=tk.DISABLED)
    
    def update_reputation_display(self):
        """Обновление репутации"""
        self.rep_text.config(state=tk.NORMAL)
        self.rep_text.delete(1.0, tk.END)
        
        for group, value in self.game_state.player["reputation"].items():
            if value > 50:
                color = "#00ff00"
            elif value > 0:
                color = "#ffff00"
            elif value > -50:
                color = "#ff8800"
            else:
                color = "#ff0000"
            
            bar_length = int(abs(value) / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            
            self.rep_text.insert(tk.END, f"{group}:\n", ("group",))
            self.rep_text.insert(tk.END, f"[{bar}] {value}\n\n", ("value", color))
        
        self.rep_text.config(state=tk.DISABLED)
    
    def move_to_location(self, location_name: str):
        """Перемещение в локацию"""
        self.game_state.current_location = location_name
        self.world.advance_time(10)
        self.stats["шагов_сделано"] += 1
        
        self.add_text(f"\n📍 Ты переместился в {self.get_location_display(location_name)}", "info")
        
        if random.random() < 0.2:
            self.trigger_random_event()
        
        self.update_ui()
    
    def on_npc_select(self, event):
        """Выбор NPC"""
        selection = self.npc_list.curselection()
        if selection:
            npc_text = self.npc_list.get(selection[0])
            if npc_text != "Никого нет":
                npc_name = npc_text.split(' ', 1)[-1].split(' (')[0]
                
                for npc in self.npcs.values():
                    if npc.name == npc_name:
                        self.talk_to_npc(npc)
                        break
    
    def talk_to_npc(self, npc: NPC):
        """Разговор с NPC"""
        self.add_text(f"\n--- {npc.name} ---", "gold")
        self.add_text(npc.dialog["greeting"], "info")
        
        current_rel = self.game_state.player["relationships"].get(npc.id, 0)
        current_rel += random.randint(-2, 5)
        self.game_state.player["relationships"][npc.id] = max(-100, min(100, current_rel))
        
        self.stats["диалогов_проведено"] += 1
        
        if npc.is_merchant and npc.trade_goods:
            self.add_text(f"💰 {npc.name}: Хочешь посмотреть товары?", "info")
        
        self.update_ui()
    
    def examine(self):
        """Осмотр локации"""
        self.add_text("\n🔍 Ты внимательно осматриваешься...", "info")
        
        if random.random() < 0.25:
            items = [
                ("монета", "misc", 1, random.randint(1, 10)),
                ("ржавый_меч", "weapons", 1, 0),
                ("старая_книга", "books", 1, 0),
                ("зелье_здоровья", "potions", random.randint(1, 3), 0),
                ("ключ", "keys", 1, 0),
                ("веревка", "misc", 1, 0),
                ("факел", "misc", random.randint(1, 3), 0)
            ]
            
            item_name, category, count, gold = random.choice(items)
            
            if gold > 0:
                self.game_state.player["money"] += gold
                self.add_text(f"💰 Ты нашел {gold} монет!", "success")
                self.stats["золота_собрано"] += gold
            else:
                self.game_state.player["inventory"].add_item(category, item_name, count)
                self.add_text(f"📦 Ты нашел: {item_name.replace('_', ' ').title()} x{count}", "success")
                self.stats["предметов_найдено"] += count
            
            self.update_ui()
        else:
            self.add_text("Ничего интересного.", "system")
    
    def trigger_random_event(self):
        """Случайное событие"""
        event = self.event_gen.get_random_event()
        if event:
            self.add_text(f"\n⚡ {event['name']}!", "warning")
            self.add_text(event['text'], "info")
            
            if callable(event.get('effect')):
                event['effect'](self.game_state.player)
    
    def show_cheat_console(self):
        """Показать консоль читов"""
        console = tk.Toplevel(self.root)
        console.title("Консоль читов")
        console.geometry("500x300")
        console.configure(bg='#0a0a0a')
        console.transient(self.root)
        
        # Заголовок
        tk.Label(console, text="💀 ЧИТ-КОНСОЛЬ 💀",
                bg='#0a0a0a', fg='#00ff00',
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Поле ввода
        entry_frame = tk.Frame(console, bg='#0a0a0a')
        entry_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(entry_frame, text="Введите чит-код:",
                bg='#0a0a0a', fg='#ffffff').pack(anchor='w')
        
        entry = tk.Entry(entry_frame, bg='#1a1a1a', fg='#00ff00',
                         font=('Courier', 12), insertbackground='#00ff00')
        entry.pack(fill=tk.X, pady=5)
        entry.focus()
        
        # Результат
        result_frame = tk.Frame(console, bg='#0a0a0a')
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        result_text = scrolledtext.ScrolledText(result_frame,
                                                wrap=tk.WORD,
                                                bg='#1a1a1a',
                                                fg='#00ff00',
                                                font=('Consolas', 10),
                                                height=8)
        result_text.pack(fill=tk.BOTH, expand=True)
        
        def execute_cheat():
            cheat = entry.get().strip()
            if cheat:
                result = self.cheat_system.process_cheat(cheat)
                result_text.insert(tk.END, f"> {cheat}\n{result}\n\n")
                result_text.see(tk.END)
                entry.delete(0, tk.END)
        
        def show_help():
            result_text.insert(tk.END, self.cheat_system.show_cheats() + "\n\n")
            result_text.see(tk.END)
        
        # Кнопки
        btn_frame = tk.Frame(console, bg='#0a0a0a')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Выполнить", command=execute_cheat,
                 bg='#333', fg='#00ff00', width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Справка", command=show_help,
                 bg='#333', fg='#ffff00', width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Закрыть", command=console.destroy,
                 bg='#333', fg='#ff4444', width=12).pack(side=tk.LEFT, padx=5)
        
        entry.bind('<Return>', lambda e: execute_cheat())
    
    def show_map(self):
        """Показать карту"""
        map_screen = MapScreen(self.root, self.world, self.game_state.current_location)
        map_screen.show()
    
    def show_character(self):
        """Показать характеристики"""
        char_screen = CharacterScreen(self.root, self.game_state.player)
        char_screen.show()
    
    def show_inventory_screen(self):
        """Показать полный инвентарь"""
        inv_screen = InventoryScreen(self.root, self.game_state.player["inventory"])
        inv_screen.show()
    
    def save_game(self):
        """Сохранение игры"""
        self.add_text("\n💾 Сохранение...", "system")
        
        success, message = SaveSystem.save_game(
            self.game_state,
            self.world,
            self.market,
            self.quest_system,
            self.stats
        )
        
        if success:
            self.add_text(f"✅ {message}", "success")
        else:
            self.add_text(f"❌ Ошибка сохранения: {message}", "warning")
    
    def load_game(self):
        """Загрузка игры"""
        save_load_screen = SaveLoadScreen(self.root, self)
        save_load_screen.show()
    
    def perform_load(self, filename: str):
        """Выполнение загрузки"""
        success, data = SaveSystem.load_game(filename)
        
        if success:
            try:
                self.game_state = GameState.from_dict(data["game_state"])
                self.world = DynamicWorld.from_dict(data["world"])
                self.market = MarketSystem()
                for key, value in data["market"].items():
                    setattr(self.market, key, value)
                self.quest_system = QuestSystem.from_dict(data["quest_system"])
                self.stats = data["stats"]
                
                self.add_text(f"\n✅ Загружено: {filename}", "success")
                self.update_ui()
            except Exception as e:
                self.add_text(f"❌ Ошибка загрузки: {e}", "warning")
        else:
            self.add_text(f"❌ Ошибка загрузки: {data}", "warning")
    
    def show_intro(self):
        """Показать вступление"""
        intro = """
╔══════════════════════════════════════════════════════════════╗
║     THE LIFE AND SUFFERING OF PRINCE JERIAN                  ║
║                    КРОВЬ И ПЕПЕЛ                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   Ты - Джериан, проклятый с рождения.                        ║
║   Тьма внутри тебя растет с каждым днем.                     ║
║                                                              ║
║   Сможешь ли ты победить демона внутри себя?                 ║
║   Или станешь величайшим злом этого мира?                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.add_text(intro, "gold")
        self.add_text("\n⚡ Используй кнопки локаций чтобы начать путешествие...", "info")
        self.add_text("💡 Горячие клавиши: F1 - помощь, F5 - сохранить, F9 - загрузить, F12 - читы", "system")
    
    def show_help(self):
        """Показать помощь"""
        help_text = """
📖 СПРАВКА:

⚔ ИГРОВОЙ ПРОЦЕСС:
  • Перемещайся по локациям используя кнопки внизу
  • Общайся с NPC для получения квестов и информации
  • Исследуй мир и находи сокровища

⌨ ГОРЯЧИЕ КЛАВИШИ:
  F1 - эта справка
  F2 - характеристики
  F3 - инвентарь
  F4 - карта
  F5 - сохранить
  F9 - загрузить
  F12 - консоль читов
  ESC - выход

💀 ЧИТ-КОДЫ:
  hesoyam - восстановить ресурсы
  baguvix - +1000 золота
  levelup - повысить уровень
  godmode - режим бога
  allweapons - всё оружие
  allpotions - все зелья
        """
        self.add_text(help_text, "info")
    
    def quit_game(self):
        """Выход из игры"""
        if messagebox.askyesno("Выход", "Точно хочешь выйти? Несохраненный прогресс будет потерян."):
            self.root.quit()
    
    def death(self, reason: str = ""):
        """Обработка смерти"""
        self.stats["смертей"] += 1
        self.game_state.player["death_count"] += 1
        
        death_screen = DeathScreen(self.root, self.stats, self.death_callback)
        death_screen.show(reason)
    
    def death_callback(self, action: str):
        """Колбэк после смерти"""
        if action == "load":
            self.load_game()
        elif action == "new":
            self.new_game()
        elif action == "quit":
            self.root.quit()
    
    def new_game(self):
        """Новая игра"""
        self.game_state = GameState("Джериан")
        self.world = DynamicWorld()
        self.market = MarketSystem()
        self.quest_system = QuestSystem()
        self.stats = self.init_stats()
        self.npcs = self.generate_npcs(30)
        
        self.show_intro()
        self.update_ui()
    
    def run(self):
        """Запуск игры"""
        self.root.mainloop()