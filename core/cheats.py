import random
import tkinter as tk
from typing import Dict, List, Optional, Any

class CheatSystem:
    
    def __init__(self, game_window):
        self.game = game_window
        self.cheats_enabled = True
        self.cheat_history = []
        self.cheat_codes = self.init_cheats()
        
    def init_cheats(self) -> Dict[str, Dict]:
        return {
            # Ресурсы
            "hesoyam": {
                "name": "Ресурсы",
                "description": "Восстанавливает здоровье, ману и выносливость",
                "function": self.cheat_hesoyam,
                "cooldown": 0
            },
            "baguvix": {
                "name": "Золото",
                "description": "Добавляет 1000 золота",
                "function": self.cheat_money,
                "cooldown": 0
            },
            "fullheal": {
                "name": "Полное исцеление",
                "description": "Полностью восстанавливает здоровье",
                "function": self.cheat_fullheal,
                "cooldown": 0
            },
            
            # Характеристики
            "levelup": {
                "name": "Повышение уровня",
                "description": "Повышает уровень на 1",
                "function": self.cheat_levelup,
                "cooldown": 0
            },
            "strong": {
                "name": "Сила",
                "description": "Увеличивает силу на 10",
                "function": lambda: self.cheat_stat("сила", 10),
                "cooldown": 0
            },
            "agile": {
                "name": "Ловкость",
                "description": "Увеличивает ловкость на 10",
                "function": lambda: self.cheat_stat("ловкость", 10),
                "cooldown": 0
            },
            "smart": {
                "name": "Интеллект",
                "description": "Увеличивает интеллект на 10",
                "function": lambda: self.cheat_stat("интеллект", 10),
                "cooldown": 0
            },
            "wise": {
                "name": "Мудрость",
                "description": "Увеличивает мудрость на 10",
                "function": lambda: self.cheat_stat("мудрость", 10),
                "cooldown": 0
            },
            "charming": {
                "name": "Харизма",
                "description": "Увеличивает харизму на 10",
                "function": lambda: self.cheat_stat("харизма", 10),
                "cooldown": 0
            },
            "luckyme": {
                "name": "Удача",
                "description": "Увеличивает удачу на 10",
                "function": lambda: self.cheat_stat("удача", 10),
                "cooldown": 0
            },
            
            # Предметы
            "allweapons": {
                "name": "Все оружие",
                "description": "Добавляет все виды оружия",
                "function": self.cheat_all_weapons,
                "cooldown": 0
            },
            "allarmor": {
                "name": "Вся броня",
                "description": "Добавляет все виды брони",
                "function": self.cheat_all_armor,
                "cooldown": 0
            },
            "allpotions": {
                "name": "Все зелья",
                "description": "Добавляет все виды зелий (x10)",
                "function": self.cheat_all_potions,
                "cooldown": 0
            },
            "godmode": {
                "name": "Режим бога",
                "description": "Включает/выключает режим бога (бессмертие)",
                "function": self.cheat_godmode,
                "cooldown": 0
            },
            
            # Мир
            "changeweather": {
                "name": "Смена погоды",
                "description": "Меняет погоду",
                "function": self.cheat_weather,
                "cooldown": 0
            },
            "daytime": {
                "name": "Время суток",
                "description": "Переключает время суток",
                "function": self.cheat_time,
                "cooldown": 0
            },
            "fasttravel": {
                "name": "Быстрое перемещение",
                "description": "Телепортирует в указанную локацию",
                "function": self.cheat_travel,
                "cooldown": 0
            },
            
            # Отношения
            "friendly": {
                "name": "Дружелюбие",
                "description": "Увеличивает отношения со всеми NPC",
                "function": self.cheat_friendly,
                "cooldown": 0
            },
            "respect": {
                "name": "Репутация",
                "description": "Увеличивает всю репутацию",
                "function": self.cheat_reputation,
                "cooldown": 0
            },
            
            # Информация
            "map": {
                "name": "Карта",
                "description": "Открывает всю карту",
                "function": self.cheat_map,
                "cooldown": 0
            },
            "stats": {
                "name": "Статистика",
                "description": "Показывает подробную статистику",
                "function": self.cheat_stats,
                "cooldown": 0
            },
            "whereis": {
                "name": "Где NPC",
                "description": "Показывает местоположение всех NPC",
                "function": self.cheat_whereis,
                "cooldown": 0
            },
            
            # Квесты
            "completequest": {
                "name": "Завершить квест",
                "description": "Завершает текущий активный квест",
                "function": self.cheat_complete_quest,
                "cooldown": 0
            },
            "showquests": {
                "name": "Показать квесты",
                "description": "Показывает все доступные квесты",
                "function": self.cheat_show_quests,
                "cooldown": 0
            },
            
            # Веселые
            "party": {
                "name": "Вечеринка",
                "description": "Включает режим вечеринки",
                "function": self.cheat_party,
                "cooldown": 0
            },
            "dance": {
                "name": "Танец",
                "description": "Заставляет всех NPC танцевать",
                "function": self.cheat_dance,
                "cooldown": 0
            },
            "rainbow": {
                "name": "Радуга",
                "description": "Радужный режим",
                "function": self.cheat_rainbow,
                "cooldown": 0
            },
            
            # Секретные
            "konami": {
                "name": "Konami Code",
                "description": "Секретный код Konami",
                "function": self.cheat_konami,
                "cooldown": 0,
                "hidden": True
            },
            "idkfa": {
                "name": "Doom Mode",
                "description": "Режим Doom",
                "function": self.cheat_doom,
                "cooldown": 0,
                "hidden": True
            },
            "motherlode": {
                "name": "Sims Mode",
                "description": "Очень много денег",
                "function": self.cheat_motherlode,
                "cooldown": 0,
                "hidden": True
            },
            "rosebud": {
                "name": "Sims Classic",
                "description": "1000 золота (классика)",
                "function": lambda: self.cheat_money(1000),
                "cooldown": 0,
                "hidden": True
            },
            "howdoyouturnthison": {
                "name": "Age of Empires",
                "description": "Спавнит машину",
                "function": self.cheat_aoe,
                "cooldown": 0,
                "hidden": True
            },
            "thereisnospoon": {
                "name": "Матрица",
                "description": "Замедление времени",
                "function": self.cheat_matrix,
                "cooldown": 0,
                "hidden": True
            }
        }
    
    def process_cheat(self, cheat_code: str) -> str:
        """Обработка чит-кода"""
        cheat_code = cheat_code.lower().strip()
        
        if not self.cheats_enabled and cheat_code != "enablecheats":
            return "❌ Читы отключены"
        
        # Специальные коды
        if cheat_code == "enablecheats":
            self.cheats_enabled = True
            return "✅ Читы включены"
        
        if cheat_code == "disablecheats":
            self.cheats_enabled = False
            return "✅ Читы отключены"
        
        if cheat_code == "cheats":
            return self.show_cheats()
        
        # Поиск чит-кода
        if cheat_code in self.cheat_codes:
            cheat = self.cheat_codes[cheat_code]
            
            # Проверка на скрытые читы
            if cheat.get("hidden", False) and not self.cheats_enabled:
                return "❌ Неизвестный код"
            
            # Выполнение
            try:
                result = cheat["function"]()
                
                self.cheat_history.append({
                    "code": cheat_code,
                    "name": cheat["name"],
                    "time": self.game.world.get_time_string()
                })
                
                return f"✅ {cheat['name']}: {result}"
            except Exception as e:
                return f"❌ Ошибка: {e}"
        
        return f"❌ Неизвестный код: {cheat_code}"
    
    def show_cheats(self) -> str:
        """Показать все доступные читы"""
        result = "📋 ДОСТУПНЫЕ ЧИТ-КОДЫ:\n\n"
        
        # Группировка по категориям
        categories = {
            "Ресурсы": ["hesoyam", "baguvix", "fullheal", "motherlode", "rosebud"],
            "Характеристики": ["levelup", "strong", "agile", "smart", "wise", "charming", "luckyme"],
            "Предметы": ["allweapons", "allarmor", "allpotions", "godmode"],
            "Мир": ["changeweather", "daytime", "fasttravel"],
            "Отношения": ["friendly", "respect"],
            "Информация": ["map", "stats", "whereis", "showquests"],
            "Квесты": ["completequest"],
            "Секретные": ["konami", "idkfa", "howdoyouturnthison", "thereisnospoon"]
        }
        
        for category, codes in categories.items():
            result += f"📌 {category}:\n"
            for code in codes:
                if code in self.cheat_codes and not self.cheat_codes[code].get("hidden", False):
                    cheat = self.cheat_codes[code]
                    result += f"  • {code} - {cheat['description']}\n"
            result += "\n"
        
        result += "⚡ enablecheats - включить читы\n"
        result += "⚡ disablecheats - выключить читы\n"
        result += "⚡ cheats - показать эту справку"
        
        return result
    
    # Чит-функции
    def cheat_hesoyam(self) -> str:
        """Восстановление ресурсов"""
        player = self.game.game_state.player
        player["health"] = player["max_health"]
        player["mana"] = player["max_mana"]
        player["stamina"] = player["max_stamina"]
        self.game.update_ui()
        return "Здоровье, мана и выносливость восстановлены"
    
    def cheat_money(self, amount: int = 1000) -> str:
        """Добавление денег"""
        self.game.game_state.player["money"] += amount
        self.game.update_ui()
        return f"Добавлено {amount} золота"
    
    def cheat_motherlode(self) -> str:
        """Очень много денег"""
        self.game.game_state.player["money"] += 50000
        self.game.update_ui()
        return "Добавлено 50000 золота (мать лод!)"
    
    def cheat_fullheal(self) -> str:
        """Полное исцеление"""
        player = self.game.game_state.player
        player["health"] = player["max_health"]
        self.game.update_ui()
        return "Здоровье полностью восстановлено"
    
    def cheat_levelup(self) -> str:
        """Повышение уровня"""
        player = self.game.game_state.player
        player["level"] += 1
        player["exp"] = 0
        player["max_health"] += 10
        player["health"] = player["max_health"]
        player["stat_points"] += 3
        self.game.update_ui()
        return f"Уровень повышен до {player['level']}"
    
    def cheat_stat(self, stat: str, amount: int) -> str:
        """Увеличение характеристики"""
        if stat in self.game.game_state.player["stats"]:
            self.game.game_state.player["stats"][stat] += amount
            self.game.update_ui()
            return f"{stat.capitalize()} увеличена на {amount}"
        return f"Характеристика {stat} не найдена"
    
    def cheat_all_weapons(self) -> str:
        """Все оружие"""
        weapons = ["ржавый_меч", "стальной_меч", "длинный_меч", "двуручный_меч",
                  "боевой_топор", "секира", "кинжал", "короткий_лук", "длинный_лук",
                  "арбалет", "булава", "цеп", "копье", "алебарда"]
        
        for weapon in weapons:
            self.game.game_state.player["inventory"].add_item("weapons", weapon, 1)
        
        self.game.update_ui()
        return f"Добавлено {len(weapons)} видов оружия"
    
    def cheat_all_armor(self) -> str:
        """Вся броня"""
        armors = ["старая_куртка", "кожаная_броня", "кольчуга", "латы",
                 "щит", "шлем", "поножи", "наручи", "плащ"]
        
        for armor in armors:
            self.game.game_state.player["inventory"].add_item("armor", armor, 1)
        
        self.game.update_ui()
        return f"Добавлено {len(armors)} видов брони"
    
    def cheat_all_potions(self) -> str:
        """Все зелья"""
        potions = ["зелье_здоровья", "зелье_маны", "зелье_силы", "зелье_ловкости",
                  "противоядие", "эликсир_жизни", "зелье_невидимости"]
        
        for potion in potions:
            self.game.game_state.player["inventory"].add_item("potions", potion, 10)
        
        self.game.update_ui()
        return f"Добавлено {len(potions)} видов зелий (x10)"
    
    def cheat_godmode(self) -> str:
        """Режим бога"""
        if not hasattr(self.game, "godmode"):
            self.game.godmode = True
            return "Режим бога ВКЛЮЧЕН"
        else:
            self.game.godmode = not self.game.godmode
            return f"Режим бога {'ВКЛЮЧЕН' if self.game.godmode else 'ВЫКЛЮЧЕН'}"
    
    def cheat_weather(self) -> str:
        """Смена погоды"""
        weathers = ["ясно", "облачно", "дождь", "гроза", "снег", "туман"]
        current = self.game.world.weather
        next_weather = weathers[(weathers.index(current) + 1) % len(weathers)]
        self.game.world.weather = next_weather
        self.game.update_ui()
        return f"Погода изменена на: {next_weather}"
    
    def cheat_time(self) -> str:
        """Смена времени суток"""
        self.game.world.hour = (self.game.world.hour + 6) % 24
        self.game.update_ui()
        return f"Время изменено на: {self.game.world.get_time_string()}"
    
    def cheat_travel(self) -> str:
        """Быстрое перемещение (вызывает диалог)"""
        # Создаем диалог выбора локации
        dialog = tk.Toplevel(self.game.root)
        dialog.title("Быстрое перемещение")
        dialog.geometry("300x400")
        dialog.configure(bg='#0a0a0a')
        dialog.transient(self.game.root)
        dialog.grab_set()
        
        # Заголовок
        tk.Label(dialog, text="🌍 Выбери локацию:",
                bg='#0a0a0a', fg='#00ff00',
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        locations = [
            "городская_площадь", "таверна", "рынок", "трущобы",
            "храм", "замок", "порт", "лес", "кладбище",
            "кузница", "гильдия", "подземелье", "башня_мага"
        ]
        
        # Список локаций
        listbox = tk.Listbox(dialog, bg='#1a1a1a', fg='#00ff00',
                             selectbackground='#4444ff', font=('Arial', 11))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заполняем список
        for loc in locations:
            display_name = loc.replace('_', ' ').title()
            listbox.insert(tk.END, display_name)
        
        def teleport():
            selection = listbox.curselection()
            if selection:
                loc = locations[selection[0]]
                self.game.game_state.current_location = loc
                self.game.add_text(f"📍 Телепортирован в {loc.replace('_', ' ').title()}", "gold")
                self.game.update_ui()
                dialog.destroy()
        
        # Кнопки
        btn_frame = tk.Frame(dialog, bg='#0a0a0a')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Телепорт", command=teleport,
                 bg='#333', fg='#00ff00', width=10,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy,
                 bg='#333', fg='#ff4444', width=10,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Привязка двойного клика
        listbox.bind('<Double-Button-1>', lambda e: teleport())
        
        return "Выберите локацию в открывшемся окне"
    
    def cheat_friendly(self) -> str:
        """Увеличение отношений со всеми NPC"""
        count = 0
        for npc in self.game.npcs.values():
            npc.relationship = min(100, npc.relationship + 30)
            count += 1
        return f"Отношения увеличены с {count} NPC"
    
    def cheat_reputation(self) -> str:
        """Увеличение всей репутации"""
        for group in self.game.game_state.player["reputation"]:
            self.game.game_state.player["reputation"][group] = min(100, 
                self.game.game_state.player["reputation"][group] + 30)
        return "Репутация увеличена во всех фракциях"
    
    def cheat_map(self) -> str:
        """Открытие карты"""
        self.game.show_map()
        return "Карта открыта"
    
    def cheat_stats(self) -> str:
        """Показать статистику"""
        stats = self.game.stats
        result = "📊 ПОДРОБНАЯ СТАТИСТИКА:\n"
        for key, value in stats.items():
            result += f"  • {key}: {value}\n"
        return result
    
    def cheat_whereis(self) -> str:
        """Показать местоположение всех NPC"""
        result = "👥 МЕСТОПОЛОЖЕНИЕ NPC:\n"
        locations = {}
        
        for npc in self.game.npcs.values():
            if npc.location not in locations:
                locations[npc.location] = []
            locations[npc.location].append(npc.name)
        
        for loc, names in locations.items():
            result += f"\n📍 {loc.replace('_', ' ').title()}:\n"
            for name in names[:5]:  # первые 5
                result += f"  • {name}\n"
            if len(names) > 5:
                result += f"  ... и еще {len(names) - 5}\n"
        
        return result
    
    def cheat_complete_quest(self) -> str:
        """Завершить текущий квест"""
        if self.game.quest_system.active_quests:
            quest = self.game.quest_system.active_quests[0]
            self.game.quest_system.completed_quests.append(quest)
            self.game.quest_system.active_quests.pop(0)
            self.game.game_state.player["money"] += quest["reward"]
            self.game.game_state.player["exp"] += quest["reward"]
            self.game.update_ui()
            return f"Квест '{quest['name']}' завершен! Получено {quest['reward']} опыта и золота"
        return "Нет активных квестов"
    
    def cheat_show_quests(self) -> str:
        """Показать все квесты"""
        result = "⚔ ДОСТУПНЫЕ КВЕСТЫ:\n"
        
        if self.game.quest_system.quests:
            for qid, quest in self.game.quest_system.quests.items():
                status = "✅" if qid in self.game.quest_system.completed_quests else "⚡" if qid in self.game.quest_system.active_quests else "📌"
                result += f"\n{status} {quest['name']}\n"
                result += f"   {quest['description']}\n"
                result += f"   Награда: {quest['reward']}💰"
        else:
            result += "Нет квестов"
        
        return result
    
    def cheat_party(self) -> str:
        """Режим вечеринки"""
        self.game.world.weather = "ясно"
        self.game.world.hour = 20
        self.game.add_text("🎉 ВЕЧЕРИНКА НАЧИНАЕТСЯ! 🎉", "gold")
        self.game.add_text("Все NPC собрались в таверне!", "info")
        
        for npc in self.game.npcs.values():
            npc.location = "таверна"
        
        self.game.update_ui()
        return "Party mode activated!"
    
    def cheat_dance(self) -> str:
        """Танец всех NPC"""
        self.game.add_text("💃 ВСЕ ТАНЦУЮТ! 🕺", "rainbow")
        return "All NPC are now dancing!"
    
    def cheat_rainbow(self) -> str:
        """Радужный режим"""
        import random
        
        def rainbow_cycle():
            colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'cyan', 'magenta']

            widgets = []
            if hasattr(self.game, 'name_label') and self.game.name_label:
                widgets.append(self.game.name_label)
            if hasattr(self.game, 'time_label') and self.game.time_label:
                widgets.append(self.game.time_label)
            if hasattr(self.game, 'weather_label') and self.game.weather_label:
                widgets.append(self.game.weather_label)
            if hasattr(self.game, 'health_label') and self.game.health_label:
                widgets.append(self.game.health_label)
            if hasattr(self.game, 'money_label') and self.game.money_label:
                widgets.append(self.game.money_label)
            
            for widget in widgets:
                if widget and widget.winfo_exists():
                    widget.config(fg=random.choice(colors))
            
            if hasattr(self.game, 'root') and self.game.root.winfo_exists():
                self.game.root.after(500, rainbow_cycle)
        
        rainbow_cycle()
        return "🌈 Rainbow mode enabled!"
    
    def cheat_konami(self) -> str:
        """Konami code"""
        self.game.add_text("⬆️⬆️⬇️⬇️⬅️➡️⬅️➡️🅱️🅰️ START", "gold")
        self.game.add_text("30 жизней добавлено!", "success")
        self.game.game_state.player["max_health"] += 30
        self.game.game_state.player["health"] = self.game.game_state.player["max_health"]
        return "Konami code activated!"
    
    def cheat_doom(self) -> str:
        """Doom mode"""
        self.game.add_text("🔥 IDKFA 🔥", "red")
        self.cheat_all_weapons()
        self.cheat_godmode()
        return "DOOM mode activated!"
    
    def cheat_aoe(self) -> str:
        """Age of Empires cheat"""
        self.game.add_text("🚗 HOW DO YOU TURN THIS ON 🚗", "blue")
        self.game.game_state.player["inventory"].add_item("misc", "бронемобиль", 1)
        return "Колесница смерти добавлена в инвентарь!"
    
    def cheat_matrix(self) -> str:
        """Matrix mode"""
        self.game.add_text("🧊 THERE IS NO SPOON 🧊", "green")
        self.game.add_text("Время замедлилось...", "info")
        return "Matrix mode activated!"