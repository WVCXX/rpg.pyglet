import tkinter as tk
from tkinter import ttk, scrolledtext

class HouseScreen:
    """Экран управления домом"""
    
    def __init__(self, parent, house_system, game_window):
        self.parent = parent
        self.house = house_system
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
            'fg_gray': '#888888',
            'wood': '#8b4513',
            'wood_light': '#a0522d'
        }
    
    def show(self):
        """Показать окно дома"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Мой дом")
        self.window.geometry("1000x700")
        self.window.configure(bg=self.colors['bg_dark'])
        self.window.transient(self.parent)
        
        house_info = self.house.get_house_info()
        
        if not house_info["owned"]:
            self.show_no_house()
        else:
            self.show_house(house_info)
    
    def show_no_house(self):
        """Показать информацию об отсутствии дома"""
        # Центральное сообщение
        main_frame = tk.Frame(self.window, bg=self.colors['bg_dark'])
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Иконка
        icon_label = tk.Label(main_frame, text="🏚️",
                               bg=self.colors['bg_dark'],
                               fg=self.colors['fg_gray'],
                               font=('Arial', 72))
        icon_label.pack(pady=50)
        
        # Текст
        tk.Label(main_frame, text="У тебя пока нет дома",
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_white'],
                font=('Arial', 24, 'bold')).pack(pady=20)
        
        tk.Label(main_frame, text="Ты можешь купить дом в любом городе",
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_gray'],
                font=('Arial', 12)).pack()
        
        # Доступные дома
        houses_frame = tk.LabelFrame(main_frame, text="🏠 ДОСТУПНЫЕ ДОМА",
                                     bg=self.colors['bg_medium'],
                                     fg=self.colors['fg_gold'],
                                     font=('Arial', 12, 'bold'))
        houses_frame.pack(pady=30, padx=50, fill=tk.X)
        
        for house_id, house_data in self.house.HOUSE_TYPES.items():
            if house_data["level"] == 1:  # Только начальные дома
                frame = tk.Frame(houses_frame, bg=self.colors['bg_light'],
                                 relief=tk.RAISED, bd=2)
                frame.pack(fill=tk.X, pady=5, padx=10)
                
                # Название
                name_label = tk.Label(frame, text=house_id.replace('_', ' ').title(),
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['fg_gold'],
                                      font=('Arial', 11, 'bold'))
                name_label.pack(anchor='w', padx=5, pady=2)
                
                # Описание
                desc_label = tk.Label(frame, text=house_data["description"],
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['fg_white'],
                                      font=('Arial', 9))
                desc_label.pack(anchor='w', padx=10)
                
                # Характеристики
                stats_frame = tk.Frame(frame, bg=self.colors['bg_light'])
                stats_frame.pack(fill=tk.X, padx=10, pady=2)
                
                tk.Label(stats_frame, text=f"🏠 Комнат: {house_data['rooms']}",
                        bg=self.colors['bg_light'],
                        fg=self.colors['fg_green']).pack(side=tk.LEFT, padx=5)
                
                tk.Label(stats_frame, text=f"📦 Хранилище: {house_data['storage_slots']} слотов",
                        bg=self.colors['bg_light'],
                        fg=self.colors['fg_blue']).pack(side=tk.LEFT, padx=5)
                
                # Цена и кнопка
                price_frame = tk.Frame(frame, bg=self.colors['bg_light'])
                price_frame.pack(fill=tk.X, padx=10, pady=5)
                
                tk.Label(price_frame, text=f"💰 Цена: {house_data['price']} золота",
                        bg=self.colors['bg_light'],
                        fg=self.colors['fg_gold']).pack(side=tk.LEFT)
                
                tk.Button(price_frame, text="Купить",
                         bg=self.colors['bg_medium'],
                         fg=self.colors['fg_green'],
                         command=lambda hid=house_id: self.buy_house(hid),
                         width=10).pack(side=tk.RIGHT)
        
        # Кнопка закрытия
        tk.Button(self.window, text="Закрыть",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=self.window.destroy,
                 font=('Arial', 12)).pack(pady=20)
    
    def show_house(self, house_info):
        """Показать информацию о доме"""
        # Верхняя панель с информацией
        info_frame = tk.Frame(self.window, bg=self.colors['wood'],
                              relief=tk.RAISED, bd=3)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Название дома
        title_frame = tk.Frame(info_frame, bg=self.colors['wood'])
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        house_type = house_info["type"].replace('_', ' ').title()
        tk.Label(title_frame, text=f"🏠 {house_type}",
                bg=self.colors['wood'],
                fg=self.colors['fg_gold'],
                font=('Cinzel', 18, 'bold')).pack(side=tk.LEFT)
        
        tk.Label(title_frame, text=f"Уровень {house_info['level']}",
                bg=self.colors['wood'],
                fg=self.colors['fg_green'],
                font=('Arial', 14)).pack(side=tk.RIGHT)
        
        # Описание
        tk.Label(info_frame, text=house_info["description"],
                bg=self.colors['wood'],
                fg=self.colors['fg_white'],
                font=('Arial', 11)).pack(anchor='w', padx=10, pady=2)
        
        # Характеристики
        stats_frame = tk.Frame(info_frame, bg=self.colors['wood'])
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(stats_frame, text=f"📍 {house_info['location'].replace('_', ' ').title()}",
                bg=self.colors['wood'],
                fg=self.colors['fg_blue']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(stats_frame, text=f"✨ Комфорт: {house_info['comfort']}",
                bg=self.colors['wood'],
                fg=self.colors['fg_green']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(stats_frame, text=f"👑 Престиж: {house_info['prestige']}",
                bg=self.colors['wood'],
                fg=self.colors['fg_gold']).pack(side=tk.LEFT, padx=10)
        
        # Кнопки действий
        action_frame = tk.Frame(info_frame, bg=self.colors['wood'])
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(action_frame, text="💤 Отдохнуть",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_green'],
                 command=self.rest_in_house,
                 width=15).pack(side=tk.LEFT, padx=5)
        
        if house_info["level"] < 5:
            tk.Button(action_frame, text="🔨 Улучшить дом",
                     bg=self.colors['bg_light'],
                     fg=self.colors['fg_blue'],
                     command=self.upgrade_house,
                     width=15).pack(side=tk.LEFT, padx=5)
        
        # Основной контейнер с вкладками
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка интерьера
        self.create_interior_tab(notebook, house_info)
        
        # Вкладка хранилища
        self.create_storage_tab(notebook)
        
        # Вкладка магазина мебели
        self.create_furniture_shop_tab(notebook, house_info)
        
        # Кнопка закрытия
        tk.Button(self.window, text="Закрыть",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_white'],
                 command=self.window.destroy,
                 font=('Arial', 12)).pack(pady=10)
    
    def create_interior_tab(self, notebook, house_info):
        """Создание вкладки интерьера"""
        frame = tk.Frame(notebook, bg=self.colors['wood_light'])
        notebook.add(frame, text="🏠 Интерьер")
        
        # Схема дома
        canvas = tk.Canvas(frame, bg=self.colors['wood'], height=300)
        canvas.pack(fill=tk.X, padx=10, pady=10)
        
        # Рисуем комнаты
        rooms = house_info["level"] * 2
        for i in range(rooms):
            x = 50 + (i % 3) * 200
            y = 50 + (i // 3) * 150
            
            # Комната
            canvas.create_rectangle(x, y, x+150, y+100,
                                   fill=self.colors['wood_light'],
                                   outline=self.colors['fg_gold'],
                                   width=2)
            
            # Номер комнаты
            canvas.create_text(x+75, y+20, text=f"Комната {i+1}",
                              fill='white', font=('Arial', 9))
            
            # Мебель в комнате
            furniture_in_room = [f for f in house_info["furniture_list"] 
                                if len(f) > i % len(house_info["furniture_list"])]
            if furniture_in_room:
                canvas.create_text(x+75, y+50, text=furniture_in_room[0][:10],
                                  fill=self.colors['fg_green'], font=('Arial', 8))
        
        # Список мебели
        furniture_frame = tk.LabelFrame(frame, text="🪑 МЕБЕЛЬ",
                                        bg=self.colors['wood_light'],
                                        fg=self.colors['fg_gold'],
                                        font=('Arial', 12, 'bold'))
        furniture_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if not house_info["furniture_list"]:
            tk.Label(furniture_frame, text="В доме пока нет мебели",
                    bg=self.colors['wood_light'],
                    fg=self.colors['fg_gray']).pack(pady=20)
        else:
            canvas = tk.Canvas(furniture_frame, bg=self.colors['wood_light'], highlightthickness=0)
            scrollbar = tk.Scrollbar(furniture_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['wood_light'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for furniture in house_info["furniture_list"]:
                f_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_medium'],
                                   relief=tk.RAISED, bd=2)
                f_frame.pack(fill=tk.X, pady=2, padx=5)
                
                tk.Label(f_frame, text=f"• {furniture}",
                        bg=self.colors['bg_medium'],
                        fg=self.colors['fg_white'],
                        font=('Arial', 10)).pack(anchor='w', padx=5, pady=2)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_storage_tab(self, notebook):
        """Создание вкладки хранилища"""
        frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(frame, text="📦 Хранилище")
        
        # Инвентарь игрока
        player_frame = tk.LabelFrame(frame, text="🎒 ИНВЕНТАРЬ",
                                     bg=self.colors['bg_light'],
                                     fg=self.colors['fg_gold'])
        player_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_item_list(player_frame, self.house.player["inventory"], "player")
        
        # Хранилище дома
        storage_frame = tk.LabelFrame(frame, text="🏠 ХРАНИЛИЩЕ",
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['fg_gold'])
        storage_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_item_list(storage_frame, self.house.house["storage"], "storage")
    
    def create_item_list(self, parent, inventory, source):
        """Создание списка предметов"""
        items = inventory.get_all_items()
        
        canvas = tk.Canvas(parent, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
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
        
        for cat_key, cat_name in cat_names.items():
            if cat_key in items and items[cat_key]:
                cat_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_medium'])
                cat_frame.pack(fill=tk.X, pady=2)
                
                tk.Label(cat_frame, text=cat_name,
                        bg=self.colors['bg_medium'],
                        fg=self.colors['fg_gold'],
                        font=('Arial', 10, 'bold')).pack(anchor='w', padx=5)
                
                for item_name, count in items[cat_key]:
                    item_frame = tk.Frame(cat_frame, bg=self.colors['bg_medium'])
                    item_frame.pack(fill=tk.X, padx=10)
                    
                    display_name = item_name.replace('_', ' ').title()
                    tk.Label(item_frame, text=f"  • {display_name}",
                            bg=self.colors['bg_medium'],
                            fg=self.colors['fg_white'],
                            width=25, anchor='w').pack(side=tk.LEFT)
                    
                    tk.Label(item_frame, text=f"x{count}",
                            bg=self.colors['bg_medium'],
                            fg=self.colors['fg_green'],
                            width=3).pack(side=tk.LEFT)
                    
                    # Кнопка перемещения
                    if source == "player":
                        tk.Button(item_frame, text="📥 В хранилище",
                                 bg=self.colors['bg_light'],
                                 fg=self.colors['fg_blue'],
                                 command=lambda c=cat_key, i=item_name: self.move_to_storage(c, i),
                                 font=('Arial', 8)).pack(side=tk.RIGHT, padx=2)
                    else:
                        tk.Button(item_frame, text="📤 В инвентарь",
                                 bg=self.colors['bg_light'],
                                 fg=self.colors['fg_green'],
                                 command=lambda c=cat_key, i=item_name: self.take_from_storage(c, i),
                                 font=('Arial', 8)).pack(side=tk.RIGHT, padx=2)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_furniture_shop_tab(self, notebook, house_info):
        """Создание вкладки магазина мебели"""
        frame = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(frame, text="🪑 Магазин мебели")
        
        canvas = tk.Canvas(frame, bg=self.colors['bg_light'], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for furn_id, furn_data in self.house.FURNITURE.items():
            # Проверка уровня дома
            if furn_data["level_req"] > house_info["level"]:
                continue
            
            frame = tk.Frame(scrollable_frame, bg=self.colors['bg_medium'],
                             relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Название
            name_label = tk.Label(frame, text=furn_data["description"],
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['fg_gold'],
                                  font=('Arial', 11, 'bold'))
            name_label.pack(anchor='w', padx=5, pady=2)
            
            # Эффект
            effect_text = "Эффект: " + ", ".join([f"{k}+{v}" for k, v in furn_data["effect"].items()])
            effect_label = tk.Label(frame, text=effect_text,
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['fg_green'],
                                    font=('Arial', 9))
            effect_label.pack(anchor='w', padx=10)
            
            # Цена и кнопка
            price_frame = tk.Frame(frame, bg=self.colors['bg_medium'])
            price_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(price_frame, text=f"💰 Цена: {furn_data['price']} золота",
                    bg=self.colors['bg_medium'],
                    fg=self.colors['fg_gold']).pack(side=tk.LEFT)
            
            # Проверка, есть ли уже такая мебель
            has_it = any(f["id"] == furn_id for f in self.house.house["furniture"])
            if has_it:
                tk.Label(price_frame, text="✅ Уже есть",
                        bg=self.colors['bg_medium'],
                        fg=self.colors['fg_green']).pack(side=tk.RIGHT)
            else:
                tk.Button(price_frame, text="Купить",
                         bg=self.colors['bg_light'],
                         fg=self.colors['fg_green'],
                         command=lambda fid=furn_id: self.buy_furniture(fid),
                         width=10).pack(side=tk.RIGHT)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def buy_house(self, house_type):
        """Покупка дома"""
        # Здесь нужно выбрать локацию
        # Пока берем текущую
        location = self.game.game_state.current_location
        
        result = self.house.buy_house(house_type, location)
        
        if result["success"]:
            self.game.add_text(result["message"], "success")
            self.window.destroy()
            self.show()  # Показываем обновленный интерфейс
        else:
            self.game.add_text(result["message"], "warning")
    
    def upgrade_house(self):
        """Улучшение дома"""
        result = self.house.upgrade_house()
        
        if result["success"]:
            self.game.add_text(result["message"], "success")
            self.window.destroy()
            self.show()
        else:
            self.game.add_text(result["message"], "warning")
    
    def buy_furniture(self, furniture_id):
        """Покупка мебели"""
        result = self.house.buy_furniture(furniture_id)
        
        if result["success"]:
            self.game.add_text(result["message"], "success")
            self.window.destroy()
            self.show()
        else:
            self.game.add_text(result["message"], "warning")
    
    def rest_in_house(self):
        """Отдых в доме"""
        result = self.house.rest()
        self.game.add_text(result["message"], "success")
        self.game.update_ui()
    
    def move_to_storage(self, category, item):
        """Переместить в хранилище"""
        if self.house.move_to_storage(category, item, 1):
            self.game.add_text(f"📦 {item} перемещен в хранилище", "success")
            self.window.destroy()
            self.show()
    
    def take_from_storage(self, category, item):
        """Взять из хранилища"""
        if self.house.take_from_storage(category, item, 1):
            self.game.add_text(f"📦 {item} взят из хранилища", "success")
            self.window.destroy()
            self.show()