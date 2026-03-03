import tkinter as tk
from tkinter import ttk, scrolledtext

class JournalScreen:
    """Экран дневника приключений"""
    
    def __init__(self, parent, journal_system, game_window):
        self.parent = parent
        self.journal = journal_system
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
        """Показать окно дневника"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Дневник приключений")
        self.window.geometry("900x700")
        self.window.configure(bg=self.colors['bg_dark'])
        self.window.transient(self.parent)
        
        # Заголовок
        title = tk.Label(self.window, text="📖 ДНЕВНИК ПРИКЛЮЧЕНИЙ 📖",
                        bg=self.colors['bg_dark'],
                        fg=self.colors['fg_gold'],
                        font=('Cinzel', 18, 'bold'))
        title.pack(pady=20)
        
        # Статистика
        stats = self.journal.get_statistics()
        stats_frame = tk.Frame(self.window, bg=self.colors['bg_medium'],
                               relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        stats_text = f"📜 Квесты: {stats['completed_quests']}/{stats['total_quests']}  |  🗺 Открытий: {stats['total_discoveries']}  |  👾 Врагов: {stats['total_enemies']}  |  📦 Предметов: {stats['unique_items']}"
        stats_label = tk.Label(stats_frame, text=stats_text,
                               bg=self.colors['bg_medium'],
                               fg=self.colors['fg_white'],
                               font=('Arial', 10))
        stats_label.pack(pady=10)
        
        # Вкладки
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Вкладка квестов
        self.create_quests_tab(notebook)
        
        # Вкладка открытий
        self.create_discoveries_tab(notebook)
        
        # Вкладка бестиария
        self.create_bestiary_tab(notebook)
        
        # Вкладка коллекции
        self.create_collection_tab(notebook)
        
        # Вкладка заметок
        self.create_notes_tab(notebook)
        
        # Кнопка экспорта
        tk.Button(self.window, text="📤 Экспорт дневника",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_green'],
                 command=self.export_journal,
                 font=('Arial', 10)).pack(pady=5)
        
        # Кнопка закрытия
        tk.Button(self.window, text="Закрыть",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=self.window.destroy,
                 font=('Arial', 12)).pack(pady=10)
    
    def create_quests_tab(self, notebook):
        """Создание вкладки квестов"""
        frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(frame, text="📜 Квесты")
        
        # Активные квесты
        active_label = tk.Label(frame, text="АКТИВНЫЕ КВЕСТЫ",
                                bg=self.colors['bg_light'],
                                fg=self.colors['fg_green'],
                                font=('Arial', 12, 'bold'))
        active_label.pack(pady=5)
        
        active_frame = tk.Frame(frame, bg=self.colors['bg_light'],
                                relief=tk.SUNKEN, bd=1)
        active_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        active_text = scrolledtext.ScrolledText(active_frame,
                                                wrap=tk.WORD,
                                                bg='#000000',
                                                fg=self.colors['fg_green'],
                                                font=('Consolas', 10),
                                                height=8)
        active_text.pack(fill=tk.BOTH, expand=True)
        
        for quest in self.journal.get_quests_by_status("активен"):
            active_text.insert(tk.END, f"⚔ {quest['name']}\n")
            active_text.insert(tk.END, f"   {quest['description']}\n")
            active_text.insert(tk.END, f"   [{quest['date']}]\n\n")
        
        active_text.config(state=tk.DISABLED)
        
        # Завершенные квесты
        completed_label = tk.Label(frame, text="ЗАВЕРШЕННЫЕ КВЕСТЫ",
                                   bg=self.colors['bg_light'],
                                   fg=self.colors['fg_gray'],
                                   font=('Arial', 12, 'bold'))
        completed_label.pack(pady=5)
        
        completed_frame = tk.Frame(frame, bg=self.colors['bg_light'],
                                   relief=tk.SUNKEN, bd=1)
        completed_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        completed_text = scrolledtext.ScrolledText(completed_frame,
                                                   wrap=tk.WORD,
                                                   bg='#000000',
                                                   fg=self.colors['fg_gray'],
                                                   font=('Consolas', 10),
                                                   height=8)
        completed_text.pack(fill=tk.BOTH, expand=True)
        
        for quest in self.journal.get_quests_by_status("завершен"):
            completed_text.insert(tk.END, f"✅ {quest['name']}\n")
            completed_text.insert(tk.END, f"   {quest['description']}\n")
            completed_text.insert(tk.END, f"   [{quest['date']}]\n\n")
        
        completed_text.config(state=tk.DISABLED)
    
    def create_discoveries_tab(self, notebook):
        """Создание вкладки открытий"""
        frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(frame, text="🗺 Открытия")
        
        discoveries = self.journal.get_discoveries_by_location()
        
        canvas = tk.Canvas(frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for location, loc_discoveries in discoveries.items():
            loc_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_medium'],
                                 relief=tk.RAISED, bd=2)
            loc_frame.pack(fill=tk.X, pady=5, padx=5)
            
            loc_name = tk.Label(loc_frame, text=f"📍 {location.replace('_', ' ').title()}",
                                bg=self.colors['bg_medium'],
                                fg=self.colors['fg_gold'],
                                font=('Arial', 11, 'bold'))
            loc_name.pack(anchor='w', padx=5, pady=2)
            
            for disc in loc_discoveries:
                disc_frame = tk.Frame(loc_frame, bg=self.colors['bg_medium'])
                disc_frame.pack(fill=tk.X, padx=10, pady=1)
                
                disc_text = tk.Label(disc_frame, text=f"• {disc['description']} [{disc['date']}]",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['fg_white'],
                                     font=('Arial', 9),
                                     anchor='w')
                disc_text.pack(anchor='w')
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_bestiary_tab(self, notebook):
        """Создание вкладки бестиария"""
        frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(frame, text="👾 Бестиарий")
        
        enemies = self.journal.get_enemy_stats()
        
        # Сортировка
        enemies.sort(key=lambda x: x["count"], reverse=True)
        
        canvas = tk.Canvas(frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        total = sum(e["count"] for e in enemies)
        
        total_label = tk.Label(scrollable_frame, text=f"Всего убито врагов: {total}",
                               bg=self.colors['bg_light'],
                               fg=self.colors['fg_gold'],
                               font=('Arial', 12, 'bold'))
        total_label.pack(pady=10)
        
        for enemy in enemies:
            frame = tk.Frame(scrollable_frame, bg=self.colors['bg_medium'],
                            relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, pady=2, padx=5)
            
            name_label = tk.Label(frame, text=enemy["name"],
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['fg_red'],
                                  font=('Arial', 11, 'bold'),
                                  width=20, anchor='w')
            name_label.pack(side=tk.LEFT, padx=5)
            
            count_label = tk.Label(frame, text=f"x{enemy['count']}",
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['fg_green'],
                                   font=('Arial', 11))
            count_label.pack(side=tk.RIGHT, padx=5)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_collection_tab(self, notebook):
        """Создание вкладки коллекции"""
        frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(frame, text="📦 Коллекция")
        
        items = self.journal.journal["items_found"]
        
        # Группировка по категориям
        categories = {}
        for item in items:
            cat = item["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        canvas = tk.Canvas(frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        cat_names = {
            "weapons": "⚔ Оружие",
            "armor": "🛡 Броня",
            "potions": "🧪 Зелья",
            "books": "📚 Книги",
            "ingredients": "🌿 Ингредиенты",
            "keys": "🔑 Ключи",
            "misc": "📦 Разное"
        }
        
        for cat, cat_items in categories.items():
            cat_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_medium'],
                                 relief=tk.RAISED, bd=2)
            cat_frame.pack(fill=tk.X, pady=5, padx=5)
            
            cat_name = cat_names.get(cat, cat.capitalize())
            cat_label = tk.Label(cat_frame, text=cat_name,
                                 bg=self.colors['bg_medium'],
                                 fg=self.colors['fg_gold'],
                                 font=('Arial', 11, 'bold'))
            cat_label.pack(anchor='w', padx=5, pady=2)
            
            for item in cat_items:
                item_frame = tk.Frame(cat_frame, bg=self.colors['bg_medium'])
                item_frame.pack(fill=tk.X, padx=10, pady=1)
                
                item_name = item["name"].replace('_', ' ').title()
                item_text = tk.Label(item_frame, text=f"• {item_name} [{item['date']}]",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['fg_white'],
                                     font=('Arial', 9),
                                     anchor='w')
                item_text.pack(anchor='w')
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_notes_tab(self, notebook):
        """Создание вкладки заметок"""
        frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(frame, text="📝 Заметки")
        
        # Панель поиска
        search_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(search_frame, text="Поиск:",
                bg=self.colors['bg_light'],
                fg=self.colors['fg_white']).pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(search_frame, bg=self.colors['bg_medium'],
                               fg=self.colors['fg_green'])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        search_btn = tk.Button(search_frame, text="🔍",
                              bg=self.colors['bg_medium'],
                              fg=self.colors['fg_white'],
                              command=lambda: self.search_notes(search_entry.get()))
        search_btn.pack(side=tk.RIGHT, padx=5)
        
        # Кнопка новой заметки
        tk.Button(frame, text="➕ Новая заметка",
                 bg=self.colors['bg_medium'],
                 fg=self.colors['fg_green'],
                 command=self.new_note,
                 font=('Arial', 10)).pack(pady=5)
        
        # Список заметок
        self.notes_frame = tk.Frame(frame, bg=self.colors['bg_light'])
        self.notes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.refresh_notes()
    
    def refresh_notes(self, notes=None):
        """Обновление списка заметок"""
        # Очистка
        for widget in self.notes_frame.winfo_children():
            widget.destroy()
        
        if notes is None:
            notes = self.journal.journal["notes"]
        
        if not notes:
            empty_label = tk.Label(self.notes_frame, text="Нет заметок",
                                   bg=self.colors['bg_light'],
                                   fg=self.colors['fg_gray'])
            empty_label.pack(expand=True)
            return
        
        # Сортировка по дате (сначала новые)
        notes.sort(key=lambda x: x["date"], reverse=True)
        
        canvas = tk.Canvas(self.notes_frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.notes_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for note in notes:
            frame = tk.Frame(scrollable_frame, bg=self.colors['bg_medium'],
                            relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, pady=2)
            
            # Заголовок
            title_frame = tk.Frame(frame, bg=self.colors['bg_medium'])
            title_frame.pack(fill=tk.X, padx=5, pady=2)
            
            title_label = tk.Label(title_frame, text=note["title"],
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['fg_gold'],
                                   font=('Arial', 10, 'bold'))
            title_label.pack(side=tk.LEFT)
            
            date_label = tk.Label(title_frame, text=f"[{note['date']} {note['time']}]",
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['fg_gray'],
                                  font=('Arial', 8))
            date_label.pack(side=tk.RIGHT)
            
            # Содержание
            content_label = tk.Label(frame, text=note["content"],
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['fg_white'],
                                     font=('Arial', 9),
                                     wraplength=500,
                                     justify=tk.LEFT)
            content_label.pack(anchor='w', padx=10, pady=2)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def search_notes(self, query):
        """Поиск по заметкам"""
        if not query:
            self.refresh_notes()
            return
        
        results = self.journal.search_notes(query)
        self.refresh_notes(results)
    
    def new_note(self):
        """Создание новой заметки"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Новая заметка")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Заголовок:",
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_white']).pack(pady=5)
        
        title_entry = tk.Entry(dialog, bg=self.colors['bg_medium'],
                               fg=self.colors['fg_green'],
                               font=('Arial', 12),
                               width=40)
        title_entry.pack(pady=5)
        
        tk.Label(dialog, text="Содержание:",
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_white']).pack(pady=5)
        
        content_text = tk.Text(dialog, bg=self.colors['bg_medium'],
                               fg=self.colors['fg_green'],
                               font=('Arial', 11),
                               height=10,
                               width=50)
        content_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        def save_note():
            title = title_entry.get().strip()
            content = content_text.get(1.0, tk.END).strip()
            
            if title and content:
                self.journal.add_note(title, content)
                dialog.destroy()
                self.refresh_notes()
        
        btn_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Сохранить",
                 bg=self.colors['bg_medium'],
                 fg=self.colors['fg_green'],
                 command=save_note,
                 width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Отмена",
                 bg=self.colors['bg_medium'],
                 fg=self.colors['fg_red'],
                 command=dialog.destroy,
                 width=15).pack(side=tk.LEFT, padx=5)
    
    def export_journal(self):
        """Экспорт дневника"""
        result = self.journal.export_journal()
        
        # Показываем сообщение
        msg = tk.Toplevel(self.window)
        msg.title("Экспорт")
        msg.geometry("300x150")
        msg.configure(bg=self.colors['bg_dark'])
        msg.transient(self.window)
        
        tk.Label(msg, text="✅ Дневник экспортирован!",
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_green'],
                font=('Arial', 12, 'bold')).pack(pady=20)
        
        tk.Label(msg, text=result,
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_white']).pack()
        
        tk.Button(msg, text="OK",
                 bg=self.colors['bg_medium'],
                 fg=self.colors['fg_white'],
                 command=msg.destroy).pack(pady=10)