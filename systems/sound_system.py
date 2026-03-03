import winsound
import threading
import time
import random
import os

class SoundSystem:
    """Система звуков и музыки"""
    
    def __init__(self):
        self.music_enabled = True
        self.sound_enabled = True
        self.current_music = None
        self.music_thread = None
        self.running = True
        
        # Частоты для звуков (в Гц)
        self.sounds = {
            # Интерфейс
            "click": (500, 100),
            "error": (200, 300),
            "success": (800, 200),
            "level_up": (600, 100, 800, 100, 1000, 200),  # последовательность
            
            # Бой
            "sword": (400, 50),
            "critical": (800, 100, 1200, 100),
            "block": (200, 50),
            "heal": (600, 200, 800, 200),
            "magic": (500, 50, 600, 50, 700, 50),
            "fireball": (300, 100, 400, 100, 500, 100),
            "explosion": (200, 300, 100, 300),
            
            # Дом
            "buy": (700, 100),
            "craft": (500, 100, 600, 100),
            "harvest": (600, 100, 800, 100),
            
            # События
            "death": (200, 500),
            "quest_complete": (800, 200, 1000, 200, 1200, 400),
            "discovery": (600, 100, 800, 100, 1000, 200),
            
            # Экономика
            "money": (900, 100),
            "trade": (700, 100, 500, 100),
        }
        
        # Музыкальные темы (частоты для простой мелодии)
        self.music_themes = {
            "town": [262, 294, 330, 349, 392, 440, 494, 523],  # До мажор
            "dungeon": [220, 233, 247, 262, 277, 294, 311, 330],  # Минор
            "battle": [440, 494, 523, 587, 659, 698, 784, 880],  # Боевая
            "tavern": [262, 330, 392, 523, 659, 784],  # Веселая
            "forest": [294, 330, 349, 392, 440, 494],  # Спокойная
            "castle": [262, 294, 330, 349, 392, 440, 523],  # Величественная
            "victory": [523, 659, 784, 1046, 1318, 1568],  # Победная
            "sad": [220, 247, 262, 294, 330, 349],  # Грустная
        }
        
        # Темп музыки (задержка между нотами)
        self.tempo = {
            "town": 300,
            "dungeon": 400,
            "battle": 200,
            "tavern": 250,
            "forest": 350,
            "castle": 400,
            "victory": 150,
            "sad": 500,
        }
    
    def play_sound(self, sound_name: str):
        """Воспроизведение звука"""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            sound_data = self.sounds[sound_name]
            
            # Запускаем в отдельном потоке, чтобы не блокировать UI
            thread = threading.Thread(target=self._play_beep_sequence, args=(sound_data,))
            thread.daemon = True
            thread.start()
    
    def _play_beep_sequence(self, sequence):
        """Воспроизведение последовательности звуков"""
        for i in range(0, len(sequence), 2):
            if i + 1 < len(sequence):
                freq = sequence[i]
                duration = sequence[i + 1]
                try:
                    winsound.Beep(freq, duration)
                except:
                    pass  # Игнорируем ошибки звука
                time.sleep(duration / 1000)  # Пауза между звуками
    
    def play_music(self, theme: str, loop: bool = True):
        """Запуск музыки"""
        if not self.music_enabled:
            return
        
        if theme not in self.music_themes:
            return
        
        self.current_music = theme
        
        # Останавливаем предыдущую музыку
        self.stop_music()
        
        # Запускаем новый поток с музыкой
        self.running = True
        self.music_thread = threading.Thread(target=self._play_music_loop, args=(theme, loop))
        self.music_thread.daemon = True
        self.music_thread.start()
    
    def _play_music_loop(self, theme: str, loop: bool):
        """Воспроизведение музыки в цикле"""
        notes = self.music_themes[theme]
        delay = self.tempo[theme]
        
        while self.running:
            for note in notes:
                if not self.running:
                    break
                try:
                    winsound.Beep(note, delay)
                except:
                    pass
                time.sleep(delay / 1000)
            
            if not loop:
                break
            
            # Небольшая пауза между повторами
            time.sleep(0.5)
    
    def stop_music(self):
        """Остановка музыки"""
        self.running = False
        if self.music_thread and self.music_thread.is_alive():
            self.music_thread.join(timeout=1)
    
    def set_music_enabled(self, enabled: bool):
        """Включение/выключение музыки"""
        self.music_enabled = enabled
        if not enabled:
            self.stop_music()
    
    def set_sound_enabled(self, enabled: bool):
        """Включение/выключение звуков"""
        self.sound_enabled = enabled
    
    # Специализированные звуки для разных действий
    def play_click(self):
        self.play_sound("click")
    
    def play_error(self):
        self.play_sound("error")
    
    def play_success(self):
        self.play_sound("success")
    
    def play_level_up(self):
        self.play_sound("level_up")
    
    def play_attack(self, weapon_type="sword"):
        if weapon_type == "sword":
            self.play_sound("sword")
        elif weapon_type == "magic":
            self.play_sound("magic")
        elif weapon_type == "fireball":
            self.play_sound("fireball")
    
    def play_critical(self):
        self.play_sound("critical")
    
    def play_block(self):
        self.play_sound("block")
    
    def play_heal(self):
        self.play_sound("heal")
    
    def play_explosion(self):
        self.play_sound("explosion")
    
    def play_buy(self):
        self.play_sound("buy")
    
    def play_craft(self):
        self.play_sound("craft")
    
    def play_harvest(self):
        self.play_sound("harvest")
    
    def play_death(self):
        self.play_sound("death")
    
    def play_quest_complete(self):
        self.play_sound("quest_complete")
    
    def play_discovery(self):
        self.play_sound("discovery")
    
    def play_money(self):
        self.play_sound("money")
    
    def play_trade(self):
        self.play_sound("trade")