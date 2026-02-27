import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class DynamicWorld:
    """Динамический мир с временем, погодой и событиями"""
    def __init__(self):
        self.day = 1
        self.month = 1
        self.year = 1256
        self.hour = 8
        self.minute = 0
        
        self.season = self.get_season()  #ПЕРЕНЕСЕНО НАВЕРХ
        
        self.weather = self.generate_weather()
        self.weather_duration = random.randint(3, 12)  # часы
        self.weather_history = []
        
        self.time_of_day = self.get_time_of_day()
        
        self.month_names = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
        
        self.day_names = [
            "Понедельник", "Вторник", "Среда", "Четверг", 
            "Пятница", "Суббота", "Воскресенье"
        ]
        
        self.holidays = self.init_holidays()
        
        self.global_events = []
        self.active_events = []
        

        self.moon_phase = random.randint(0, 3)  # 0-новолуние, 1-растущая, 2-полнолуние, 3-убывающая
        

        self.temperature = self.calculate_temperature()

        self.wind = self.generate_wind()
        

        self.visibility = self.calculate_visibility()
    
    def init_holidays(self) -> Dict[int, str]:
        """Инициализация праздников"""
        return {
            1: "Новый год",
            15: "День Единого",
            45: "Праздник весны",
            100: "День памяти",
            150: "Летнее солнцестояние",
            200: "День урожая",
            250: "Осеннее равноденствие",
            300: "День мертвых",
            350: "Зимнее солнцестояние"
        }
    
    def generate_weather(self) -> str:
        """Генерация погоды"""
        weathers = [
            "ясно", "облачно", "пасмурно", "дождь", "ливень",
            "гроза", "туман", "снег", "метель", "град",
            "морось", "ветрено", "штиль"
        ]
        
        if self.season == "зима":
            weights = [1, 2, 3, 1, 1, 0, 2, 4, 3, 1, 1, 2, 1]
        elif self.season == "весна":
            weights = [2, 3, 3, 4, 2, 1, 3, 0, 0, 0, 3, 2, 1]
        elif self.season == "лето":
            weights = [4, 3, 2, 2, 1, 3, 1, 0, 0, 0, 1, 2, 1]
        else:  # осень
            weights = [2, 3, 4, 3, 2, 1, 3, 1, 1, 0, 2, 3, 1]
        
        return random.choices(weathers, weights=weights)[0]
    
    def generate_wind(self) -> Dict:
        """Генерация ветра"""
        directions = ["северный", "южный", "западный", "восточный", 
                     "северо-западный", "северо-восточный", "юго-западный", "юго-восточный"]
        
        strengths = ["штиль", "слабый", "умеренный", "сильный", "штормовой"]
        
        return {
            "direction": random.choice(directions),
            "strength": random.choice(strengths),
            "speed": random.randint(0, 30)
        }
    
    def calculate_temperature(self) -> int:
        """Расчет температуры"""
        base_temp = {
            "зима": -10,
            "весна": 10,
            "лето": 25,
            "осень": 10
        }.get(self.season, 10)
        
        hour_mod = 0
        if self.hour < 6 or self.hour > 20:
            hour_mod = -5
        elif self.hour > 10 and self.hour < 16:
            hour_mod = 5
        
        weather_mod = {
            "ясно": 2,
            "облачно": 0,
            "пасмурно": -2,
            "дождь": -3,
            "ливень": -5,
            "гроза": -2,
            "туман": -1,
            "снег": -5,
            "метель": -8,
            "град": -4
        }.get(self.weather, 0)
        
        return base_temp + hour_mod + weather_mod + random.randint(-2, 2)
    
    def calculate_visibility(self) -> int:
        """Расчет видимости (в метрах)"""
        base = 1000
        
        # время суток
        if self.hour < 6 or self.hour > 20:
            base = 200  # ночь
        
        # погода
        weather_vis = {
            "ясно": 1.0,
            "облачно": 0.8,
            "пасмурно": 0.6,
            "дождь": 0.5,
            "ливень": 0.3,
            "гроза": 0.4,
            "туман": 0.2,
            "снег": 0.4,
            "метель": 0.2,
            "град": 0.5
        }.get(self.weather, 0.7)
        
        return int(base * weather_vis)
    
    def get_season(self) -> str:
        """Определение сезона по дате"""
        day_of_year = self.day
        if day_of_year <= 80:
            return "зима"
        elif day_of_year <= 170:
            return "весна"
        elif day_of_year <= 260:
            return "лето"
        elif day_of_year <= 350:
            return "осень"
        else:
            return "зима"
    
    def get_time_of_day(self) -> str:
        """Определение времени суток"""
        if 6 <= self.hour < 12:
            return "утро"
        elif 12 <= self.hour < 18:
            return "день"
        elif 18 <= self.hour < 22:
            return "вечер"
        else:
            return "ночь"
    
    def advance_time(self, minutes: int = 60):
        """Продвижение времени"""
        self.minute += minutes
        
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1
            
            if self.day > 360:
                self.day = 1
                self.year += 1
            
            self.month = (self.day // 30) + 1
            self.season = self.get_season()
            self.daily_update()
        
        self.weather_duration -= 1
        if self.weather_duration <= 0:
            self.weather = self.generate_weather()
            self.weather_duration = random.randint(3, 12)
        
        self.time_of_day = self.get_time_of_day()
        self.temperature = self.calculate_temperature()
        self.visibility = self.calculate_visibility()
        
        if self.day % 7 == 0 and self.minute == 0:
            self.moon_phase = (self.moon_phase + 1) % 4
    
    def daily_update(self):
        """Ежедневное обновление"""
        if self.day in self.holidays:
            self.active_events.append({
                "type": "holiday",
                "name": self.holidays[self.day],
                "day": self.day
            })
        
        if random.random() < 0.1:
            self.generate_global_event()
        
        self.active_events = [e for e in self.active_events if e.get("duration", 1) > 0]
        for event in self.active_events:
            if "duration" in event:
                event["duration"] -= 1
    
    def generate_global_event(self):
        """Генерация глобального события"""
        events = [
            {
                "name": "Война",
                "description": "В королевстве началась война",
                "effects": {"цены": 2.0, "опасность": 1.5},
                "duration": random.randint(30, 90)
            },
            {
                "name": "Эпидемия",
                "description": "Город охватила эпидемия",
                "effects": {"здоровье": 0.7, "цены": 1.3},
                "duration": random.randint(20, 60)
            },
            {
                "name": "Урожай",
                "description": "Богатый урожай в этом году",
                "effects": {"цены": 0.7, "настроение": 1.2},
                "duration": random.randint(15, 30)
            },
            {
                "name": "Фестиваль",
                "description": "В городе проходит фестиваль",
                "effects": {"настроение": 1.5, "цены": 1.1},
                "duration": random.randint(3, 7)
            },
            {
                "name": "Нашествие монстров",
                "description": "Монстры атакуют окрестности",
                "effects": {"опасность": 2.0, "цены": 1.2},
                "duration": random.randint(10, 30)
            },
            {
                "name": "Визит короля",
                "description": "Король посещает город",
                "effects": {"настроение": 1.3, "цены": 1.5},
                "duration": random.randint(3, 5)
            }
        ]
        
        event = random.choice(events).copy()
        event["start_day"] = self.day
        self.active_events.append(event)
    
    def get_holiday(self) -> Optional[str]:
        """Получение праздника в текущий день"""
        return self.holidays.get(self.day)
    
    def get_moon_phase_name(self) -> str:
        """Получение названия фазы луны"""
        phases = ["новолуние", "растущая луна", "полнолуние", "убывающая луна"]
        return phases[self.moon_phase]
    
    def get_date_string(self) -> str:
        """Получение строки с датой"""
        day_name = self.day_names[(self.day - 1) % 7]
        month_name = self.month_names[self.month - 1]
        return f"{day_name}, {self.day} {month_name} {self.year} года"
    
    def get_time_string(self) -> str:
        """Получение строки с временем"""
        return f"{self.hour:02d}:{self.minute:02d}"
    
    def get_full_time_string(self) -> str:
        """Получение полной строки с временем"""
        time_str = self.get_time_string()
        date_str = self.get_date_string()
        return f"{date_str}, {time_str}"
    
    def get_weather_string(self) -> str:
        """Получение строки с погодой"""
        weather_icons = {
            "ясно": "☀",
            "облачно": "⛅",
            "пасмурно": "☁",
            "дождь": "🌧",
            "ливень": "🌊",
            "гроза": "⚡",
            "туман": "🌫",
            "снег": "❄",
            "метель": "🌨",
            "град": "🌩",
            "морось": "💧",
            "ветрено": "💨",
            "штиль": "🍃"
        }
        
        icon = weather_icons.get(self.weather, "☀")
        temp_sign = "+" if self.temperature > 0 else ""
        
        return f"{icon} {self.weather.capitalize()}, {temp_sign}{self.temperature}°C"
    
    def get_wind_string(self) -> str:
        """Получение строки с ветром"""
        return f"{self.wind['direction']} ветер, {self.wind['strength']}"
    
    def get_visibility_string(self) -> str:
        """Получение строки с видимостью"""
        if self.visibility > 800:
            return "Отличная видимость"
        elif self.visibility > 500:
            return "Хорошая видимость"
        elif self.visibility > 200:
            return "Средняя видимость"
        else:
            return "Плохая видимость"
    
    def get_event_effects(self) -> Dict:
        """Получение суммарных эффектов от событий"""
        effects = {
            "цены": 1.0,
            "опасность": 1.0,
            "здоровье": 1.0,
            "настроение": 1.0
        }
        
        for event in self.active_events:
            for key, value in event.get("effects", {}).items():
                if key in effects:
                    effects[key] *= value
        
        return effects
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "hour": self.hour,
            "minute": self.minute,
            "weather": self.weather,
            "season": self.season,
            "moon_phase": self.moon_phase,
            "temperature": self.temperature,
            "wind": self.wind,
            "active_events": self.active_events,
            "weather_history": self.weather_history[-10:]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DynamicWorld':
        """Загрузка из словаря"""
        world = cls()
        world.day = data.get("day", 1)
        world.month = data.get("month", 1)
        world.year = data.get("year", 1256)
        world.hour = data.get("hour", 8)
        world.minute = data.get("minute", 0)
        world.weather = data.get("weather", "ясно")
        world.season = data.get("season", world.get_season())
        world.moon_phase = data.get("moon_phase", 0)
        world.temperature = data.get("temperature", 10)
        world.wind = data.get("wind", world.generate_wind())
        world.active_events = data.get("active_events", [])
        world.weather_history = data.get("weather_history", [])
        return world