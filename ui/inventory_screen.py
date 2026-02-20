import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional

class InventoryScreen:

    def create_category_tab(self, notebook, tab_name, category_key):
        """Создание вкладки категории"""
        frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(frame, text=tab_name)
        
        items = self.inventory.get_all_items().get(category_key, [])
        
        if not items:
            empty_frame = tk.Frame(frame, bg=self.colors['bg_light'])
            empty_frame.pack(expand=True)
            tk.Label(empty_frame, text="✨ Пусто",
                    bg=self.colors['bg_light'],
                    fg=self.colors['fg_white'],
                    font=('Arial', 14)).pack()
            return
        
        # создание сетки предметов
        canvas = tk.Canvas(frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # отображение предметов
        row = 0
        col = 0
        max_cols = 3
        
        for item_name, count in items:
            self.create_item_widget(scrollable_frame, category_key, item_name, count, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_item_widget(self, parent, category, item_name, count, row, col):
        """Создание виджета предмета"""
        frame = tk.Frame(parent, bg=self.colors['bg_medium'],
                        relief=tk.RAISED, bd=1)
        frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        icon_label = tk.Label(frame, text="📦",
                              bg=self.colors['bg_medium'],
                              fg=self.colors['fg_gold'],
                              font=('Arial', 24))
        icon_label.pack(pady=5)
        
        # название
        name_label = tk.Label(frame, text=item_name.replace('_', ' ').title(),
                             bg=self.colors['bg_medium'],
                             fg=self.colors['fg_white'],
                             font=('Arial', 10, 'bold'))
        name_label.pack()
        
        # количество
        if count > 1:
            count_label = tk.Label(frame, text=f"x{count}",
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['fg_green'],
                                  font=('Arial', 9))
            count_label.pack()
        
        # кнопки действий
        btn_frame = tk.Frame(frame, bg=self.colors['bg_medium'])
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Исп.",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=lambda c=category, i=item_name: self.use_item(c, i),
                 width=3).pack(side=tk.LEFT, padx=1)
        
        tk.Button(btn_frame, text="Выбр.",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=lambda c=category, i=item_name: self.drop_item(c, i),
                 width=3).pack(side=tk.LEFT, padx=1)
    
    def use_item(self, category, item_name):
        """Использование предмета"""
        print(f"Использован {item_name} из категории {category}")
        
    
    def drop_item(self, category, item_name):
        """Выбрасывание предмета"""
        if self.inventory.remove_item(category, item_name, 1):

            self.window.destroy()
            self.show()