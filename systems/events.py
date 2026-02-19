import random

class RandomEventGenerator:
    """Генератор случайных событий"""
    def __init__(self):
        self.events = [
            {
                "name": "Карманник",
                "type": "negative",
                "chance": 10,
                "text": "Карманник украл {} монет!",
                "effect": lambda p: p["money"] - random.randint(5, 20)
            },
            {
                "name": "Находка",
                "type": "positive",
                "chance": 15,
                "text": "Ты нашел {} монет!",
                "effect": lambda p: p["money"] + random.randint(1, 10)
            },
            {
                "name": "Несчастный случай",
                "type": "danger",
                "chance": 5,
                "text": "На тебя упал камень! -{} здоровья",
                "effect": lambda p: p["health"] - random.randint(10, 30)
            },
            {
                "name": "Нищий",
                "type": "choice",
                "chance": 20,
                "text": "Нищий просит милостыню. Дать 5 монет?",
                "choices": [
                    {"text": "Дать", "effect": lambda p: (p["money"] - 5, p["reputation"]["peasants"] + 2)},
                    {"text": "Отказать", "effect": lambda p: (p["reputation"]["peasants"] - 1,)}
                ]
            }
        ]
    
    def get_random_event(self):
        """Получение случайного события"""
        if random.randint(1, 100) <= 10:
            return random.choice(self.events)
        return None


class AccidentGenerator:
    """Генератор несчастных случаев"""
    def __init__(self):
        self.accidents = [
            "поскользнулся на гнилых досках - сломал ногу",
            "отравился несвежей едой",
            "подрался с пьяным стражником",
            "упал в открытый люк",
            "наступил на грабли",
            "укусила бешеная собака"
        ]
    
    def generate_accident(self):
        """Генерация несчастного случая"""
        return random.choice(self.accidents)