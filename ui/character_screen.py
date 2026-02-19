import tkinter as tk
from tkinter import ttk

class CharacterScreen:
    """Экран персонажа"""
    def __init__(self, parent, player):
        self.parent = parent
        self.player = player
        self.window = None
        
    def show(self):
        """Показать окно персонажа"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Характеристики персонажа")
        self.window.geometry("600x500")
        self.window.configure(bg='#0a0a0a')
        
        # Имя и уровень
        name_frame = tk.Frame(self.window, bg='#1a1a1a')
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(name_frame, text=self.player.name, 
                bg='#1a1a1a', fg='gold', font=('Arial', 16, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(name_frame, text=f"Уровень {self.player.level}", 
                bg='#1a1a1a', fg='#00ff00', font=('Arial', 14)).pack(side=tk.RIGHT, padx=10)
        
        # Основные характеристики
        stats_frame = tk.LabelFrame(self.window, text="Характеристики", 
                                    bg='#1a1a1a', fg='white', font=('Arial', 12))
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        stats = [
            ("Сила", self.player.stats["strength"]),
            ("Ловкость", self.player.stats["dexterity"]),
            ("Интеллект", self.player.stats["intelligence"]),
            ("Мудрость", self.player.stats["wisdom"]),
            ("Харизма", self.player.stats["charisma"]),
            ("Удача", self.player.stats["luck"])
        ]
        
        for i, (name, value) in enumerate(stats):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(stats_frame, bg='#1a1a1a')
            frame.grid(row=row, column=col, sticky='w', padx=20, pady=5)
            
            tk.Label(frame, text=f"{name}:", bg='#1a1a1a', fg='#87ceeb', width=12, anchor='w').pack(side=tk.LEFT)
            tk.Label(frame, text=str(value), bg='#1a1a1a', fg='white', width=5).pack(side=tk.LEFT)
        
        # Здоровье и мана
        resources_frame = tk.Frame(self.window, bg='#1a1a1a')
        resources_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Здоровье
        health_frame = tk.Frame(resources_frame, bg='#1a1a1a')
        health_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(health_frame, text="Здоровье:", bg='#1a1a1a', fg='#ff4444', width=12, anchor='w').pack(side=tk.LEFT)
        
        health_bar = tk.Canvas(health_frame, bg='#333', height=20, width=200)
        health_bar.pack(side=tk.LEFT, padx=5)
        
        health_percent = self.player.health / self.player.max_health
        health_bar.create_rectangle(0, 0, 200 * health_percent, 20, fill='#ff4444', width=0)
        
        tk.Label(health_frame, text=f"{self.player.health}/{self.player.max_health}", 
                bg='#1a1a1a', fg='white').pack(side=tk.LEFT)
        
        # Мана
        mana_frame = tk.Frame(resources_frame, bg='#1a1a1a')
        mana_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(mana_frame, text="Мана:", bg='#1a1a1a', fg='#4444ff', width=12, anchor='w').pack(side=tk.LEFT)
        
        mana_bar = tk.Canvas(mana_frame, bg='#333', height=20, width=200)
        mana_bar.pack(side=tk.LEFT, padx=5)
        
        mana_percent = self.player.mana / self.player.max_mana
        mana_bar.create_rectangle(0, 0, 200 * mana_percent, 20, fill='#4444ff', width=0)
        
        tk.Label(mana_frame, text=f"{self.player.mana}/{self.player.max_mana}", 
                bg='#1a1a1a', fg='white').pack(side=tk.LEFT)
        
        # Навыки
        skills_frame = tk.LabelFrame(self.window, text="Навыки", 
                                     bg='#1a1a1a', fg='white', font=('Arial', 12))
        skills_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Список навыков
        skills_list = tk.Text(skills_frame, bg='#2a2a2a', fg='#00ff00', height=10)
        skills_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for skill, value in self.player.skills.items():
            skills_list.insert(tk.END, f"{skill}: {value}\n")
        
        # Кнопка закрытия
        tk.Button(self.window, text="Закрыть", bg='#333', fg='white',
                 command=self.window.destroy).pack(pady=10)