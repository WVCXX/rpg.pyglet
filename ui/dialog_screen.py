import tkinter as tk
from tkinter import scrolledtext
import random

class DialogScreen:
    """Окно диалога с NPC"""
    def __init__(self, parent, player, npc, game_window):
        self.parent = parent
        self.player = player
        self.npc = npc
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
            'fg_white': '#ffffff'
        }
    
    def show(self):
        """Показать окно диалога"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Разговор с {self.npc.name}")
        self.window.geometry("600x500")
        self.window.configure(bg=self.colors['bg_dark'])
        self.window.transient(self.parent)
        
        # Заголовок
        self.create_header()
        
        # Область диалога
        self.create_dialog_area()
        
        # Кнопки действий
        self.create_action_buttons()
    
    def create_header(self):
        """Создание заголовка"""
        header = tk.Frame(self.window, bg=self.colors['bg_medium'])
        header.pack(fill=tk.X, pady=5)
        
        # Имя и профессия
        name_frame = tk.Frame(header, bg=self.colors['bg_medium'])
        name_frame.pack(fill=tk.X, pady=5, padx=10)
        
        tk.Label(name_frame, text=self.npc.name,
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_gold'],
                font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        tk.Label(name_frame, text=f"({self.npc.profession})",
                bg=self.colors['bg_medium'],
                fg=self.colors['fg_blue'],
                font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        # Отношения
        rel = self.player["relationships"].get(self.npc.id, 0)
        rel_color = self.colors['fg_green'] if rel >= 0 else self.colors['fg_red']
        rel_text = f"Отношения: {rel}"
        
        tk.Label(name_frame, text=rel_text,
                bg=self.colors['bg_medium'],
                fg=rel_color,
                font=('Arial', 10)).pack(side=tk.RIGHT)
    
    def create_dialog_area(self):
        """Создание области диалога"""
        dialog_frame = tk.Frame(self.window, bg=self.colors['bg_medium'])
        dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dialog_text = scrolledtext.ScrolledText(dialog_frame,
                                                     wrap=tk.WORD,
                                                     bg='#000000',
                                                     fg=self.colors['fg_green'],
                                                     font=('Consolas', 11),
                                                     height=15)
        self.dialog_text.pack(fill=tk.BOTH, expand=True)
        self.dialog_text.config(state=tk.DISABLED)
        
        # Приветствие
        self.add_dialog(f"{self.npc.name}: {self.npc.dialog['greeting']}", self.colors['fg_blue'])
    
    def create_action_buttons(self):
        """Создание кнопок действий"""
        button_frame = tk.Frame(self.window, bg=self.colors['bg_dark'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        actions = [
            ("💬 Поговорить", self.talk),
            ("💰 Торговать", self.trade),
            ("📜 Квесты", self.quests),
            ("🤝 Подарок", self.gift),
            ("👋 Прощай", self.farewell)
        ]
        
        for text, cmd in actions:
            btn = tk.Button(button_frame, text=text,
                           bg=self.colors['bg_light'],
                           fg=self.colors['fg_white'],
                           command=cmd,
                           width=12)
            btn.pack(side=tk.LEFT, padx=2, expand=True)
    
    def add_dialog(self, text, color=None):
        """Добавление текста в диалог"""
        self.dialog_text.config(state=tk.NORMAL)
        self.dialog_text.insert(tk.END, text + "\n\n")
        
        if color:
            # Изменение цвета последней строки
            last_line_start = self.dialog_text.index(f"end-2c linestart")
            last_line_end = self.dialog_text.index("end-1c")
            self.dialog_text.tag_add("color", last_line_start, last_line_end)
            self.dialog_text.tag_config("color", foreground=color)
        
        self.dialog_text.see(tk.END)
        self.dialog_text.config(state=tk.DISABLED)
    
    def talk(self):
        """Обычный разговор"""
        responses = [
            "Как жизнь?",
            "Что нового в городе?",
            "Как прошел твой день?",
            "Есть какие-то новости?",
            "Расскажи о себе"
        ]
        
        player_text = random.choice(responses)
        self.add_dialog(f"Ты: {player_text}", self.colors['fg_green'])
        
        # Ответ NPC
        npc_responses = [
            "Да все как обычно...",
            "Слышал, в замке что-то готовят",
            "День прошел хорошо, спасибо",
            "Новостей особо нет",
            f"Я {self.npc.name}, {self.npc.profession}. А ты?"
        ]
        
        self.add_dialog(f"{self.npc.name}: {random.choice(npc_responses)}", self.colors['fg_blue'])
        
        # Изменение отношений
        self.update_relationship(1)
    
    def trade(self):
        """Торговля"""
        if not self.npc.is_merchant:
            self.add_dialog(f"{self.npc.name}: Я не торгую", self.colors['fg_red'])
            return
        
        self.add_dialog(f"{self.npc.name}: {self.npc.dialog['trade']}", self.colors['fg_blue'])
        
        # Показ товаров
        if self.npc.trade_goods:
            goods = "\n".join([f"  • {item['name']} - {item['price']}💰" 
                              for item in self.npc.trade_goods.values()])
            self.add_dialog(f"Товары:\n{goods}", self.colors['fg_gold'])
    
    def quests(self):
        """Квесты"""
        if self.npc.is_quest_giver:
            self.add_dialog(f"{self.npc.name}: {self.npc.dialog['quest']}", self.colors['fg_blue'])
        else:
            self.add_dialog(f"{self.npc.name}: У меня нет для тебя заданий", self.colors['fg_gray'])
    
    def gift(self):
        """Подарок"""
        # Проверка наличия подарков в инвентаре
        gifts = self.player["inventory"].get_all_items().get("misc", [])
        
        if not gifts:
            self.add_dialog("У тебя нет ничего для подарка", self.colors['fg_red'])
            return
        
        # Создание окна выбора подарка
        gift_window = tk.Toplevel(self.window)
        gift_window.title("Выбери подарок")
        gift_window.geometry("300x400")
        gift_window.configure(bg=self.colors['bg_dark'])
        
        tk.Label(gift_window, text="Что подарить?",
                bg=self.colors['bg_dark'],
                fg=self.colors['fg_gold']).pack(pady=10)
        
        listbox = tk.Listbox(gift_window, bg=self.colors['bg_light'],
                             fg=self.colors['fg_green'])
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item_name, count in gifts:
            if count > 0:
                listbox.insert(tk.END, f"{item_name} x{count}")
        
        def give_selected():
            selection = listbox.curselection()
            if selection:
                item_data = gifts[selection[0]]
                item_name = item_data[0]
                
                # Удаляем предмет
                if self.player["inventory"].remove_item("misc", item_name, 1):
                    self.add_dialog(f"Ты даришь {item_name} {self.npc.name}", self.colors['fg_green'])
                    
                    # Реакция NPC
                    reactions = [
                        "О, спасибо!",
                        "Какой приятный сюрприз!",
                        "Ты очень щедр!",
                        f"{item_name}? Спасибо!"
                    ]
                    self.add_dialog(f"{self.npc.name}: {random.choice(reactions)}", self.colors['fg_blue'])
                    
                    # Увеличение отношений
                    self.update_relationship(5)
                    
                    gift_window.destroy()
        
        tk.Button(gift_window, text="Подарить",
                 bg=self.colors['bg_light'],
                 fg=self.colors['fg_green'],
                 command=give_selected).pack(pady=5)
    
    def farewell(self):
        """Прощание"""
        self.add_dialog(f"{self.npc.name}: {self.npc.dialog['farewell']}", self.colors['fg_blue'])
        self.window.after(1500, self.window.destroy)
    
    def update_relationship(self, amount):
        """Обновление отношений"""
        current = self.player["relationships"].get(self.npc.id, 0)
        new_value = max(-100, min(100, current + amount))
        self.player["relationships"][self.npc.id] = new_value
        
        self.game.stats["диалогов_проведено"] += 1
        self.game.update_ui()