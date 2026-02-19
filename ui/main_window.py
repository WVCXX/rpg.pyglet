import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game_state import GameState
from core.world import DynamicWorld
from core.save_system import SaveSystem
from systems.economy import MarketSystem
from systems.quests import QuestSystem
from systems.events import RandomEventGenerator
from entities.npc import NPC

class RPGameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("The Life and Suffering of Prince Jerian")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        
        self.game_state = GameState()
        self.world = DynamicWorld()
        self.market = MarketSystem()
        self.quest_system = QuestSystem()
        self.event_gen = RandomEventGenerator()
        self.stats = self.init_stats()
        
        # Генерация NPC
        self.npcs = self.generate_npcs(20)
        
        # Создание интерфейса
        self.setup_ui()
        
        # Запуск
        self.show_intro()
    
    def init_stats(self):
        """Инициализация статистики"""
        return {
            "games_played": 1,
            "hours_played": 0,
            "enemies_killed": 0,
            "quests_completed": 0,
            "deaths": 0,
            "steps_taken": 0,
            "gold_collected": 0
        }
    
    def generate_npcs(self, count):
        """Генерация NPC"""
        npcs = {}
        races = ["человек", "эльф", "гном"]
        professions = ["крестьянин", "торговец", "стражник", "жрец", "кузнец"]
        personalities = ["добрый", "злой", "хитрый", "честный", "грубый"]
        
        for i in range(count):
            race = random.choice(races)
            gender = random.choice(["муж", "жен"])
            name = self.generate_name(race, gender)
            
            npc = NPC(
                f"npc_{i}",
                name,
                race,
                gender,
                random.choice(professions),
                random.choice(personalities)
            )
            npc.location = random.choice(["town_square", "tavern", "temple", "market"])
            npcs[npc.id] = npc
        
        return npcs
    
    def generate_name(self, race, gender):
        """Генерация имени"""
        names = {
            "человек": {"муж": ["Иван", "Петр", "Алексей", "Дмитрий", "Сергей"], 
                       "жен": ["Анна", "Мария", "Елена", "Ольга", "Наталья"]},
            "эльф": {"муж": ["Эриан", "Леголас", "Элронд"], 
                    "жен": ["Арвен", "Галадриэль", "Лутиэн"]},
            "гном": {"муж": ["Гимли", "Торин", "Балин"], 
                    "жен": ["Диса", "Хельга", "Бригитта"]}
        }
        name_dict = names.get(race, names["человек"])
        name_list = name_dict.get(gender, name_dict["муж"])
        return random.choice(name_list)
    
    def setup_ui(self):
        """Настройка интерфейса"""
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Верхняя панель статуса
        status_frame = tk.Frame(main_frame, bg='#1a1a1a', height=60)
        status_frame.pack(fill=tk.X, pady=(0, 5))
        status_frame.pack_propagate(False)
        
        self.name_label = tk.Label(status_frame, text=self.game_state.player["name"], 
                                   bg='#1a1a1a', fg='gold', font=('Arial', 12, 'bold'))
        self.name_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(status_frame, 
                                   text=f"День {self.world.day}, {self.world.hour:02d}:{self.world.minute:02d}",
                                   bg='#1a1a1a', fg='#00ff00')
        self.time_label.pack(side=tk.LEFT, padx=20)
        
        self.weather_label = tk.Label(status_frame, text=self.world.weather,
                                      bg='#1a1a1a', fg='#87ceeb')
        self.weather_label.pack(side=tk.LEFT, padx=20)
        
        self.health_label = tk.Label(status_frame, 
                                     text=f"❤ {self.game_state.player['health']}/{self.game_state.player['max_health']}",
                                     bg='#1a1a1a', fg='#ff4444')
        self.health_label.pack(side=tk.RIGHT, padx=10)
        
        self.money_label = tk.Label(status_frame, 
                                    text=f"💰 {self.game_state.player['money']}",
                                    bg='#1a1a1a', fg='gold')
        self.money_label.pack(side=tk.RIGHT, padx=10)
        
        # Основная область
        center_frame = tk.Frame(main_frame, bg='#0a0a0a')
        center_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая панель (инвентарь)
        left_frame = tk.Frame(center_frame, bg='#1a1a1a', width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text="ИНВЕНТАРЬ", bg='#1a1a1a', fg='gold').pack(pady=5)
        
        self.inv_text = tk.Text(left_frame, bg='#2a2a2a', fg='#00ff00', height=15)
        self.inv_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Центральная панель (текст игры)
        center_panel = tk.Frame(center_frame, bg='#1a1a1a')
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.game_text = scrolledtext.ScrolledText(center_panel, wrap=tk.WORD,
                                                   bg='black', fg='#00ff00',
                                                   font=('Courier', 10),
                                                   height=25)
        self.game_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.game_text.config(state=tk.DISABLED)
        
        # Правая панель (NPC и квесты)
        right_frame = tk.Frame(center_frame, bg='#1a1a1a', width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_frame.pack_propagate(False)
        
        tk.Label(right_frame, text="ПЕРСОНАЖИ", bg='#1a1a1a', fg='gold').pack(pady=5)
        
        self.npc_list = tk.Listbox(right_frame, bg='#2a2a2a', fg='#00ff00', height=10)
        self.npc_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.npc_list.bind('<Double-Button-1>', self.on_npc_select)
        
        tk.Label(right_frame, text="КВЕСТЫ", bg='#1a1a1a', fg='gold').pack(pady=5)
        
        self.quest_text = tk.Text(right_frame, bg='#2a2a2a', fg='#00ff00', height=8)
        self.quest_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Нижняя панель (кнопки)
        button_frame = tk.Frame(main_frame, bg='#1a1a1a', height=50)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        button_frame.pack_propagate(False)
        
        # Кнопки действий
        actions = [
            ("Осмотреть", self.examine),
            ("Инвентарь", self.show_inventory),
            ("Карта", self.show_map),
            ("Персонаж", self.show_character),
            ("Сохранить", self.save_game),
            ("Загрузить", self.load_game)
        ]
        
        for text, cmd in actions:
            btn = tk.Button(button_frame, text=text, bg='#333', fg='white',
                           command=cmd)
            btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Кнопки локаций
        loc_frame = tk.Frame(main_frame, bg='#1a1a1a', height=40)
        loc_frame.pack(fill=tk.X, pady=(5, 0))
        loc_frame.pack_propagate(False)
        
        locations = [
            ("Площадь", "town_square"),
            ("Таверна", "tavern"),
            ("Рынок", "market"),
            ("Трущобы", "slums"),
            ("Храм", "temple"),
            ("Замок", "castle")
        ]
        
        for text, loc in locations:
            btn = tk.Button(loc_frame, text=text, bg='#333', fg='white',
                           command=lambda l=loc: self.move_to_location(l))
            btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
    
    def add_text(self, text):
        """Добавление текста"""
        self.game_text.config(state=tk.NORMAL)
        self.game_text.insert(tk.END, text + "\n")
        self.game_text.see(tk.END)
        self.game_text.config(state=tk.DISABLED)
    
    def update_ui(self):
        """Обновление интерфейса"""
        self.time_label.config(text=f"День {self.world.day}, {self.world.hour:02d}:{self.world.minute:02d}")
        self.weather_label.config(text=self.world.weather)
        self.health_label.config(text=f"❤ {self.game_state.player['health']}/{self.game_state.player['max_health']}")
        self.money_label.config(text=f"💰 {self.game_state.player['money']}")
        
        # Обновление инвентаря
        self.inv_text.delete(1.0, tk.END)
        for category, items in self.game_state.player["inventory"].items():
            if items:
                self.inv_text.insert(tk.END, f"{category}:\n")
                for item in items:
                    self.inv_text.insert(tk.END, f"  • {item}\n")
        
        # Обновление списка NPC
        self.npc_list.delete(0, tk.END)
        for npc in self.npcs.values():
            if npc.location == self.game_state.current_location and npc.is_alive:
                self.npc_list.insert(tk.END, f"{npc.name} ({npc.profession})")
        
        # Обновление квестов
        self.quest_text.delete(1.0, tk.END)
        for quest in self.quest_system.active_quests:
            self.quest_text.insert(tk.END, f"• {quest['name']}\n")
    
    def move_to_location(self, location_name):
        """Перемещение в локацию"""
        self.game_state.current_location = location_name
        self.world.advance_time(10)
        self.stats["steps_taken"] += 1
        
        loc_display = {
            "town_square": "Городской площади",
            "tavern": "Таверне",
            "market": "Рынке",
            "slums": "Трущобах",
            "temple": "Храме",
            "castle": "Замке"
        }
        
        self.add_text(f"\n📍 Ты на {loc_display.get(location_name, location_name)}.")
        self.update_ui()
    
    def on_npc_select(self, event):
        """Выбор NPC"""
        selection = self.npc_list.curselection()
        if selection:
            npc_text = self.npc_list.get(selection[0])
            npc_name = npc_text.split(" ")[0]
            for npc in self.npcs.values():
                if npc.name == npc_name:
                    self.talk_to_npc(npc)
                    break
    
    def talk_to_npc(self, npc):
        """Разговор с NPC"""
        self.add_text(f"\n--- {npc.name} ---")
        
        greetings = {
            "добрый": f"{npc.name}: 'Рад тебя видеть!'",
            "злой": f"{npc.name}: 'Чего надо?'",
            "хитрый": f"{npc.name}: 'А, клиент...'",
            "честный": f"{npc.name}: 'Здравствуй, путник'",
            "грубый": f"{npc.name}: 'Проваливай, не до тебя'"
        }
        
        self.add_text(greetings.get(npc.personality, f"{npc.name}: '...'"))
        
        if npc.is_merchant:
            self.add_text(f"💰 {npc.name} (торговец): Хочешь купить что-то?")
            # TODO: открыть торговлю
    
    def examine(self):
        """Осмотр локации"""
        self.add_text("\n🔍 Ты внимательно осматриваешься...")
        
        # Шанс найти что-то
        if random.random() < 0.2:
            items = ["монета", "старая книга", "зелье", "ключ"]
            item = random.choice(items)
            
            if item == "монета":
                gold = random.randint(1, 10)
                self.game_state.player["money"] += gold
                self.add_text(f"💰 Ты нашел {gold} монет!")
                self.stats["gold_collected"] += gold
            else:
                self.game_state.player["inventory"]["misc"].append(item)
                self.add_text(f"📦 Ты нашел: {item}")
            
            self.update_ui()
        else:
            self.add_text("Ничего интересного.")
    
    def show_inventory(self):
        """Показать инвентарь"""
        self.add_text("\n📦 ИНВЕНТАРЬ:")
        for category, items in self.game_state.player["inventory"].items():
            if items:
                self.add_text(f"  {category}: {', '.join(items)}")
        self.add_text(f"  💰 монеты: {self.game_state.player['money']}")
    
    def show_map(self):
        """Показать карту"""
        self.add_text("\n🗺️ КАРТА МИРА:")
        self.add_text("  • Площадь (центр города)")
        self.add_text("  • Таверна 'Гнилой Зуб'")
        self.add_text("  • Рынок")
        self.add_text("  • Трущобы")
        self.add_text("  • Храм Единого")
        self.add_text("  • Княжеский замок")
        self.add_text(f"\n📍 Текущая локация: {self.game_state.current_location}")
    
    def show_character(self):
        """Показать характеристики"""
        self.add_text("\n📊 ХАРАКТЕРИСТИКИ:")
        self.add_text(f"  Имя: {self.game_state.player['name']}")
        self.add_text(f"  Уровень: {self.game_state.player['level']}")
        self.add_text(f"  Опыт: {self.game_state.player['exp']}")
        self.add_text(f"  Здоровье: {self.game_state.player['health']}/{self.game_state.player['max_health']}")
        self.add_text(f"  Выносливость: {self.game_state.player['stamina']}/{self.game_state.player['max_stamina']}")
        self.add_text(f"  Мана: {self.game_state.player['mana']}/{self.game_state.player['max_mana']}")
        
        for stat, value in self.game_state.player['stats'].items():
            self.add_text(f"  {stat}: {value}")
    
    def save_game(self):
        """Сохранение игры"""
        success, message = SaveSystem.save_game(
            self.game_state,
            self.world,
            self.market,
            self.quest_system,
            self.stats
        )
        
        if success:
            self.add_text(f"\n💾 {message}")
        else:
            self.add_text(f"\n❌ Ошибка сохранения: {message}")
    
    def load_game(self):
        """Загрузка игры"""
        saves = SaveSystem.get_saves()
        
        if not saves:
            self.add_text("\n❌ Нет сохранений!")
            return
        
        # последнее сохранение
        success, data = SaveSystem.load_game(saves[0])
        
        if success:
            # Восстановка состояния
            self.game_state = GameState.from_dict(data["game_state"])
            self.world = data["world"]
            # Восстанова объекта из словарей
            if hasattr(self.world, '__dict__'):
                for key, value in data["world"].items():
                    setattr(self.world, key, value)
            
            self.market = MarketSystem()
            if hasattr(self.market, '__dict__'):
                for key, value in data["market"].items():
                    setattr(self.market, key, value)
            
            self.quest_system = QuestSystem.from_dict(data["quest_system"])
            self.stats = data["stats"]
            
            self.add_text(f"\n✅ Загружено: {saves[0]}")
            self.update_ui()
        else:
            self.add_text(f"\n❌ Ошибка загрузки: {data}")
    
    def show_intro(self):
        """Вступление"""
        intro = """
╔══════════════════════════════════════════════════════════╗
║     THE LIFE AND SUFFERING OF PRINCE JERIAN              ║
║                    КРОВЬ И ПЕПЕЛ                         ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   Ты - Джериан, проклятый с рождения.                    ║
║   Тьма внутри тебя растет с каждым днем.                 ║
║                                                          ║
║   Сможешь ли ты победить демона внутри себя?             ║
║   Или станешь величайшим злом этого мира?                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        self.add_text(intro)
        self.add_text("\nНажми на любую кнопку локации чтобы начать...")
    
    def run(self):
        """Запуск"""
        self.root.mainloop()