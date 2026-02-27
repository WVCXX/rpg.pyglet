import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime

class SaveLoadScreen:
    """Экран сохранения и загрузки"""
    def __init__(self, parent, game_window):
        self.parent = parent
        self.game_window = game_window
        self.window = None
        self.saves_listbox = None
        
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
        """Показать окно сохранений"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Сохранения")
        self.window.geometry("600x500")
        self.window.configure(bg=self.colors['bg_dark'])
        
        # заголовок
        title_frame = tk.Frame(self.window, bg=self.colors['bg_medium'])
        title_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(title_frame, text="💾 СОХРАНЕНИЯ",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_gold'],
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        # основная область
        main_frame = tk.Frame(self.window, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # список сохранений
        list_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(list_frame, text="Доступные сохранения:",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_white']).pack(anchor='w', padx=5, pady=5)
        
        # создаем listbox с прокруткой
        list_container = tk.Frame(list_frame, bg=self.colors['bg_light'])
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.saves_listbox = tk.Listbox(list_container,
                                        bg=self.colors['bg_light'],
                                        fg=self.colors['fg_green'],
                                        selectbackground=self.colors['fg_blue'],
                                        font=('Courier', 10),
                                        yscrollcommand=scrollbar.set)
        self.saves_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.saves_listbox.yview)
        
        # загружаем список сохранений
        self.refresh_saves_list()
        
        # информационная панель
        info_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'])
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_label = tk.Label(info_frame,
                                   text="Выберите сохранение для загрузки или удаления",
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['fg_gray'],
                                   wraplength=500)
        self.info_label.pack(pady=5)
        
        # кнопки действий
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        button_frame.pack(fill=tk.X, pady=10)
        
        buttons = [
            ("📂 Загрузить", self.load_selected, self.colors['fg_green']),
            ("💾 Сохранить как", self.save_as, self.colors['fg_blue']),
            ("🗑 Удалить", self.delete_selected, self.colors['fg_red']),
            ("❌ Закрыть", self.window.destroy, self.colors['fg_gray'])
        ]
        
        for text, cmd, color in buttons:
            btn = tk.Button(button_frame, text=text,
                           bg=self.colors['bg_light'],
                           fg=color,
                           command=cmd,
                           font=('Arial', 11),
                           width=15)
            btn.pack(side=tk.LEFT, padx=5, expand=True)
        
        # привязка двойного клика
        self.saves_listbox.bind('<Double-Button-1>', lambda e: self.load_selected())
    
    def refresh_saves_list(self):
        """Обновление списка сохранений"""
        from core.save_system import SaveSystem
        
        self.saves_listbox.delete(0, tk.END)
        saves = SaveSystem.get_saves()
        
        if not saves:
            self.saves_listbox.insert(tk.END, "--- Нет сохранений ---")
            self.saves_listbox.itemconfig(0, fg=self.colors['fg_gray'])
            return
        
        for save in saves:
            # форматирование строки
            date_str = save['date'].strftime("%d.%m.%Y %H:%M")
            size_kb = save['size'] / 1024
            
            # метаданные
            metadata = save.get('metadata', {})
            level = metadata.get('player_level', '?')
            location = metadata.get('location', '?')
            location_display = self.get_location_name(location)
            
            display = f"{date_str} | Ур.{level} | {location_display} | {size_kb:.1f}KB"
            self.saves_listbox.insert(tk.END, display)
    
    def get_location_name(self, loc_key):
        """Получение названия локации"""
        locations = {
            "городская_площадь": "Площадь",
            "таверна": "Таверна",
            "рынок": "Рынок",
            "трущобы": "Трущобы",
            "храм": "Храм",
            "замок": "Замок",
            "порт": "Порт",
            "лес": "Лес",
            "кладбище": "Кладбище"
        }
        return locations.get(loc_key, loc_key.replace('_', ' ').title())
    
    def load_selected(self):
        """Загрузка выбранного сохранения"""
        selection = self.saves_listbox.curselection()
        if not selection:
            self.show_info("Выберите сохранение для загрузки!", self.colors['fg_red'])
            return
        
        from core.save_system import SaveSystem
        saves = SaveSystem.get_saves()
        
        if not saves:
            return
        
        filename = saves[selection[0]]['filename']
        self.window.destroy()
        self.game_window.perform_load(filename)
    
    def save_as(self):
        """Сохранение с указанием имени"""
        # диалог ввода имени
        dialog = tk.Toplevel(self.window)
        dialog.title("Сохранить как")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Введите имя сохранения:",
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_white']).pack(pady=20)
        
        entry = tk.Entry(dialog, bg=self.colors['bg_light'],
                        fg=self.colors['fg_green'],
                        font=('Arial', 12))
        entry.pack(pady=10, padx=20, fill=tk.X)
        entry.focus()
        
        def do_save():
            name = entry.get().strip()
            if name:
                if not name.endswith('.sav'):
                    name += '.sav'
                dialog.destroy()
                self.window.destroy()
                self.game_window.save_game()
        
        def cancel():
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Сохранить",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_green'],
                 command=do_save).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Отмена",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_red'],
                 command=cancel).pack(side=tk.LEFT, padx=5)
    
    def delete_selected(self):
        """Удаление выбранного сохранения"""
        selection = self.saves_listbox.curselection()
        if not selection:
            self.show_info("Выберите сохранение для удаления!", self.colors['fg_red'])
            return
        
        from core.save_system import SaveSystem
        saves = SaveSystem.get_saves()
        
        if not saves:
            return
        
        filename = saves[selection[0]]['filename']
        
        # подтверждение
        if tk.messagebox.askyesno("Подтверждение",
                                  f"Удалить сохранение {filename}?"):
            if SaveSystem.delete_save(filename):
                self.refresh_saves_list()
                self.show_info("Сохранение удалено", self.colors['fg_green'])
            else:
                self.show_info("Ошибка удаления", self.colors['fg_red'])
    
    def show_info(self, text, color):
        """Показать информационное сообщение"""
        self.info_label.config(text=text, fg=color)