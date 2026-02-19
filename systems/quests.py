import random
from datetime import datetime

class QuestSystem:
    """Система квестов"""
    def __init__(self):
        self.quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.failed_quests = []
    
    def generate_quest(self, quest_type="random"):
        """Генерация случайного квеста"""
        templates = {
            "hunt": {
                "name": "Охота на {}",
                "description": "В округе завелся {}",
                "targets": ["волкодлак", "упырь", "виверна", "грифон"],
                "reward_min": 100,
                "reward_max": 500
            },
            "delivery": {
                "name": "Доставка {}",
                "description": "Нужно доставить {} в {}",
                "targets": ["вино", "оружие", "свитки", "лекарства"],
                "locations": ["столица", "порт", "монастырь"],
                "reward_min": 30,
                "reward_max": 100
            },
            "rescue": {
                "name": "Спасение {}",
                "description": "Пропал {}",
                "targets": ["ребенок", "купец", "крестьянин"],
                "reward_min": 50,
                "reward_max": 300
            }
        }
        
        template = random.choice(list(templates.values()))
        
        quest = {
            "id": f"quest_{len(self.quests) + 1}",
            "name": template["name"].format(random.choice(template.get("targets", [""]))),
            "description": template["description"].format(
                random.choice(template.get("targets", [""])),
                random.choice(template.get("locations", [""])) if "locations" in template else ""
            ),
            "stage": 0,
            "stages": ["start", "find", "complete", "return"],
            "reward": random.randint(template["reward_min"], template["reward_max"]),
            "start_day": 1,
            "time_limit": random.randint(3, 10)
        }
        
        self.quests[quest["id"]] = quest
        return quest
    
    def to_dict(self):
        """Конвертация в словарь"""
        return {
            "quests": self.quests,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests,
            "failed_quests": self.failed_quests
        }
    
    @classmethod
    def from_dict(cls, data):
        """Загрузка из словаря"""
        system = cls()
        system.quests = data["quests"]
        system.active_quests = data["active_quests"]
        system.completed_quests = data["completed_quests"]
        system.failed_quests = data["failed_quests"]
        return system