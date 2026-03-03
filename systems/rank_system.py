import random
from typing import Dict, List, Optional

class RankSystem:
    """Система рангов и титулов"""
    
    RANKS = [
        {"name": "Новичок", "points": 0, "color": "#888888"},
        {"name": "Ученик", "points": 100, "color": "#00aa00"},
        {"name": "Подмастерье", "points": 300, "color": "#00ff00"},
        {"name": "Мастер", "points": 600, "color": "#0000ff"},
        {"name": "Эксперт", "points": 1000, "color": "#aa00aa"},
        {"name": "Ветеран", "points": 1500, "color": "#ffaa00"},
        {"name": "Герой", "points": 2200, "color": "#ff0000"},
        {"name": "Легенда", "points": 3000, "color": "#ffd700"},
        {"name": "Миф", "points": 4000, "color": "#ffffff"},
        {"name": "Бог", "points": 5000, "color": "#ff00ff"}
    ]
    
    TITLES = {
        "убийца_монстров": {
            "name": "Убийца монстров",
            "requirement": {"enemies_killed": 50},
            "color": "#ff4444",
            "description": "Убито 50 врагов"
        },
        "миллионер": {
            "name": "Миллионер",
            "requirement": {"gold_collected": 10000},
            "color": "#ffd700",
            "description": "Собрано 10000 золота"
        },
        "исследователь": {
            "name": "Исследователь",
            "requirement": {"locations_visited": 10},
            "color": "#00ff00",
            "description": "Посещено 10 локаций"
        },
        "герой": {
            "name": "Герой",
            "requirement": {"quests_completed": 20},
            "color": "#ffaa00",
            "description": "Выполнено 20 квестов"
        },
        "бессмертный": {
            "name": "Бессмертный",
            "requirement": {"deaths": 0, "level": 10},
            "color": "#ffffff",
            "description": "Достичь 10 уровня без смертей"
        },
        "кровавый_барон": {
            "name": "Кровавый барон",
            "requirement": {"enemies_killed": 200},
            "color": "#ff0000",
            "description": "Убито 200 врагов"
        },
        "книгочей": {
            "name": "Книгочей",
            "requirement": {"books_read": 20},
            "color": "#8888ff",
            "description": "Прочитано 20 книг"
        },
        "алхимик": {
            "name": "Алхимик",
            "requirement": {"potions_brewed": 30},
            "color": "#00ff00",
            "description": "Сварено 30 зелий"
        },
        "кузнец": {
            "name": "Кузнец",
            "requirement": {"items_crafted": 50},
            "color": "#ff8800",
            "description": "Создано 50 предметов"
        },
        "романтик": {
            "name": "Романтик",
            "requirement": {"relationships": 5},
            "color": "#ff69b4",
            "description": "Завести 5 романтических отношений"
        },
        "семьянин": {
            "name": "Семьянин",
            "requirement": {"children": 3},
            "color": "#ffaa00",
            "description": "Иметь 3 детей"
        },
        "безумец": {
            "name": "Безумец",
            "requirement": {"death_count": 10},
            "color": "#8b00ff",
            "description": "Умереть 10 раз"
        },
        "счастливчик": {
            "name": "Счастливчик",
            "requirement": {"luck_events": 20},
            "color": "#ffff00",
            "description": "Пережить 20 случайных событий"
        },
        "авантюрист": {
            "name": "Авантюрист",
            "requirement": {"dungeons_cleared": 10},
            "color": "#00ffff",
            "description": "Очищено 10 подземелий"
        },
        "миротворец": {
            "name": "Миротворец",
            "requirement": {"reputation": {"все": 50}},
            "color": "#ffffff",
            "description": "Достичь 50 репутации во всех фракциях"
        }
    }
    
    def __init__(self, player, game_state):
        self.player = player
        self.game_state = game_state
        self.rank_points = game_state.rank_points
        self.current_rank = game_state.rank
        self.titles = player.get("titles", [])
        self.current_title = player.get("current_title", "Новичок")
        
        # Статистика для титулов
        self.stats = {
            "enemies_killed": 0,
            "gold_collected": 0,
            "locations_visited": 1,
            "quests_completed": 0,
            "deaths": 0,
            "books_read": 0,
            "potions_brewed": 0,
            "items_crafted": 0,
            "relationships": 0,
            "children": 0,
            "luck_events": 0,
            "dungeons_cleared": 0
        }
    
    def add_rank_points(self, points: int):
        """Добавление очков ранга"""
        self.rank_points += points
        self.check_rank_up()
    
    def check_rank_up(self) -> Optional[str]:
        """Проверка повышения ранга"""
        new_rank = self.current_rank
        new_rank_color = "#888888"
        
        for rank in self.RANKS:
            if self.rank_points >= rank["points"]:
                new_rank = rank["name"]
                new_rank_color = rank["color"]
            else:
                break
        
        if new_rank != self.current_rank:
            self.current_rank = new_rank
            self.game_state.rank = new_rank
            return f"✨ ПОВЫШЕНИЕ РАНГА! Теперь ты {new_rank}!"
        
        return None
    
    def check_titles(self) -> List[str]:
        """Проверка получения новых титулов"""
        new_titles = []
        
        for title_id, title_data in self.TITLES.items():
            if title_id in self.titles:
                continue
            
            requirements = title_data["requirement"]
            met = True
            
            for req, value in requirements.items():
                if req in self.stats:
                    if self.stats[req] < value:
                        met = False
                        break
                elif req in self.player:
                    if self.player[req] < value:
                        met = False
                        break
                elif req == "reputation":
                    # Проверка репутации
                    rep = self.player.get("reputation", {})
                    for faction, val in value.items():
                        if faction == "все":
                            # Проверяем все репутации
                            for f in rep:
                                if rep[f] < val:
                                    met = False
                                    break
                        else:
                            if rep.get(faction, 0) < val:
                                met = False
                                break
            
            if met:
                self.titles.append(title_id)
                self.player["titles"].append(title_id)
                new_titles.append(title_data["name"])
        
        return new_titles
    
    def update_stat(self, stat: str, value: int = 1):
        """Обновление статистики"""
        if stat in self.stats:
            self.stats[stat] += value
            
            # Проверка титулов при обновлении
            new_titles = self.check_titles()
            return new_titles
        
        return []
    
    def get_rank_info(self) -> Dict:
        """Получение информации о ранге"""
        current_index = 0
        next_rank = None
        points_needed = 0
        
        for i, rank in enumerate(self.RANKS):
            if rank["name"] == self.current_rank:
                current_index = i
                if i < len(self.RANKS) - 1:
                    next_rank = self.RANKS[i + 1]
                    points_needed = next_rank["points"] - self.rank_points
                break
        
        return {
            "current_rank": self.current_rank,
            "current_color": self.RANKS[current_index]["color"],
            "rank_points": self.rank_points,
            "next_rank": next_rank["name"] if next_rank else None,
            "points_needed": points_needed,
            "progress": (self.rank_points / self.RANKS[current_index + 1]["points"] * 100) if next_rank else 100
        }
    
    def get_available_titles(self) -> List[Dict]:
        """Получение всех титулов с информацией"""
        result = []
        
        for title_id, title_data in self.TITLES.items():
            unlocked = title_id in self.titles
            result.append({
                "id": title_id,
                "name": title_data["name"],
                "description": title_data["description"],
                "color": title_data["color"],
                "unlocked": unlocked
            })
        
        return result
    
    def set_current_title(self, title_id: str) -> bool:
        """Установка текущего титула"""
        if title_id in self.titles:
            self.current_title = self.TITLES[title_id]["name"]
            self.player["current_title"] = self.current_title
            return True
        return False
    
    def to_dict(self) -> Dict:
        """Сохранение в словарь"""
        return {
            "rank_points": self.rank_points,
            "current_rank": self.current_rank,
            "titles": self.titles,
            "current_title": self.current_title,
            "stats": self.stats
        }
    
    @classmethod
    def from_dict(cls, data: Dict, player, game_state) -> 'RankSystem':
        """Загрузка из словаря"""
        system = cls(player, game_state)
        system.rank_points = data.get("rank_points", 0)
        system.current_rank = data.get("current_rank", "Новичок")
        system.titles = data.get("titles", [])
        system.current_title = data.get("current_title", "Новичок")
        system.stats = data.get("stats", system.stats)
        return system