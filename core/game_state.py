class GameState:
    def __init__(self):
        self.player = self.create_player()
        self.current_location = "town_square"
        self.game_running = True
        
    def create_player(self):
        return {
            "name": "Джериан",
            "health": 100,
            "max_health": 100,
            "stamina": 100,
            "mana": 50,
            "max_mana": 50,
            "money": 50,
            "exp": 0,
            "level": 1,
            "stats": {
                "strength": 8,
                "dexterity": 8,
                "intelligence": 8,
                "wisdom": 8,
                "charisma": 8,
                "luck": 8
            },
            "skills": {},
            "inventory": {
                "weapons": ["ржавый меч"],
                "armor": ["старая куртка"],
                "potions": [],
                "books": [],
                "ingredients": [],
                "keys": [],
                "misc": ["фляга", "веревка", "огниво"]
            },
            "reputation": {},
            "relationships": {},
            "flags": {},
            "curses": [],
            "blessings": [],
            "diseases": [],
            "injuries": []
        }