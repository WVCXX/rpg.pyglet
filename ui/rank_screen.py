import tkinter as tk
from tkinter import ttk

class RankScreen:
    """Экран рангов и титулов"""
    
    def __init__(self, parent, rank_system, game_window):
        self.parent = parent
        self.rank_system = rank_system
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
            'fg_white': '#ffffff',
            'fg_gray': '#888888'
        }
    
    def show(self):
        """Показать окно рангов"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Ранги и титулы")
        self.window.geometry("800x600")
        self.window.configure(bg=self.colors['bg_dark'])
        self.window.transient(self.parent)
        
        # Заголовок
        title = tk.Label(self.window, text="🏆 РАНГИ И ТИТУЛЫ 🏆",
                        bg=self.colors['bg_dark'],
                        fg=self.colors['fg_gold'],
                        font=('Cinzel', 18, 'bold'))
        title.pack(pady=20)
        
        # Основной контейнер
        main_frame = tk.Frame(self.window, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Левая панель - текущий ранг
        left_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'],
                              relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.create_rank_panel(left_frame)
        
        # Правая панель - титулы
        right_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'],
                               relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.create_titles_panel(right_frame)
        
        # Кнопка закрытия
        tk.Button(self.window, text="Закрыть",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=self.window.destroy,
                 font=('Arial', 12)).pack(pady=10)
    
    def create_rank_panel(self, parent):
        """Создание панели ранга"""
        rank_info = self.rank_system.get_rank_info()
        
        # Текущий ранг
        rank_label = tk.Label(parent, text="ТЕКУЩИЙ РАНГ",
                              bg=self.colors['bg_medium'],
                              fg=self.colors['fg_gold'],
                              font=('Arial', 14, 'bold'))
        rank_label.pack(pady=10)
        
        current_rank = tk.Label(parent, text=rank_info["current_rank"],
                                bg=self.colors['bg_medium'],
                                fg=rank_info["current_color"],
                                font=('Arial', 24, 'bold'))
        current_rank.pack(pady=5)
        
        # Очки ранга
        points_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        points_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(points_frame, text="Очки ранга:",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_white']).pack(side=tk.LEFT)
        
        tk.Label(points_frame, text=str(rank_info["rank_points"]),
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_green'],
                font=('Arial', 12, 'bold')).pack(side=tk.RIGHT)
        
        # Следующий ранг
        if rank_info["next_rank"]:
            next_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
            next_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(next_frame, text="Следующий:",
                    bg=self.colors['bg_medium'],
                    fg=self.colors['fg_white']).pack(side=tk.LEFT)
            
            tk.Label(next_frame, text=rank_info["next_rank"],
                    bg=self.colors['bg_medium'],
                    fg=self.colors['fg_gold']).pack(side=tk.RIGHT)
            
            # Прогресс
            progress_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
            progress_frame.pack(fill=tk.X, padx=20, pady=10)
            
            progress = rank_info["progress"]
            progress_bar = tk.Canvas(progress_frame, bg='#333', height=20, width=300)
            progress_bar.pack()
            progress_bar.create_rectangle(0, 0, 300 * progress/100, 20,
                                         fill=self.colors['fg_green'], width=0)
            progress_bar.create_text(150, 10, text=f"{progress:.1f}%",
                                    fill='white', font=('Arial', 8))
            
            # Очков до следующего
            tk.Label(parent, text=f"Нужно еще: {rank_info['points_needed']}",
                    bg=self.colors['bg_medium'],
                    fg=self.colors['fg_red']).pack()
        
        # Список всех рангов
        ranks_label = tk.Label(parent, text="\nВСЕ РАНГИ",
                               bg=self.colors['bg_medium'],
                               fg=self.colors['fg_gold'],
                               font=('Arial', 12, 'bold'))
        ranks_label.pack(pady=10)
        
        ranks_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        ranks_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        canvas = tk.Canvas(ranks_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = tk.Scrollbar(ranks_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for rank in self.rank_system.RANKS:
            frame = tk.Frame(scrollable_frame, bg=rank["color"],
                            relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=2)
            
            name_label = tk.Label(frame, text=rank["name"],
                                  bg=rank["color"],
                                  fg='black' if rank["color"] != "#000000" else 'white',
                                  font=('Arial', 10, 'bold'),
                                  width=15, anchor='w')
            name_label.pack(side=tk.LEFT, padx=5)
            
            points_label = tk.Label(frame, text=f"{rank['points']} очков",
                                    bg=rank["color"],
                                    fg='black',
                                    font=('Arial', 9))
            points_label.pack(side=tk.RIGHT, padx=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_titles_panel(self, parent):
        """Создание панели титулов"""
        titles_label = tk.Label(parent, text="ДОСТУПНЫЕ ТИТУЛЫ",
                                bg=self.colors['bg_medium'],
                                fg=self.colors['fg_gold'],
                                font=('Arial', 14, 'bold'))
        titles_label.pack(pady=10)
        
        # Текущий титул
        current_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        current_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(current_frame, text="Текущий:",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_white']).pack(side=tk.LEFT)
        
        current_title = self.rank_system.current_title
        current_color = "#ffffff"
        for title in self.rank_system.get_available_titles():
            if title["name"] == current_title:
                current_color = title["color"]
                break
        
        tk.Label(current_frame, text=current_title,
                bg=self.colors['bg_medium'],
                fg=current_color,
                font=('Arial', 12, 'bold')).pack(side=tk.RIGHT)
        
        # Список титулов
        titles_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        titles_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(titles_frame, bg=self.colors['bg_medium'], highlightthickness=0)
        scrollbar = tk.Scrollbar(titles_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_medium'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for title in self.rank_system.get_available_titles():
            frame = tk.Frame(scrollable_frame, bg=self.colors['bg_light'],
                            relief=tk.RAISED if title["unlocked"] else tk.SUNKEN,
                            bd=2)
            frame.pack(fill=tk.X, pady=2)
            
            # Название
            name_label = tk.Label(frame, text=title["name"],
                                  bg=self.colors['bg_light'],
                                  fg=title["color"] if title["unlocked"] else self.colors['fg_gray'],
                                  font=('Arial', 11, 'bold'),
                                  anchor='w')
            name_label.pack(anchor='w', padx=5, pady=2)
            
            # Описание
            desc_label = tk.Label(frame, text=title["description"],
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['fg_white'] if title["unlocked"] else self.colors['fg_gray'],
                                  font=('Arial', 8),
                                  wraplength=300,
                                  justify=tk.LEFT)
            desc_label.pack(anchor='w', padx=10, pady=1)
            
            # Статус
            if title["unlocked"]:
                status_label = tk.Label(frame, text="✅ ПОЛУЧЕН",
                                        bg=self.colors['bg_light'],
                                        fg=self.colors['fg_green'],
                                        font=('Arial', 8))
                status_label.pack(anchor='e', padx=5, pady=1)
                
                # Кнопка выбора
                if title["name"] != self.rank_system.current_title:
                    tk.Button(frame, text="Выбрать",
                             bg=self.colors['bg_medium'],
                             fg=self.colors['fg_white'],
                             command=lambda t=title["id"]: self.select_title(t),
                             font=('Arial', 8)).pack(anchor='e', padx=5, pady=2)
            else:
                status_label = tk.Label(frame, text="🔒 НЕ ПОЛУЧЕН",
                                        bg=self.colors['bg_light'],
                                        fg=self.colors['fg_red'],
                                        font=('Arial', 8))
                status_label.pack(anchor='e', padx=5, pady=1)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def select_title(self, title_id: str):
        """Выбор титула"""
        if self.rank_system.set_current_title(title_id):
            # Обновляем окно
            self.window.destroy()
            self.show()
            
            # Обновляем интерфейс игры
            self.game.update_ui()