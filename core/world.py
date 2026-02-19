# core/world.py
import random

class DynamicWorld:
    def __init__(self):
        self.day = 1
        self.hour = 12
        self.minute = 0
        self.weather = self.generate_weather()
        self.season = self.get_season()
        
    def generate_weather(self):
        weathers = ["ясно", "облачно", "дождь", "гроза", "туман", "снег"]
        return random.choice(weathers)
    
    def get_season(self):
        month = (self.day // 30) % 12 + 1
        if month in [12, 1, 2]:
            return "зима"
        elif month in [3, 4, 5]:
            return "весна"
        elif month in [6, 7, 8]:
            return "лето"
        else:
            return "осень"
    
    def advance_time(self, minutes=60):
        self.minute += minutes
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1
            self.weather = self.generate_weather()
            self.season = self.get_season()