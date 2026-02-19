import random

class MarketSystem:
    """Экономическая система"""
    def __init__(self):
        self.base_prices = {
            "iron": 10,
            "silver": 50,
            "gold": 200,
            "copper": 1,
            "leather": 5,
            "cloth": 3,
            "wood": 2,
            "stone": 4,
            "health_potion": 30,
            "mana_potion": 25,
            "sword": 100,
            "shield": 80,
            "bow": 60,
            "arrows": 1,
            "food": 2,
            "water": 1,
            "wine": 10,
            "book": 40,
            "candle": 5,
            "rope": 8
        }
        
        self.current_prices = self.base_prices.copy()
        self.shortage = None
        self.glut = None
        self.market_news = []
        self.tax_rate = 0.1
    
    def update_market(self):
        """Обновление цен"""
        for item in self.current_prices:
            fluctuation = random.uniform(0.8, 1.2)
            self.current_prices[item] = int(self.base_prices[item] * fluctuation)
        
        # Дефицит
        if random.random() < 0.3:
            self.shortage = random.choice(list(self.current_prices.keys()))
            self.current_prices[self.shortage] *= 3
            self.market_news.append(f"Дефицит {self.shortage}!")
        
        # Переизбыток
        if random.random() < 0.3:
            self.glut = random.choice(list(self.current_prices.keys()))
            self.current_prices[self.glut] = int(self.current_prices[self.glut] * 0.5)
            self.market_news.append(f"Переизбыток {self.glut}!")
    
    def get_price(self, item):
        """Получение цены"""
        return self.current_prices.get(item, 0)
    
    def can_afford(self, item, amount, money):
        """Проверка, хватает ли денег"""
        price = self.get_price(item) * amount * (1 + self.tax_rate)
        return money >= price, price