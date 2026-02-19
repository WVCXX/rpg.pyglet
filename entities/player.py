class Player:
    def __init__(self, game_state):
        self.data = game_state["player"] if isinstance(game_state, dict) else game_state.player
    
    def take_damage(self, damage):
        self.data["health"] -= damage
        if self.data["health"] < 0:
            self.data["health"] = 0
        return damage
    
    def heal(self, amount):
        self.data["health"] = min(self.data["max_health"], self.data["health"] + amount)
    
    def add_money(self, amount):
        self.data["money"] += amount
    
    def remove_money(self, amount):
        if self.data["money"] >= amount:
            self.data["money"] -= amount
            return True
        return False
    
    def add_item(self, category, item):
        if category in self.data["inventory"]:
            self.data["inventory"][category].append(item)
            return True
        return False
    
    def get_damage(self):
        base = 5 + self.data["stats"]["strength"] * 2
        if "ржавый меч" in self.data["inventory"]["weapons"]:
            return base + 3
        return base