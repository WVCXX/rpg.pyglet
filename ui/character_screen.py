# ui/character_screen.py
import tkinter as tk
from tkinter import ttk

class CharacterScreen:
    """Экран характеристик персонажа"""
    def __init__(self, parent, player_data):
        self.parent = parent
        self.player = player_data
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
        """Показать окно характеристик"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Характеристики персонажа")
        self.window.geometry("700x800")
        self.window.configure(bg=self.colors['bg_dark'])
        
        # создание интерфейса
        self.create_header()
        self.create_stats_section()
        self.create_resources_section()
        self.create_skills_section()
        self.create_effects_section()
        
        # кнопка закрытия
        tk.Button(self.window, text="Закрыть",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=self.window.destroy,
                 font=('Arial', 12)).pack(pady=10)
    
    def create_header(self):
        """Создание заголовка"""
        header = tk.Frame(self.window, bg=self.colors['bg_medium'])
        header.pack(fill=tk.X, padx=10, pady=5)
        
        # имя и уровень
        name_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        name_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(name_frame, text=self.player["name"],
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_gold'],
                font=('Cinzel', 18, 'bold')).pack(side=tk.LEFT, padx=10)
        
        tk.Label(name_frame, text=f"Уровень {self.player['level']}",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_green'],
                font=('Arial', 14)).pack(side=tk.RIGHT, padx=10)
        
        # опыт
        exp_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        exp_frame.pack(fill=tk.X, pady=5)
        
        exp_needed = self.player['level'] * 100
        exp_percent = (self.player['exp'] / exp_needed) * 100
        
        tk.Label(exp_frame, text=f"Опыт: {self.player['exp']}/{exp_needed}",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_white']).pack()
        
        # полоска опыта
        exp_bar = tk.Canvas(exp_frame, bg='#333', height=10, width=300)
        exp_bar.pack(pady=2)
        exp_bar.create_rectangle(0, 0, 300 * (self.player['exp'] / exp_needed), 10,
                                fill='#00ff00', width=0)
    
    def create_stats_section(self):
        """Создание секции характеристик"""
        stats_frame = tk.LabelFrame(self.window, text="⚔ ХАРАКТЕРИСТИКИ",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_gold'],
                                    font=('Arial', 12, 'bold'))
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # основные характеристики
        stats = [
            ("Сила", self.player['stats']["сила"], "💪 Влияет на урон в ближнем бою"),
            ("Ловкость", self.player['stats']["ловкость"], "🏃 Влияет на уклонение и порядок хода"),
            ("Интеллект", self.player['stats']["интеллект"], "🧠 Влияет на магический урон"),
            ("Мудрость", self.player['stats']["мудрость"], "📚 Влияет на восстановление маны"),
            ("Харизма", self.player['stats']["харизма"], "💬 Влияет на цены и отношения"),
            ("Удача", self.player['stats']["удача"], "🍀 Влияет на шанс критического удара")
        ]
        
        for i, (name, value, desc) in enumerate(stats):
            frame = tk.Frame(stats_frame, bg=self.colors['bg_medium'])
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=f"{name}:",)