import tkinter as tk
from tkinter import ttk
import math

class MapScreen:
    """Экран карты"""
    def __init__(self, parent, world, current_location):
        self.parent = parent
        self.world = world
        self.current_location = current_location
        self.window = None
        
        # Координаты локаций
        self.locations_coords = {
            "town_square": (300, 200),
            "tavern": (250, 250),
            "market": (350, 200),
            "slums": (200, 300),
            "temple": (300, 150),
            "castle": (400, 150),
            "port": (450, 250),
            "forest": (200, 100),
            "cemetery": (150, 200),
            "dungeon": (100, 250),
            "wizard_tower": (400, 100),
            "blacksmith": (300, 250),
            "guild": (250, 200),
            "brothel": (300, 300),
            "prison": (350, 300),
            "palace": (400, 200)
        }
        
    def show(self):
        """Показать карту"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Карта мира")
        self.window.geometry("800x600")
        self.window.configure(bg='#0a0a0a')
        
        # canvas для карты
        self.canvas = tk.Canvas(self.window, bg='#1a2a1a', width=700, height=500)
        self.canvas.pack(pady=10)
        
        # отрисовка карты
        self.draw_map()
        
        # Информация
        info_frame = tk.Frame(self.window, bg='#1a1a1a')
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(info_frame, text=f"День {self.world.day}, {self.world.season}", 
                bg='#1a1a1a', fg='white').pack()
        tk.Label(info_frame, text=f"Погода: {self.world.weather}", 
                bg='#1a1a1a', fg='#87ceeb').pack()
        
        # Кнопка закрытия
        tk.Button(self.window, text="Закрыть", bg='#333', fg='white',
                 command=self.window.destroy).pack(pady=5)
    
    def draw_map(self):
        """Рисование карты"""
        # дороги
        self.canvas.create_line(200, 200, 400, 200, fill='#8b4513', width=3, dash=(5, 3))
        self.canvas.create_line(300, 150, 300, 300, fill='#8b4513', width=3, dash=(5, 3))
        self.canvas.create_line(250, 250, 350, 250, fill='#8b4513', width=3, dash=(5, 3))
        
        # отрисовка лок
        for loc_name, (x, y) in self.locations_coords.items():
            # определение цвета
            if loc_name == self.current_location:
                color = 'gold'
                outline = 'red'
                width = 3
            else:
                color = self.get_location_color(loc_name)
                outline = 'black'
                width = 1
            
            # точка
            self.canvas.create_oval(x-10, y-10, x+10, y+10, 
                                   fill=color, outline=outline, width=width)
            
            # название
            display_name = loc_name.replace('_', ' ').title()
            self.canvas.create_text(x, y-20, text=display_name, 
                                   fill='white', font=('Arial', 8))
    
    def get_location_color(self, loc_name):
        """Цвет локации"""
        colors = {
            "town_square": '#cd853f',
            "tavern": '#8b4513',
            "market": '#daa520',
            "slums": '#696969',
            "temple": '#ffffff',
            "castle": '#c0c0c0',
            "port": '#4682b4',
            "forest": '#228b22',
            "cemetery": '#2f4f4f',
            "dungeon": '#4a4a4a',
            "wizard_tower": '#9370db',
            "blacksmith": '#b22222',
            "guild": '#8b008b',
            "brothel": '#ff69b4',
            "prison": '#556b2f',
            "palace": '#ffd700'
        }
        return colors.get(loc_name, '#ffffff')