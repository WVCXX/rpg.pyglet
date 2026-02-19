# core/save_system.py
import pickle
import os
from datetime import datetime

class SaveSystem:
    SAVE_DIR = "saves"
    
    @classmethod
    def ensure_dir(cls):
        if not os.path.exists(cls.SAVE_DIR):
            os.makedirs(cls.SAVE_DIR)
    
    @classmethod
    def save_game(cls, game_state, world, filename=None):
        cls.ensure_dir()
        
        if not filename:
            filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sav"
        
        filepath = os.path.join(cls.SAVE_DIR, filename)
        
        save_data = {
            "game_state": game_state.__dict__,
            "world": world.__dict__,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(save_data, f)
            return True, f"Сохранено в {filename}"
        except Exception as e:
            return False, str(e)
    
    @classmethod
    def load_game(cls, filename):
        cls.ensure_dir()
        filepath = os.path.join(cls.SAVE_DIR, filename)
        
        try:
            with open(filepath, 'rb') as f:
                return True, pickle.load(f)
        except Exception as e:
            return False, str(e)
    
    @classmethod
    def get_saves(cls):
        cls.ensure_dir()
        saves = [f for f in os.listdir(cls.SAVE_DIR) if f.endswith('.sav')]
        return sorted(saves, key=lambda x: os.path.getmtime(os.path.join(cls.SAVE_DIR, x)), reverse=True)