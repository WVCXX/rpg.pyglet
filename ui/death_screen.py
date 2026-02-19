import tkinter as tk

class DeathScreen:
    """Экран смерти"""
    def __init__(self, parent, stats, callback):
        self.parent = parent
        self.stats = stats
        self.callback = callback
        self.window = None
        
    def show(self, death_reason=""):
        """Показать экран смерти"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("ТЫ УМЕР")
        self.window.geometry("500x400")
        self.window.configure(bg='#0a0a0a')
        
        # Заголовок
        tk.Label(self.window, text="⚰️ ТЫ УМЕР ⚰️", 
                bg='#0a0a0a', fg='red', font=('Arial', 24, 'bold')).pack(pady=20)
        
        # Причина смерти
        if death_reason:
            tk.Label(self.window, text=death_reason, 
                    bg='#0a0a0a', fg='#ff4444', font=('Arial', 14)).pack(pady=10)
        
        # Статистика
        stats_frame = tk.Frame(self.window, bg='#1a1a1a')
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        stats_list = [
            f"Дней прожито: {self.stats.get('days', 0)}",
            f"Врагов убито: {self.stats.get('enemies_killed', 0)}",
            f"Квестов выполнено: {self.stats.get('quests_completed', 0)}",
            f"Золота собрано: {self.stats.get('gold_collected', 0)}",
            f"Смертей: {self.stats.get('deaths', 1)}"
        ]
        
        for stat in stats_list:
            tk.Label(stats_frame, text=stat, bg='#1a1a1a', fg='white', 
                    font=('Arial', 12)).pack(anchor='w', padx=10, pady=2)
        
        # Кнопки
        button_frame = tk.Frame(self.window, bg='#0a0a0a')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Загрузить игру", bg='#333', fg='white',
                 width=15, command=self.load_game).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Новая игра", bg='#333', fg='white',
                 width=15, command=self.new_game).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Выход", bg='#333', fg='white',
                 width=15, command=self.quit_game).pack(side=tk.LEFT, padx=5)
    
    def load_game(self):
        """Загрузить игру"""
        self.window.destroy()
        if self.callback:
            self.callback("load")
    
    def new_game(self):
        """Новая игра"""
        self.window.destroy()
        if self.callback:
            self.callback("new")
    
    def quit_game(self):
        """Выход"""
        self.window.destroy()
        self.parent.quit()