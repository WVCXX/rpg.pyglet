import tkinter as tk
import random  
from typing import Dict, List, Optional, Callable

class DeathScreen:
    """Экран смерти"""
    def __init__(self, parent, stats, callback):
        self.parent = parent
        self.stats = stats
        self.callback = callback
        self.window = None
        
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_blood': '#1a0000',
            'bg_medium': '#2a0000',
            'fg_red': '#ff0000',
            'fg_dark_red': '#8b0000',
            'fg_white': '#ffffff',
            'fg_gray': '#888888',
            'fg_gold': '#ffd700'
        }
    
    def show(self, death_reason=""):
        """Показать экран смерти"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("ТЫ УМЕР")
        self.window.geometry("600x500")
        self.window.configure(bg=self.colors['bg_dark'])
        
        # делаем модальным
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # центральный контейнер
        main_frame = tk.Frame(self.window, bg=self.colors['bg_blood'],
                              relief=tk.RIDGE, bd=2)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # заголовок
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_blood'])
        title_frame.pack(pady=20)
        
        tk.Label(title_frame, text="⚰️ ТЫ УМЕР ⚰️",
                bg=self.colors['bg_blood'],
                fg=self.colors['fg_red'],
                font=('Cinzel', 24, 'bold')).pack()
        
        # причина смерти
        if death_reason:
            reason_label = tk.Label(main_frame,
                                    text=death_reason,
                                    bg=self.colors['bg_blood'],
                                    fg=self.colors['fg_white'],
                                    font=('Arial', 14, 'italic'),
                                    wraplength=500)
            reason_label.pack(pady=10)
        
        # эпитафия
        epitaphs = [
            "Здесь покоится тот, кто слишком много на себя взял...",
            "Смерть - это только начало",
            "Он жил быстро, умер молодым",
            "Его приключения подошли к концу",
            "Он пал в бою, как настоящий герой",
            "Даже боги умирают...",
            "Его история не закончена"
        ]
        
        tk.Label(main_frame,
                text=random.choice(epitaphs),
                bg=self.colors['bg_blood'],
                fg=self.colors['fg_gray'],
                font=('Arial', 12)).pack(pady=5)
        
        # статистика
        stats_frame = tk.Frame(main_frame, bg='#1a0000',
                               relief=tk.SUNKEN, bd=1)
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        stats_title = tk.Label(stats_frame,
                              text="📊 СТАТИСТИКА ЖИЗНИ",
                              bg='#1a0000',
                              fg=self.colors['fg_gold'],
                              font=('Arial', 14, 'bold'))
        stats_title.pack(pady=5)
        
        stats_list = [
            ("Дней прожито:", str(self.stats.get('шагов_сделано', 0))),
            ("Врагов убито:", str(self.stats.get('врагов_убито', 0))),
            ("Квестов выполнено:", str(self.stats.get('квестов_выполнено', 0))),
            ("Золота собрано:", str(self.stats.get('золота_собрано', 0))),
            ("Предметов найдено:", str(self.stats.get('предметов_найдено', 0))),
            ("Смертей:", str(self.stats.get('смертей', 1)))
        ]
        
        for label, value in stats_list:
            row = tk.Frame(stats_frame, bg='#1a0000')
            row.pack(fill=tk.X, padx=10, pady=2)
            
            tk.Label(row, text=label,
                    bg='#1a0000',
                    fg=self.colors['fg_white'],
                    font=('Arial', 11),
                    width=20,
                    anchor='w').pack(side=tk.LEFT)
            
            tk.Label(row, text=value,
                    bg='#1a0000',
                    fg=self.colors['fg_red'],
                    font=('Arial', 11, 'bold'),
                    anchor='e').pack(side=tk.RIGHT)
        
        # кнопки
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_blood'])
        button_frame.pack(pady=20)
        
        buttons = [
            ("📂 Загрузить игру", "load", self.colors['fg_white']),
            ("🔄 Новая игра", "new", self.colors['fg_green']),
            ("❌ Выход", "quit", self.colors['fg_red'])
        ]
        
        for text, action, color in buttons:
            btn = tk.Button(button_frame, text=text,
                           bg='#2a0000',
                           fg=color,
                           command=lambda a=action: self.handle_action(a),
                           font=('Arial', 12),
                           width=20,
                           relief=tk.RAISED)
            btn.pack(pady=5)
    
    def handle_action(self, action):
        """Обработка выбора действия"""
        self.window.destroy()
        if self.callback:
            self.callback(action)