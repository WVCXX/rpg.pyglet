import pickle
import os
import json
from datetime import datetime
from typing import Optional, Tuple, List, Any, Dict 
import zlib
import base64

class SaveSystem:
    """Улучшенная система сохранения с компрессией и метаданными"""
    SAVE_DIR = "saves"
    BACKUP_DIR = "saves/backups"
    MAX_SAVES = 20  # максимальное количество сохранений
    
    @classmethod
    def ensure_dir(cls):
        """Создание директорий"""
        os.makedirs(cls.SAVE_DIR, exist_ok=True)
        os.makedirs(cls.BACKUP_DIR, exist_ok=True)
    
    @classmethod
    def save_game(cls, game_state, world, market, quest_system, stats, 
                  filename: Optional[str] = None, compress: bool = True) -> Tuple[bool, str]:
        """Сохранение игры с компрессией"""
        cls.ensure_dir()
        cls._cleanup_old_saves()
        
        if not filename:
            filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sav"
        
        filepath = os.path.join(cls.SAVE_DIR, filename)
        
        save_data = {
            "game_state": game_state.to_dict() if hasattr(game_state, 'to_dict') else game_state.__dict__,
            "world": world.__dict__,
            "market": market.__dict__,
            "quest_system": quest_system.to_dict(),
            "stats": stats,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "0.0.1",
                "player_name": game_state.player["name"],
                "player_level": game_state.player["level"],
                "location": game_state.current_location,
                "play_time": game_state.play_time
            }
        }
        
        try:
            data = pickle.dumps(save_data)
            
            if compress:
                data = zlib.compress(data)
            
            with open(filepath, 'wb') as f:
                f.write(data)
            
            backup_path = os.path.join(cls.BACKUP_DIR, f"backup_{filename}")
            with open(backup_path, 'wb') as f:
                f.write(data)
            
            return True, f"Сохранено в {filename}"
        except Exception as e:
            return False, str(e)
    
    @classmethod
    def load_game(cls, filename: str, compressed: bool = True) -> Tuple[bool, Any]:
        """Загрузка игры с распаковкой"""
        cls.ensure_dir()
        filepath = os.path.join(cls.SAVE_DIR, filename)
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            if compressed:
                try:
                    data = zlib.decompress(data)
                except zlib.error:
                    pass
            
            return True, pickle.loads(data)
        except Exception as e:
            backup_path = os.path.join(cls.BACKUP_DIR, f"backup_{filename}")
            if os.path.exists(backup_path):
                try:
                    with open(backup_path, 'rb') as f:
                        data = f.read()
                    if compressed:
                        try:
                            data = zlib.decompress(data)
                        except:
                            pass
                    return True, pickle.loads(data)
                except:
                    pass
            return False, str(e)
    
    @classmethod
    def get_saves(cls) -> List[Dict]:
        """Получение списка сохранений с метаданными"""
        cls.ensure_dir()
        saves = []
        
        for filename in os.listdir(cls.SAVE_DIR):
            if filename.endswith('.sav'):
                filepath = os.path.join(cls.SAVE_DIR, filename)
                mtime = os.path.getmtime(filepath)
                
                metadata = cls._read_metadata(filepath)
                
                saves.append({
                    "filename": filename,
                    "date": datetime.fromtimestamp(mtime),
                    "size": os.path.getsize(filepath),
                    "metadata": metadata
                })
        
        return sorted(saves, key=lambda x: x["date"], reverse=True)
    
    @classmethod
    def _read_metadata(cls, filepath: str) -> Dict:
        """Чтение метаданных из сохранения"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            try:
                data = zlib.decompress(data)
            except:
                pass
            
            save_data = pickle.loads(data)
            return save_data.get("metadata", {})
        except:
            return {}
    
    @classmethod
    def _cleanup_old_saves(cls):
        """Очистка старых сохранений"""
        saves = cls.get_saves()
        if len(saves) > cls.MAX_SAVES:
            for save in saves[cls.MAX_SAVES:]:
                try:
                    os.remove(os.path.join(cls.SAVE_DIR, save["filename"]))
                except:
                    pass
    
    @classmethod
    def delete_save(cls, filename: str) -> bool:
        """Удаление сохранения"""
        try:
            filepath = os.path.join(cls.SAVE_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                backup_path = os.path.join(cls.BACKUP_DIR, f"backup_{filename}")
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                
                return True
        except:
            pass
        return False
    #доработана система сохранений