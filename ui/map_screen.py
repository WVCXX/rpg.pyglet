import tkinter as tk
import math
class MapScreen:
    """Экран карты"""
    
    _instance = None  
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None or not cls._instance.window.winfo_exists():
            cls._instance = super().__new__(cls)
            return cls._instance
        else:
            cls._instance.window.lift()
            cls._instance.window.focus_force()
            return None
    
    def __init__(self, parent, world, current_location, game_window):
        if hasattr(self, 'initialized') and self.initialized:
            return
            
        self.parent = parent
        self.world = world
        self.current_location = current_location
        self.game = game_window
        self.window = None
        self.initialized = True
        
        # цвета
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_map': '#1a2a1a',
            'road': '#8b4513',
            'water': '#4444ff',
            'forest': '#228b22',
            'mountain': '#696969',
            'city': '#ffd700',
            'current': '#ff0000'
        }
        
        # координаты локаций 
        self.locations_coords = {
            "городская_площадь": (400, 300),
            "таверна": (350, 350),
            "рынок": (450, 300),
            "трущобы": (300, 400),
            "храм": (400, 250),
            "замок": (500, 250),
            "порт": (550, 350),
            "лес": (300, 200),
            "кладбище": (250, 300),
            "подземелье": (200, 350),
            "башня_мага": (500, 200),
            "кузница": (400, 350),
            "гильдия": (350, 300),
            "притон": (400, 400),
            "тюрьма": (450, 400),
            "дворец": (500, 300),
            "монастырь": (300, 150),
            "руины": (200, 250),
            "пещеры": (150, 300)
        }
        
        self.show()
    
    def show(self):
        """Показать карту"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Карта мира")
        self.window.geometry("900x700")
        self.window.configure(bg=self.colors['bg_dark'])
        
        # заголовок
        title_frame = tk.Frame(self.window, bg='#1a1a1a')
        title_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(title_frame, text="🗺 КАРТА МИРА",
                bg='#1a1a1a', fg='#ffd700',
                font=('Arial', 16, 'bold')).pack(pady=10)

        map_frame = tk.Frame(self.window, bg=self.colors['bg_dark'])
        map_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.canvas = tk.Canvas(map_frame, bg=self.colors['bg_map'],
                                width=700, height=500)
        self.canvas.pack(expand=True)
        
        # отрисовка карты
        self.draw_map()
        
        self.canvas.bind('<Button-1>', self.on_map_click)
        info_frame = tk.Frame(self.window, bg='#1a1a1a')
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(info_frame,
                text=f"📅 День {self.world.day}, {self.world.season}",
                bg='#1a1a1a', fg='white').pack(side=tk.LEFT, padx=10)
        
        tk.Label(info_frame,
                text=f"🌤 Погода: {self.world.weather}",
                bg='#1a1a1a', fg='#87ceeb').pack(side=tk.LEFT, padx=10)
        
        tk.Label(info_frame,
                text=f"📍 Текущая: {self.get_location_name(self.current_location)}",
                bg='#1a1a1a', fg='#ffd700').pack(side=tk.RIGHT, padx=10)
        
        tk.Button(self.window, text="Закрыть",
                 bg='#333', fg='white',
                 command=self.close_window,
                 font=('Arial', 12)).pack(pady=10)
        
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
    
    def close_window(self):
        """Закрытие окна"""
        MapScreen._instance = None
        self.window.destroy()
    
    def on_map_click(self, event):
        """Обработка клика по карте"""
        x, y = event.x, event.y
        
        closest_loc = None
        min_distance = float('inf')
        
        for loc_name, (loc_x, loc_y) in self.locations_coords.items():
            distance = ((x - loc_x) ** 2 + (y - loc_y) ** 2) ** 0.5
            if distance < 30 and distance < min_distance:
                min_distance = distance
                closest_loc = loc_name
        
        if closest_loc:
            self.game.move_to_location(closest_loc)
            
            self.current_location = closest_loc
            self.canvas.delete("all")
            self.draw_map()
            
            for widget in self.window.winfo_children():
                if isinstance(widget, tk.Frame) and widget.winfo_children():
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label) and "📍" in child.cget("text"):
                            child.config(text=f"📍 Текущая: {self.get_location_name(closest_loc)}")
    
    def draw_map(self):
        """Рисование карты"""
        # дороги
        roads = [
            (400, 300, 350, 350),  # площадь - таверна
            (400, 300, 450, 300),  # площадь - рынок
            (400, 300, 400, 250),  # площадь - храм
            (400, 300, 500, 300),  # площадь - замок
            (400, 300, 300, 400),  # площадь - трущобы
            (500, 300, 550, 350),  # замок - порт
            (300, 400, 250, 300),  # трущобы - кладбище
            (300, 400, 200, 350),  # трущобы - подземелье
            (500, 300, 500, 200),  # замок - башня мага
            (400, 300, 400, 350),  # площадь - кузница
            (350, 300, 400, 300),  # гильдия - площадь
            (300, 200, 400, 250),  # лес - храм
            (300, 150, 400, 250),  # монастырь - храм
            (200, 250, 300, 300),  # руины - гильдия
        ]
        
        for x1, y1, x2, y2 in roads:
            self.canvas.create_line(x1, y1, x2, y2,
                                   fill=self.colors['road'],
                                   width=2, dash=(5, 3))
        
        # река
        self.canvas.create_line(550, 200, 550, 450,
                               fill=self.colors['water'],
                               width=4, smooth=True)
        
        # лес
        for i in range(5):
            x = 250 + i*30
            y = 150
            self.create_tree(x, y)
        
        # горы
        for i in range(3):
            x = 150 + i*40
            y = 350
            self.create_mountain(x, y)
        
        # локации
        for loc_name, (x, y) in self.locations_coords.items():
            # цвет локации
            if loc_name == self.current_location:
                color = self.colors['current']
                outline = 'white'
                width = 3
            else:
                color = self.get_location_color(loc_name)
                outline = 'black'
                width = 1
            
            # маркер
            self.canvas.create_oval(x-12, y-12, x+12, y+12,
                                   fill=color, outline=outline,
                                   width=width, tags=(loc_name,))
            
            # название
            display_name = self.get_location_name(loc_name)
            self.canvas.create_text(x, y-20, text=display_name,
                                   fill='white', font=('Arial', 8, 'bold'))
            
            # легенда
            if loc_name == self.current_location:
                self.canvas.create_text(x, y-35, text="● ВЫ ЗДЕСЬ ●",
                                       fill='yellow', font=('Arial', 7))
    
    def create_tree(self, x, y):
        """Создание дерева"""
        self.canvas.create_polygon(x-10, y+20, x, y-20, x+10, y+20,
                                  fill=self.colors['forest'],
                                  outline='darkgreen')
    
    def create_mountain(self, x, y):
        """Создание горы"""
        self.canvas.create_polygon(x-20, y+20, x, y-30, x+20, y+20,
                                  fill=self.colors['mountain'],
                                  outline='black')
    
    def get_location_color(self, loc_name: str) -> str:
        """Цвет локации"""
        colors = {
            "городская_площадь": '#cd853f',
            "таверна": '#8b4513',
            "рынок": '#daa520',
            "трущобы": '#696969',
            "храм": '#ffffff',
            "замок": '#c0c0c0',
            "порт": '#4682b4',
            "лес": '#228b22',
            "кладбище": '#2f4f4f',
            "подземелье": '#4a4a4a',
            "башня_мага": '#9370db',
            "кузница": '#b22222',
            "гильдия": '#8b008b',
            "притон": '#ff69b4',
            "тюрьма": '#556b2f',
            "дворец": '#ffd700',
            "монастырь": '#98fb98',
            "руины": '#808080',
            "пещеры": '#8b4513'
        }
        return colors.get(loc_name, '#ffffff')
    
    def get_location_name(self, loc_name: str) -> str:
        """Русское название локации"""
        names = {
            "городская_площадь": "Городская площадь",
            "таверна": "Таверна",
            "рынок": "Рынок",
            "трущобы": "Трущобы",
            "храм": "Храм",
            "замок": "Замок",
            "порт": "Порт",
            "лес": "Лес",
            "кладбище": "Кладбище",
            "подземелье": "Подземелье",
            "башня_мага": "Башня Мага",
            "кузница": "Кузница",
            "гильдия": "Гильдия",
            "притон": "Притон",
            "тюрьма": "Тюрьма",
            "дворец": "Дворец",
            "монастырь": "Монастырь",
            "руины": "Руины",
            "пещеры": "Пещеры"
        }
        return names.get(loc_name, loc_name.replace('_', ' ').title())