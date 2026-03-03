import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class JournalSystem:
    """Дневник приключений"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.journal = game_state.journal
        
        # Категории записей
        self.categories = {
            "quests": {"name": "📜 Квесты", "color": "#ffd700"},
            "discoveries": {"name": "🗺 Открытия", "color": "#00ff00"},
            "enemies": {"name": "👾 Бестиарий", "color": "#ff4444"},
            "items": {"name": "📦 Коллекция", "color": "#8888ff"},
            "notes": {"name": "📝 Заметки", "color": "#ffffff"}
        }
    
    def add_quest_entry(self, quest_name: str, description: str, status: str = "активен"):
        """Добавление записи о квесте"""
        entry = {
            "type": "quest",
            "name": quest_name,
            "description": description,
            "status": status,
            "date": self.get_current_date(),
            "time": self.get_current_time()
        }
        self.journal["quests"].append(entry)
        return entry
    
    def update_quest_status(self, quest_name: str, status: str):
        """Обновление статуса квеста"""
        for quest in self.journal["quests"]:
            if quest["name"] == quest_name:
                quest["status"] = status
                quest["completed_date"] = self.get_current_date()
                break
    
    def add_discovery(self, location: str, description: str):
        """Добавление открытия"""
        if location not in self.journal["discoveries"]:
            entry = {
                "location": location,
                "description": description,
                "date": self.get_current_date()
            }
            self.journal["discoveries"].append(entry)
            return entry
        return None
    
    def add_enemy_killed(self, enemy_name: str, level: int):
        """Добавление записи об убитом враге"""
        if enemy_name in self.journal["enemies_killed"]:
            self.journal["enemies_killed"][enemy_name] += 1
        else:
            self.journal["enemies_killed"][enemy_name] = 1
            
        return {
            "name": enemy_name,
            "count": self.journal["enemies_killed"][enemy_name],
            "level": level
        }
    
    def add_item_found(self, item_name: str, category: str):
        """Добавление найденного предмета"""
        entry = {
            "name": item_name,
            "category": category,
            "date": self.get_current_date()
        }
        
        # Проверяем, есть ли уже такой предмет
        for item in self.journal["items_found"]:
            if item["name"] == item_name:
                return None
        
        self.journal["items_found"].append(entry)
        return entry
    
    def add_note(self, title: str, content: str):
        """Добавление заметки"""
        entry = {
            "title": title,
            "content": content,
            "date": self.get_current_date(),
            "time": self.get_current_time()
        }
        self.journal["notes"].append(entry)
        return entry
    
    def get_current_date(self) -> str:
        """Получение текущей даты в игре"""
        world = self.game_state.world
        return f"{world.day}.{world.month}.{world.year}"
    
    def get_current_time(self) -> str:
        """Получение текущего времени в игре"""
        world = self.game_state.world
        return f"{world.hour:02d}:{world.minute:02d}"
    
    def get_quests_by_status(self, status: str) -> List[Dict]:
        """Получение квестов по статусу"""
        return [q for q in self.journal["quests"] if q["status"] == status]
    
    def get_enemy_stats(self) -> List[Dict]:
        """Получение статистики по врагам"""
        stats = []
        for enemy, count in self.journal["enemies_killed"].items():
            stats.append({
                "name": enemy,
                "count": count
            })
        return sorted(stats, key=lambda x: x["count"], reverse=True)
    
    def get_discoveries_by_location(self) -> Dict:
        """Получение открытий по локациям"""
        discoveries = {}
        for d in self.journal["discoveries"]:
            loc = d["location"]
            if loc not in discoveries:
                discoveries[loc] = []
            discoveries[loc].append(d)
        return discoveries
    
    def search_notes(self, query: str) -> List[Dict]:
        """Поиск по заметкам"""
        results = []
        for note in self.journal["notes"]:
            if query.lower() in note["title"].lower() or query.lower() in note["content"].lower():
                results.append(note)
        return results
    
    def export_journal(self, filename: str = "journal_export.json"):
        """Экспорт дневника в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.journal, f, ensure_ascii=False, indent=2)
        return f"Дневник экспортирован в {filename}"
    
    def get_statistics(self) -> Dict:
        """Получение общей статистики"""
        return {
            "total_quests": len(self.journal["quests"]),
            "completed_quests": len([q for q in self.journal["quests"] if q["status"] == "завершен"]),
            "total_discoveries": len(self.journal["discoveries"]),
            "total_enemies": sum(self.journal["enemies_killed"].values()),
            "unique_enemies": len(self.journal["enemies_killed"]),
            "unique_items": len(self.journal["items_found"]),
            "total_notes": len(self.journal["notes"])
        }