import random
from typing import Dict, List, Optional, Any  
from datetime import datetime

class NPC:
    """Класс NPC с расширенными возможностями и русской локализацией"""
    
    RACES = ["человек", "эльф", "гном", "полурослик", "орк", "полуэльф"]
    
    PROFESSIONS = [
        "крестьянин", "торговец", "стражник", "жрец", "кузнец",
        "трактирщик", "алхимик", "лекарь", "вор", "наемник",
        "менестрель", "охотник", "рыбак", "пекарь", "портной",
        "сапожник", "гончар", "плотник", "каменщик", "винодел",
        "ученый", "библиотекарь", "писарь", "ювелир", "кожевник"
    ]
    
    PERSONALITIES = [
        "добрый", "злой", "хитрый", "честный", "грубый",
        "веселый", "угрюмый", "болтливый", "молчаливый", "подозрительный",
        "щедрый", "жадный", "храбрый", "трусливый", "мудрый",
        "глупый", "романтичный", "прагматичный", "религиозный", "циничный"
    ]
    
    # Русские имена
    MALE_NAMES = [
        "Иван", "Петр", "Алексей", "Дмитрий", "Сергей", "Николай",
        "Владимир", "Михаил", "Андрей", "Павел", "Артем", "Максим",
        "Александр", "Константин", "Григорий", "Борис", "Федор",
        "Илья", "Роман", "Василий", "Георгий", "Юрий", "Виктор",
        "Эриан", "Леголас", "Гимли", "Торин", "Балин", "Двалин",
        "Кили", "Фили", "Оин", "Глоин", "Бифур", "Бофур"
    ]
    
    FEMALE_NAMES = [
        "Анна", "Мария", "Елена", "Ольга", "Наталья", "Татьяна",
        "Светлана", "Ирина", "Екатерина", "Дарья", "Юлия", "Анастасия",
        "София", "Александра", "Вера", "Надежда", "Любовь", "Ксения",
        "Арвен", "Галадриэль", "Лутиэн", "Диса", "Хельга", "Бригитта",
        "Исиль", "Тин", "Нин", "Элен"
    ]
    
    SURNAMES = [
        "Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов",
        "Попов", "Васильев", "Михайлов", "Федоров", "Морозов",
        "Волков", "Алексеев", "Лебедев", "Семенов", "Егоров",
        "Павлов", "Козлов", "Степанов", "Николаев", "Орлов"
    ]
    
    NICKNAMES = [
        "Хитрый", "Сильный", "Мудрый", "Быстрый", "Ворчун",
        "Молчун", "Весельчак", "Угрюмый", "Рыжий", "Косой",
        "Кривой", "Хромой", "Толстый", "Тощий", "Длинный",
        "Маленький", "Лысый", "Бородач", "Кузнечик", "Соловей"
    ]
    
    def __init__(self, npc_id: str, name: str = None, race: str = None, 
                 gender: str = None, profession: str = None, personality: str = None):
        """
        Инициализация NPC
        :param npc_id: уникальный идентификатор
        :param name: имя (если None - генерируется)
        :param race: раса (если None - генерируется)
        :param gender: пол (если None - генерируется)
        :param profession: профессия (если None - генерируется)
        :param personality: характер (если None - генерируется)
        """
        self.id = npc_id
        self.gender = gender if gender else random.choice(["муж", "жен"])
        self.name = name if name else self.generate_name()
        self.race = race if race else random.choice(self.RACES)
        self.profession = profession if profession else random.choice(self.PROFESSIONS)
        self.personality = personality if personality else random.choice(self.PERSONALITIES)
        
        # Основные характеристики (должны быть до вызова generate_dialog)
        self.age = random.randint(16, 80)
        self.relationship = 0  # -100 до 100, отношение к игроку
        self.location = self.generate_start_location()
        self.home_location = self.location
        
        # Экономика
        self.money = random.randint(10, 500) * (1 + self.age // 50)
        self.is_merchant = self.profession in ["торговец", "трактирщик", "кузнец", "алхимик"] or random.random() < 0.2
        self.inventory = self.generate_inventory()
        self.trade_goods = self.generate_trade_goods() if self.is_merchant else {}
        
        # ВАЖНО: is_quest_giver должен быть определен ДО generate_dialog
        self.is_quest_giver = random.random() < 0.15
        self.quests_available = []
        
        # Диалоги и общение (теперь is_quest_giver уже определен)
        self.dialog = self.generate_dialog()
        self.secrets = self.generate_secrets()
        self.gossip = self.generate_gossip()
        self.rumors = []
        
        # Состояние
        self.is_alive = True
        self.is_busy = False
        
        # Внешность
        self.appearance = self.generate_appearance()
        
        # Расписание
        self.schedule = self.generate_schedule()
        self.current_activity = "отдых"
        
        # Социальные связи
        self.family = []  # члены семьи
        self.friends = []  # друзья
        self.enemies = []  # враги
        self.employer = None  # работодатель
        
        # Дополнительные характеристики
        self.skills = self.generate_skills()
        self.traits = self.generate_traits()
        self.history = self.generate_history()
        self.known_locations = [self.location]
    
    def generate_name(self) -> str:
        """Генерация полного имени NPC"""
        if self.gender == "муж":
            first_name = random.choice(self.MALE_NAMES)
        else:
            first_name = random.choice(self.FEMALE_NAMES)
        
        # 50% шанс на фамилию
        if random.random() < 0.5:
            surname = random.choice(self.SURNAMES)
            if self.gender == "жен":
                surname += "а"
            full_name = f"{first_name} {surname}"
        else:
            full_name = first_name
        
        # 30% шанс на прозвище
        if random.random() < 0.3:
            nickname = random.choice(self.NICKNAMES)
            full_name += f" по прозвищу '{nickname}'"
        
        return full_name
    
    def generate_start_location(self) -> str:
        """Генерация начальной локации"""
        locations = [
            "городская_площадь", "таверна", "рынок", "трущобы", 
            "храм", "замок", "порт", "кузница", "гильдия"
        ]
        return random.choice(locations)
    
    def generate_appearance(self) -> Dict[str, str]:
        """Генерация внешности"""
        hair_colors = ["русые", "черные", "рыжие", "седые", "светлые", "каштановые", "пепельные"]
        eye_colors = ["голубые", "карие", "зеленые", "серые", "синие", "ореховые"]
        heights = ["низкий", "ниже среднего", "средний", "выше среднего", "высокий"]
        builds = ["худой", "стройный", "средний", "плотный", "полный", "коренастый"]
        
        # Особые приметы
        special_signs = [
            "шрам на лице", "татуировка", "родинка над губой", "хромота",
            "отсутствует палец", "бородавка на носу", "шрам на руке",
            "шрам на шее", "косоглазие", "нет зуба", "пирсинг", None
        ]
        
        appearance = {
            "волосы": random.choice(hair_colors),
            "глаза": random.choice(eye_colors),
            "рост": random.choice(heights),
            "телосложение": random.choice(builds),
            "особые_приметы": random.choice(special_signs) if random.random() < 0.3 else None
        }
        
        # Расовая специфика
        if self.race == "эльф":
            appearance["волосы"] = random.choice(["золотистые", "серебряные", "белые", "русые"])
            appearance["особые_приметы"] = "острые уши"
        elif self.race == "гном":
            appearance["волосы"] = random.choice(["рыжие", "русые", "седые", "черные"])
            appearance["особые_приметы"] = "густая борода"
        elif self.race == "орк":
            appearance["рост"] = random.choice(["высокий", "очень высокий"])
            appearance["особые_приметы"] = "клыки"
        
        return appearance
    
    def generate_inventory(self) -> Dict[str, int]:
        """Генерация инвентаря"""
        inventory = {}
        
        # У всех есть базовые вещи
        base_items = {
            "хлеб": random.randint(1, 3),
            "вода": random.randint(1, 2),
            "свеча": random.randint(1, 5)
        }
        inventory.update(base_items)
        
        # Профессиональные предметы
        profession_items = {
            "крестьянин": {"зерно": random.randint(5, 20), "яйца": random.randint(3, 10)},
            "торговец": {"товары": random.randint(10, 50)},
            "стражник": {"меч": 1, "щит": 1, "форма": 1},
            "жрец": {"святая_вода": random.randint(1, 3), "свечи": random.randint(5, 20)},
            "кузнец": {"уголь": random.randint(10, 30), "железо": random.randint(5, 15)},
            "трактирщик": {"пиво": random.randint(10, 50), "еда": random.randint(20, 100)},
            "алхимик": {"зелья": random.randint(1, 5), "травы": random.randint(5, 20)},
            "лекарь": {"бинты": random.randint(5, 20), "мази": random.randint(1, 5)},
            "вор": {"отмычки": random.randint(1, 5), "воровской_инструмент": 1},
            "наемник": {"меч": 1, "броня": 1, "зелье_здоровья": random.randint(1, 3)},
            "охотник": {"лук": 1, "стрелы": random.randint(10, 50), "шкуры": random.randint(1, 5)},
            "рыбак": {"удочка": 1, "рыба": random.randint(5, 20)},
            "пекарь": {"мука": random.randint(10, 30), "хлеб": random.randint(5, 20)},
            "ювелир": {"кольца": random.randint(1, 5), "камни": random.randint(3, 10)}
        }
        
        if self.profession in profession_items:
            inventory.update(profession_items[self.profession])
        
        return inventory
    
    def generate_trade_goods(self) -> Dict[str, Dict]:
        """Генерация товаров для торговли"""
        goods = {}
        
        # Цены и количество зависят от профессии
        price_mult = 1.0
        
        if self.profession == "торговец":
            categories = ["оружие", "броня", "зелья", "еда", "книги"]
            for cat in categories:
                count = random.randint(5, 20)
                for i in range(count):
                    item = f"товар_{i}"
                    goods[item] = {
                        "name": f"Товар {i}",
                        "price": random.randint(10, 100),
                        "quantity": random.randint(1, 10)
                    }
        
        elif self.profession == "кузнец":
            weapons = ["меч", "топор", "кинжал", "булава"]
            for weapon in weapons:
                goods[weapon] = {
                    "name": weapon.capitalize(),
                    "price": random.randint(50, 200),
                    "quantity": random.randint(1, 3)
                }
        
        elif self.profession == "алхимик":
            potions = ["зелье_здоровья", "зелье_маны", "противоядие"]
            for potion in potions:
                goods[potion] = {
                    "name": potion.replace('_', ' ').capitalize(),
                    "price": random.randint(20, 80),
                    "quantity": random.randint(3, 10)
                }
        
        return goods
    
    def generate_dialog(self) -> Dict[str, str]:
        """Генерация диалогов"""
        # Приветствия в зависимости от профессии
        greetings = {
            "трактирщик": "Заходи, путник! Пиво свежее, еда горячая!",
            "кузнец": "Нужен меч? Или подковать коня?",
            "стражник": "Проходи, не задерживайся.",
            "жрец": "Да хранит тебя Единый.",
            "торговец": "Лучшие товары только у меня! Заходи, не пожалеешь!",
            "крестьянин": "Здравствуй, господин хороший.",
            "вор": "Чего надо? Не до тебя сейчас.",
            "алхимик": "Осторожно, не трогай колбы! Тут такие реактивы...",
            "лекарь": "На прием? Или за травами?",
            "наемник": "Работы ищешь? У меня есть пара предложений.",
            "менестрель": "Хочешь послушать песню о славных подвигах?",
            "охотник": "Дичи прикупить хочешь? Свежая, только сегодня добыл.",
            "рыбак": "Рыбка, рыбка... Свежая рыба!",
            "пекарь": "Пирожки! Горячие пирожки!",
            "ювелир": "Украшения для прекрасных дам и доблестных воинов."
        }
        
        # Прощания
        farewells = {
            "добрый": "Будь здоров, приходи еще!",
            "злой": "Проваливай уже.",
            "хитрый": "Ну, бывай... если увидимся.",
            "честный": "Счастливого пути!",
            "грубый": "Вали отсюда.",
            "веселый": "Заходи еще, поболтаем!",
            "угрюмый": "Иди уже...",
            "болтливый": "Ой, а я тебе еще не рассказал про... А, уходишь? Ну ладно...",
            "молчаливый": "... (кивает)"
        }
        
        # Торговля
        trade = {
            "торговец": "Вот мой товар. Лучший в городе!",
            "кузнец": "Смотри, что у меня есть. Сам ковал!",
            "алхимик": "Зелья? Травы? Яды? Все есть!",
            "default": "Можешь посмотреть мой товар."
        }
        
        # Квесты - используем self.is_quest_giver который уже определен
        quest_text = "Есть одно дельце... Не поможешь?" if self.is_quest_giver else "Ничего особенного сейчас нет."
        
        # Слухи
        gossip = {
            "трактирщик": "Слышал, в старом склепе опять огни видели...",
            "стражник": "Бандиты активизировались на северной дороге.",
            "крестьянин": "Урожай в этом году плохой...",
            "default": "Ничего интересного не слышал."
        }
        
        return {
            "greeting": greetings.get(self.profession, "Здравствуй, путник."),
            "farewell": farewells.get(self.personality, "Прощай."),
            "trade": trade.get(self.profession if self.is_merchant else "default", trade["default"]),
            "quest": quest_text,
            "gossip": gossip.get(self.profession, gossip["default"]),
            "about_self": self.generate_self_description(),
            "about_others": {}
        }
    
    def generate_self_description(self) -> str:
        """Генерация описания себя"""
        templates = [
            f"Я {self.name}, {self.profession} местный.",
            f"Зовут меня {self.name}, {self.age} годков, {self.profession}.",
            f"{self.name} я. А ты кто будешь?",
            f"Я {self.name}, живу здесь с рождения.",
            f"{self.name}, {self.profession}. Чего надо?"
        ]
        return random.choice(templates)
    
    def generate_secrets(self) -> List[Dict]:
        """Генерация секретов NPC"""
        secrets = []
        
        possible_secrets = [
            {"type": "долг", "text": "Должен крупную сумму ростовщику", "revealed": False},
            {"type": "преступление", "text": "Совершил преступление в прошлом", "revealed": False},
            {"type": "любовь", "text": "Тайно влюблен в местную красавицу", "revealed": False},
            {"type": "сокровище", "text": "Знает, где спрятан клад", "revealed": False},
            {"type": "семья", "text": "Ищет пропавшего родственника", "revealed": False},
            {"type": "благородство", "text": "На самом деле обедневший дворянин", "revealed": False},
            {"type": "магия", "text": "Умеет колдовать, но скрывает", "revealed": False},
            {"type": "страх", "text": "Смертельно боится пауков", "revealed": False},
            {"type": "прошлое", "text": "Был наемником, но бросил", "revealed": False},
            {"type": "идентичность", "text": "Скрывает свою истинную личность", "revealed": False}
        ]
        
        # У каждого NPC есть 1-3 секрета
        secret_count = random.randint(1, 3)
        selected = random.sample(possible_secrets, min(secret_count, len(possible_secrets)))
        
        for secret in selected:
            secret_copy = secret.copy()
            secret_copy["id"] = f"{self.id}_secret_{len(secrets)}"
            secrets.append(secret_copy)
        
        return secrets
    
    def generate_gossip(self) -> List[str]:
        """Генерация слухов, которые знает NPC"""
        all_gossip = [
            "Говорят, в старом замке привидения...",
            "Купец Грабин завышает цены, осторожнее с ним.",
            "Видели странные огни в лесу по ночам.",
            "Кто-то грабит обозы на северной дороге.",
            "В храме ищут смельчаков для опасного задания.",
            "Гномы опять закрыли проход через горы.",
            "В порт приплыл корабль из далеких земель.",
            "Старый алхимик ищет редкие ингредиенты.",
            "У кузнеца сломался молот, теперь не работает.",
            "Крысы расплодились в подвалах...",
            "Кто-то видел дракона в горах!",
            "Цены на зерно упали, крестьяне в убытке.",
            "Стражники ищут сбежавшего преступника.",
            "В таверне новый менестрель, поет дивно.",
            "Лекарь говорит, что приближается эпидемия."
        ]
        
        # Каждый NPC знает 1-3 слуха
        gossip_count = random.randint(1, 3)
        return random.sample(all_gossip, min(gossip_count, len(all_gossip)))
    
    def generate_skills(self) -> Dict[str, int]:
        """Генерация навыков"""
        skills = {
            "торговля": random.randint(20, 80),
            "красноречие": random.randint(20, 80),
            "ремесло": random.randint(20, 80),
            "выживание": random.randint(20, 80),
            "скрытность": random.randint(20, 80)
        }
        
        # Профессиональные бонусы
        profession_bonuses = {
            "торговец": {"торговля": 30, "красноречие": 20},
            "стражник": {"бой": 30, "выживание": 10},
            "кузнец": {"ремесло": 40, "сила": 20},
            "алхимик": {"алхимия": 40, "интеллект": 20},
            "вор": {"скрытность": 40, "ловкость": 20},
            "жрец": {"мудрость": 30, "красноречие": 20},
            "охотник": {"выживание": 40, "скрытность": 20}
        }
        
        if self.profession in profession_bonuses:
            for skill, bonus in profession_bonuses[self.profession].items():
                if skill in skills:
                    skills[skill] = min(100, skills[skill] + bonus)
                else:
                    skills[skill] = 30 + bonus
        
        return skills
    
    def generate_traits(self) -> List[str]:
        """Генерация черт характера"""
        all_traits = [
            "религиозный", "суеверный", "жадный", "щедрый",
            "храбрый", "трусливый", "любопытный", "равнодушный",
            "доверчивый", "подозрительный", "ленивый", "трудолюбивый",
            "честный", "лживый", "верный", "продажный",
            "романтичный", "циничный", "оптимист", "пессимист"
        ]
        
        # 3-5 черт характера
        trait_count = random.randint(3, 5)
        return random.sample(all_traits, min(trait_count, len(all_traits)))
    
    def generate_history(self) -> str:
        """Генерация предыстории"""
        events = []
        
        # Рождение
        birth_place = random.choice(["в этом городе", "в деревне", "в столице", "в другом королевстве"])
        events.append(f"Родился {birth_place}")
        
        # Детство
        childhood = random.choice([
            "рос в бедной семье",
            "воспитывался в приюте",
            "был любимым ребенком в богатой семье",
            "рано потерял родителей",
            "был подмастерьем у ремесленника"
        ])
        events.append(childhood)
        
        # Судьбоносное событие
        fateful = random.choice([
            "пережил нападение разбойников",
            "спас кого-то от смерти",
            "совершил преступление",
            "нашел клад",
            "встретил странного странника",
            "пережил эпидемию",
            "участвовал в войне",
            "потерял все в пожаре"
        ])
        events.append(f"В юности {fateful}")
        
        # Текущая жизнь
        current = f"Сейчас работает {self.profession}"
        events.append(current)
        
        return ". ".join(events)
    
    def generate_schedule(self) -> Dict[str, str]:
        """Генерация расписания"""
        schedule = {}
        
        # Базовое расписание в зависимости от профессии
        if self.profession in ["стражник", "сторож"]:
            schedule = {
                "ночь": self.location,
                "утро": self.location,
                "день": self.location,
                "вечер": self.home_location
            }
        elif self.profession in ["трактирщик", "торговец"]:
            schedule = {
                "ночь": self.home_location,
                "утро": self.location,
                "день": self.location,
                "вечер": self.location
            }
        else:
            schedule = {
                "ночь": self.home_location,
                "утро": self.location,
                "день": self.location,
                "вечер": self.home_location
            }
        
        return schedule
    
    def update_relationship(self, change: int) -> str:
        """Обновление отношений с игроком"""
        old_rel = self.relationship
        self.relationship = max(-100, min(100, self.relationship + change))
        
        if self.relationship <= -80 and old_rel > -80:
            return f"{self.name} теперь твой кровный враг!"
        elif self.relationship <= -50 and old_rel > -50:
            return f"{self.name} ненавидит тебя"
        elif self.relationship <= -20 and old_rel > -20:
            return f"{self.name} недолюбливает тебя"
        elif self.relationship >= 80 and old_rel < 80:
            return f"{self.name} готов за тебя жизнь отдать!"
        elif self.relationship >= 50 and old_rel < 50:
            return f"{self.name} очень хорошо к тебе относится"
        elif self.relationship >= 20 and old_rel < 20:
            return f"{self.name} проникся к тебе симпатией"
        
        return ""
    
    def get_relationship_status(self) -> str:
        """Получение статуса отношений"""
        if self.relationship >= 80:
            return "преданный друг"
        elif self.relationship >= 50:
            return "хороший друг"
        elif self.relationship >= 20:
            return "приятель"
        elif self.relationship >= -20:
            return "нейтрален"
        elif self.relationship >= -50:
            return "неприязнь"
        elif self.relationship >= -80:
            return "враждебен"
        else:
            return "кровный враг"
    
    def get_dialog_by_mood(self) -> str:
        """Получение диалога в зависимости от настроения"""
        if self.relationship >= 50:
            return f"{self.name}: Рад тебя видеть, друг!"
        elif self.relationship >= 20:
            return f"{self.name}: Привет, приятно встретить."
        elif self.relationship >= -20:
            return self.dialog["greeting"]
        elif self.relationship >= -50:
            return f"{self.name}: Чего тебе? Не до разговоров."
        else:
            return f"{self.name}: Проваливай, пока цел!"
    
    def trade_with_player(self, player, item_id: str, quantity: int = 1) -> Dict:
        """Торговля с игроком"""
        result = {
            "success": False,
            "message": "",
            "price": 0,
            "item": None
        }
        
        if not self.is_merchant:
            result["message"] = f"{self.name} не торгует"
            return result
        
        if item_id not in self.trade_goods:
            result["message"] = "Такого товара нет"
            return result
        
        item = self.trade_goods[item_id]
        
        if item["quantity"] < quantity:
            result["message"] = "Недостаточно товара"
            return result
        
        total_price = item["price"] * quantity
        
        if player.money < total_price:
            result["message"] = f"Не хватает денег! Нужно {total_price} монет"
            return result
        
        # Совершаем сделку
        player.money -= total_price
        self.money += total_price
        item["quantity"] -= quantity
        
        # Определяем категорию предмета
        category = "misc"
        if "зелье" in item_id:
            category = "potions"
        elif "меч" in item_id or "топор" in item_id:
            category = "weapons"
        elif "броня" in item_id:
            category = "armor"
        
        player.inventory.add_item(category, item_id, quantity)
        
        self.update_relationship(2)
        
        result["success"] = True
        result["message"] = f"Куплено {quantity} x {item['name']} за {total_price} монет"
        result["price"] = total_price
        result["item"] = item
        
        return result
    
    def reveal_secret(self, secret_id: str) -> Optional[Dict]:
        """Раскрытие секрета"""
        for secret in self.secrets:
            if secret["id"] == secret_id and not secret["revealed"]:
                secret["revealed"] = True
                self.update_relationship(10)
                return secret
        return None
    
    def add_rumor(self, rumor: str):
        """Добавление слуха"""
        self.rumors.append(rumor)
    
    def get_info(self) -> Dict[str, Any]:
        """Получение информации о NPC"""
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "gender": self.gender,
            "profession": self.profession,
            "personality": self.personality,
            "age": self.age,
            "relationship": self.relationship,
            "relationship_status": self.get_relationship_status(),
            "location": self.location,
            "is_merchant": self.is_merchant,
            "is_alive": self.is_alive,
            "is_quest_giver": self.is_quest_giver,
            "appearance": self.appearance,
            "traits": self.traits,
            "money": self.money
        }
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь для сохранения"""
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "gender": self.gender,
            "profession": self.profession,
            "personality": self.personality,
            "age": self.age,
            "relationship": self.relationship,
            "location": self.location,
            "home_location": self.home_location,
            "money": self.money,
            "is_merchant": self.is_merchant,
            "inventory": self.inventory,
            "trade_goods": self.trade_goods,
            "dialog": self.dialog,
            "secrets": self.secrets,
            "gossip": self.gossip,
            "rumors": self.rumors,
            "is_alive": self.is_alive,
            "is_busy": self.is_busy,
            "is_quest_giver": self.is_quest_giver,
            "quests_available": self.quests_available,
            "appearance": self.appearance,
            "schedule": self.schedule,
            "current_activity": self.current_activity,
            "family": self.family,
            "friends": self.friends,
            "enemies": self.enemies,
            "employer": self.employer,
            "skills": self.skills,
            "traits": self.traits,
            "history": self.history,
            "known_locations": self.known_locations
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'NPC':
        """Загрузка из словаря"""
        npc = cls(
            data["id"],
            data["name"],
            data["race"],
            data["gender"],
            data["profession"],
            data["personality"]
        )
        
        # Загрузка всех полей
        npc.age = data.get("age", random.randint(16, 80))
        npc.relationship = data.get("relationship", 0)
        npc.location = data.get("location", "городская_площадь")
        npc.home_location = data.get("home_location", npc.location)
        npc.money = data.get("money", random.randint(10, 500))
        npc.is_merchant = data.get("is_merchant", False)
        npc.inventory = data.get("inventory", {})
        npc.trade_goods = data.get("trade_goods", {})
        npc.dialog = data.get("dialog", npc.generate_dialog())
        npc.secrets = data.get("secrets", [])
        npc.gossip = data.get("gossip", [])
        npc.rumors = data.get("rumors", [])
        npc.is_alive = data.get("is_alive", True)
        npc.is_busy = data.get("is_busy", False)
        npc.is_quest_giver = data.get("is_quest_giver", False)
        npc.quests_available = data.get("quests_available", [])
        npc.appearance = data.get("appearance", npc.generate_appearance())
        npc.schedule = data.get("schedule", npc.generate_schedule())
        npc.current_activity = data.get("current_activity", "отдых")
        npc.family = data.get("family", [])
        npc.friends = data.get("friends", [])
        npc.enemies = data.get("enemies", [])
        npc.employer = data.get("employer")
        npc.skills = data.get("skills", npc.generate_skills())
        npc.traits = data.get("traits", npc.generate_traits())
        npc.history = data.get("history", npc.generate_history())
        npc.known_locations = data.get("known_locations", [npc.location])
        
        return npc
    #добавлены новые диалоги для нпс, так же добавлены расширенные
    #возмоности