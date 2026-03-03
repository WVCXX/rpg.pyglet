import tkinter as tk
from tkinter import ttk, messagebox

class ToolTip:
    """Класс для всплывающих подсказок"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        
    def show_tip(self, event=None):
        "Показать подсказку"
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", "10", "normal"))
        label.pack()
        
    def hide_tip(self, event=None):
        "Скрыть подсказку"
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

class CharacterScreen:
    """Экран характеристик персонажа"""
    def __init__(self, parent, player_data, update_callback=None):
        self.parent = parent
        self.player = player_data
        self.update_callback = update_callback
        self.window = None
        
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
        """Показать окно характеристик"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Характеристики персонажа")
        self.window.geometry("700x800")
        self.window.configure(bg=self.colors['bg_dark'])
        self.window.transient(self.parent)
        
        # Создание интерфейса
        self.create_header()
        self.create_stats_section()
        self.create_skills_section()
        self.create_effects_section()
        
        # Кнопка закрытия
        tk.Button(self.window, text="Закрыть",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=self.window.destroy,
                 font=('Arial', 12)).pack(pady=10)
    
    def create_header(self):
        """Создание заголовка"""
        header = tk.Frame(self.window, bg=self.colors['bg_medium'])
        header.pack(fill=tk.X, padx=10, pady=5)
        
        # Имя и уровень
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
        
        # Опыт
        exp_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        exp_frame.pack(fill=tk.X, pady=5)
        
        exp_needed = self.player['level'] * 100
        exp_percent = min(100, (self.player['exp'] / exp_needed) * 100)
        
        tk.Label(exp_frame, 
                text=f"Опыт: {self.player['exp']}/{exp_needed}",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_white']).pack()
        
        # Полоска опыта
        exp_bar = tk.Canvas(exp_frame, bg='#333', height=10, width=300)
        exp_bar.pack(pady=2)
        exp_bar.create_rectangle(0, 0, 300 * exp_percent/100, 10,
                                fill='#00ff00', width=0)
        
        # Очки навыков
        if self.player.get("stat_points", 0) > 0:
            points_frame = tk.Frame(header, bg=self.colors['bg_medium'])
            points_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(points_frame,
                    text=f"✨ Доступно очков навыков: {self.player['stat_points']}",
                    bg=self.colors['bg_medium'],
                    fg=self.colors['fg_gold'],
                    font=('Arial', 12, 'bold')).pack()
    
    def create_stats_section(self):
        """Создание секции характеристик"""
        stats_frame = tk.LabelFrame(self.window, text="⚔ ХАРАКТЕРИСТИКИ",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_gold'],
                                    font=('Arial', 12, 'bold'))
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        stats = [
            ("сила", "💪", "Влияет на урон в ближнем бою"),
            ("ловкость", "🏃", "Влияет на уклонение и порядок хода"),
            ("интеллект", "🧠", "Влияет на магический урон"),
            ("мудрость", "📚", "Влияет на восстановление маны"),
            ("харизма", "💬", "Влияет на цены и отношения"),
            ("удача", "🍀", "Влияет на шанс критического удара")
        ]
        
        for stat_key, icon, desc in stats:
            self.create_stat_row(stats_frame, stat_key, icon, desc)
    
    def create_stat_row(self, parent, stat_key, icon, description):
        """Создание строки характеристики"""
        frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        frame.pack(fill=tk.X, pady=2, padx=10)
        
        # Иконка и название
        label_frame = tk.Frame(frame, bg=self.colors['bg_medium'], width=150)
        label_frame.pack(side=tk.LEFT, fill=tk.X)
        
        label = tk.Label(label_frame, text=f"{icon} {stat_key.capitalize()}:",
                        bg=self.colors['bg_medium'],
                        fg=self.colors['fg_white'],
                        font=('Arial', 11),
                        anchor='w')
        label.pack(side=tk.LEFT)
        
        # Добавляем всплывающую подсказку
        ToolTip(label, description)
        
        # Значение
        value = self.player["stats"][stat_key]
        value_label = tk.Label(frame, text=str(value),
                              bg=self.colors['bg_medium'],
                              fg=self.colors['fg_green'],
                              font=('Arial', 11, 'bold'),
                              width=3)
        value_label.pack(side=tk.LEFT, padx=5)
        
        # Кнопки увеличения (если есть очки)
        if self.player.get("stat_points", 0) > 0:
            def increase_stat(s=stat_key):
                if self.player["stat_points"] > 0:
                    self.player["stats"][s] += 1
                    self.player["stat_points"] -= 1
                    value_label.config(text=str(self.player["stats"][s]))
                    if self.update_callback:
                        self.update_callback()
                    
                    if self.player["stat_points"] == 0:
                        # Обновить окно
                        self.window.destroy()
                        self.show()
            
            tk.Button(frame, text="+", command=increase_stat,
                     bg=self.colors['bg_light'],
                     fg=self.colors['fg_green'],
                     width=2).pack(side=tk.LEFT, padx=2)
    
    def create_skills_section(self):
        """Создание секции навыков"""
        skills_frame = tk.LabelFrame(self.window, text="📚 НАВЫКИ",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['fg_gold'],
                                     font=('Arial', 12, 'bold'))
        skills_frame.pack(fill=tk.X, padx=10, pady=5)
        
        skills = self.player.get("skills", {})
        if not skills:
            tk.Label(skills_frame, text="Нет изученных навыков",
                    bg=self.colors['bg_medium'],
                    fg=self.colors['fg_gray']).pack(pady=5)
        else:
            for skill, level in skills.items():
                frame = tk.Frame(skills_frame, bg=self.colors['bg_medium'])
                frame.pack(fill=tk.X, pady=2, padx=10)
                
                tk.Label(frame, text=f"• {skill.capitalize()}:",
                        bg=self.colors['bg_medium'],
                        fg=self.colors['fg_white']).pack(side=tk.LEFT)
                
                tk.Label(frame, text=str(level),
                        bg=self.colors['bg_medium'],
                        fg=self.colors['fg_blue']).pack(side=tk.RIGHT)
    
    def create_effects_section(self):
        """Создание секции эффектов"""
        effects_frame = tk.LabelFrame(self.window, text="✨ ЭФФЕКТЫ",
                                      bg=self.colors['bg_medium'],
                                      fg=self.colors['fg_gold'],
                                      font=('Arial', 12, 'bold'))
        effects_frame.pack(fill=tk.X, padx=10, pady=5)
        
        effects = []
        
        # Благословения
        for blessing in self.player.get("blessings", []):
            effects.append(("💚", blessing, self.colors['fg_green']))
        
        # Проклятия
        for curse in self.player.get("curses", []):
            effects.append(("💔", curse, self.colors['fg_red']))
        
        # Болезни
        for disease in self.player.get("diseases", []):
            effects.append(("🤒", disease, self.colors['fg_yellow']))
        
        if not effects:
            tk.Label(effects_frame, text="Нет активных эффектов",
                    bg=self.colors['bg_medium'],
                    fg=self.colors['fg_gray']).pack(pady=5)
        else:
            for icon, text, color in effects:
                frame = tk.Frame(effects_frame, bg=self.colors['bg_medium'])
                frame.pack(fill=tk.X, pady=2, padx=10)
                
                tk.Label(frame, text=f"{icon} {text}",
                        bg=self.colors['bg_medium'],
                        fg=color).pack()