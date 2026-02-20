import random
from typing import Dict, List, Any


class ItemStackContainer:
    """Контейнер для предметов со стаками"""
    def __init__(self, name: str, max_stack: int):
        self.name = name
        self.max_stack = max_stack
        self._items: Dict[str, int] = {}  
    
    def add(self, item: str, count: int = 1) -> bool:
        """Добавление предмета"""
        if count <= 0:
            return False
        
        current = self._items.get(item, 0)
        new_count = current + count
        
        if new_count > self.max_stack:
            return False
        
        self._items[item] = new_count
        return True
    
    def remove(self, item: str, count: int = 1) -> bool:
        """Удаление предмета"""
        if count <= 0:
            return False
        
        current = self._items.get(item, 0)
        if current < count:
            return False
        
        new_count = current - count
        if new_count <= 0:
            del self._items[item]
        else:
            self._items[item] = new_count
        
        return True
    
    def get_count(self, item: str) -> int:
        """Получение количества"""
        return self._items.get(item, 0)
    
    def get_all(self) -> List[tuple]:
        """Получение всех предметов"""
        return [(item, count) for item, count in self._items.items()]
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return self._items.copy()
    
    def from_dict(self, data: Dict):
        """Загрузка из словаря"""
        self._items = data.copy()


class Inventory:
    """Система инвентаря - доступ только через методы"""
    MAX_STACK = 128
    
    def __init__(self):
        self._weapons = ItemStackContainer("weapons", 1)
        self._armor = ItemStackContainer("armor", 1)
        self._potions = ItemStackContainer("potions", self.MAX_STACK)
        self._books = ItemStackContainer("books", 1)
        self._ingredients = ItemStackContainer("ingredients", self.MAX_STACK)
        self._keys = ItemStackContainer("keys", 1)
        self._misc = ItemStackContainer("misc", self.MAX_STACK)
    
    @property
    def weapons(self):
        return self._weapons.get_all()
    
    @property
    def armor(self):
        return self._armor.get_all()
    
    @property
    def potions(self):
        return self._potions.get_all()
    
    @property
    def books(self):
        return self._books.get_all()
    
    @property
    def ingredients(self):
        return self._ingredients.get_all()
    
    @property
    def keys(self):
        return self._keys.get_all()
    
    @property
    def misc(self):
        return self._misc.get_all()
    
    def add_item(self, category: str, item: str, count: int = 1) -> bool:
        """Добавление предмета"""
        container = self._get_container(category)
        if container:
            return container.add(item, count)
        return False
    
    def remove_item(self, category: str, item: str, count: int = 1) -> bool:
        """Удаление предмета"""
        container = self._get_container(category)
        if container:
            return container.remove(item, count)
        return False
    
    def get_item_count(self, category: str, item: str) -> int:
        """Получение количества"""
        container = self._get_container(category)
        if container:
            return container.get_count(item)
        return 0
    
    def get_all_items(self) -> Dict[str, List[tuple]]:
        """Получение всех предметов"""
        result = {}
        categories = {
            "weapons": self._weapons,
            "armor": self._armor,
            "potions": self._potions,
            "books": self._books,
            "ingredients": self._ingredients,
            "keys": self._keys,
            "misc": self._misc
        }
        
        for cat_name, container in categories.items():
            items = container.get_all()
            if items:
                result[cat_name] = items
        
        return result
    
    def _get_container(self, category: str):
        """Получение контейнера по категории"""
        containers = {
            "weapons": self._weapons,
            "armor": self._armor,
            "potions": self._potions,
            "books": self._books,
            "ingredients": self._ingredients,
            "keys": self._keys,
            "misc": self._misc
        }
        return containers.get(category)
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        return {
            "weapons": self._weapons.to_dict(),
            "armor": self._armor.to_dict(),
            "potions": self._potions.to_dict(),
            "books": self._books.to_dict(),
            "ingredients": self._ingredients.to_dict(),
            "keys": self._keys.to_dict(),
            "misc": self._misc.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Inventory':
        """Загрузка из словаря"""
        inv = cls()
        for category, items_data in data.items():
            container = inv._get_container(category)
            if container:
                if isinstance(items_data, dict):
                    container.from_dict(items_data)
        return inv


class GameState:
    def __init__(self, player_name: str = "Джериан"):
        self.player = self.create_player(player_name)
        self.current_location = "городская_площадь"
        self.game_running = True
        self.play_time = 0
        self.game_version = "1.0.0"
    
    def create_player(self, name: str) -> Dict:
        """Создание игрока"""
        return {
            "name": name,
            "health": 100,
            "max_health": 100,
            "stamina": 100,
            "max_stamina": 100,
            "mana": 50,
            "max_mana": 50,
            "money": 50,
            "exp": 0,
            "level": 1,
            "stat_points": 0,
            "stats": {
                "сила": 8,
                "ловкость": 8,
                "интеллект": 8,
                "мудрость": 8,
                "харизма": 8,
                "удача": 8
            },
            "skills": {},
            "inventory": Inventory(),
            "reputation": {
                "крестьяне": 0,
                "знать": 0,
                "торговцы": 0,
                "стража": 0,
                "церковь": 0,
                "воры": 0
            },
            "relationships": {},
            "flags": {},
            "curses": [],
            "blessings": [],
            "diseases": [],
            "injuries": [],
            "achievements": [],
            "death_count": 0
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GameState':
        """Загрузка из словаря"""
        state = cls()
        for key, value in data.items():
            if key == "player" and isinstance(value, dict):
                state.player = value
                if "inventory" in value and isinstance(value["inventory"], dict):
                    state.player["inventory"] = Inventory.from_dict(value["inventory"])
            else:
                setattr(state, key, value)
        return state
    
    def to_dict(self) -> Dict:
        """Конвертация в словарь"""
        result = self.__dict__.copy()
        result["player"] = self.player.copy()
        result["player"]["inventory"] = self.player["inventory"].to_dict()
        return result

#добавлены стаки а так же добавлена возможность более подробно
#создавать персонажа