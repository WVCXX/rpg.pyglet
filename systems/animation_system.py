import tkinter as tk
import random
import math
import time

class AnimationSystem:
    """Система анимаций"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.animations = []
        self.running = True
    
    def clear(self):
        """Очистка анимаций"""
        self.canvas.delete("animation")
        self.animations = []
    
    def attack_animation(self, x, y, target_x, target_y, color="#ff0000"):
        """Анимация атаки"""
        frames = 10
        dx = (target_x - x) / frames
        dy = (target_y - y) / frames
        
        def animate(frame=0):
            if frame >= frames:
                self.explosion_animation(target_x, target_y, color)
                return
            
            current_x = x + dx * frame
            current_y = y + dy * frame
            
            # Рисуем снаряд
            self.canvas.create_oval(current_x-5, current_y-5, 
                                   current_x+5, current_y+5,
                                   fill=color, outline="yellow",
                                   tags="animation")
            
            # След
            if frame > 0:
                self.canvas.create_line(x + dx * (frame-1), y + dy * (frame-1),
                                       current_x, current_y,
                                       fill=color, width=2, tags="animation")
            
            self.canvas.after(50, lambda: animate(frame+1))
        
        animate()
    
    def explosion_animation(self, x, y, color="#ff0000"):
        """Анимация взрыва"""
        particles = []
        colors = [color, "#ffff00", "#ff8800"]
        
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(10, 20),
                "color": random.choice(colors)
            })
        
        def animate():
            self.canvas.delete("explosion")
            
            for p in particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.2  # гравитация
                p['life'] -= 1
                
                if p['life'] <= 0:
                    particles.remove(p)
                    continue
                
                size = p['life'] / 10
                self.canvas.create_oval(p['x']-size, p['y']-size,
                                       p['x']+size, p['y']+size,
                                       fill=p['color'], outline="",
                                       tags="explosion")
            
            if particles:
                self.canvas.after(50, animate)
        
        animate()
    
    def magic_animation(self, x, y, color="#4444ff", spell_type="fireball"):
        """Магическая анимация"""
        if spell_type == "fireball":
            self.fireball_animation(x, y)
        elif spell_type == "heal":
            self.heal_animation(x, y)
        elif spell_type == "shield":
            self.shield_animation(x, y)
    
    def fireball_animation(self, x, y):
        """Анимация огненного шара"""
        particles = []
        colors = ["#ff0000", "#ff4400", "#ffff00"]
        
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(15, 25),
                "color": random.choice(colors)
            })
        
        def animate():
            self.canvas.delete("fireball")
            
            for p in particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= 1
                
                if p['life'] <= 0:
                    particles.remove(p)
                    continue
                
                size = p['life'] / 5
                self.canvas.create_oval(p['x']-size, p['y']-size,
                                       p['x']+size, p['y']+size,
                                       fill=p['color'], outline="yellow",
                                       tags="fireball")
            
            if particles:
                self.canvas.after(50, animate)
        
        animate()
    
    def heal_animation(self, x, y):
        """Анимация лечения"""
        particles = []
        colors = ["#00ff00", "#88ff88", "#ffffff"]
        
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            particles.append({
                "x": x,
                "y": y,
                "angle": angle,
                "radius": 20,
                "life": 30,
                "color": random.choice(colors)
            })
        
        def animate():
            self.canvas.delete("heal")
            
            for p in particles[:]:
                p['radius'] += 1
                p['life'] -= 1
                
                if p['life'] <= 0:
                    particles.remove(p)
                    continue
                
                px = p['x'] + math.cos(p['angle']) * p['radius']
                py = p['y'] + math.sin(p['angle']) * p['radius']
                
                size = p['life'] / 10
                self.canvas.create_oval(px-size, py-size, px+size, py+size,
                                       fill=p['color'], outline="",
                                       tags="heal")
            
            if particles:
                self.canvas.after(50, animate)
        
        animate()
    
    def shield_animation(self, x, y):
        """Анимация щита"""
        def animate(angle=0):
            self.canvas.delete("shield")
            
            # Рисуем вращающийся щит
            for i in range(8):
                a = angle + (i / 8) * 2 * math.pi
                px = x + math.cos(a) * 40
                py = y + math.sin(a) * 40
                
                self.canvas.create_oval(px-5, py-5, px+5, py+5,
                                       fill="#4444ff", outline="#8888ff",
                                       tags="shield")
            
            # Внешний круг
            self.canvas.create_oval(x-30, y-30, x+30, y+30,
                                   outline="#8888ff", width=2,
                                   tags="shield")
            
            self.canvas.after(100, lambda: animate(angle + 0.5))
        
        animate()
    
    def level_up_animation(self, x, y):
        """Анимация повышения уровня"""
        stars = []
        for i in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            stars.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": 40,
                "color": "#ffd700"
            })
        
        def animate():
            self.canvas.delete("levelup")
            
            # Текст
            self.canvas.create_text(x, y-50, text="⚡ LEVEL UP! ⚡",
                                   fill="#ffd700", font=("Arial", 24, "bold"),
                                   tags="levelup")
            
            for s in stars[:]:
                s['x'] += s['vx']
                s['y'] += s['vy']
                s['life'] -= 1
                
                if s['life'] <= 0:
                    stars.remove(s)
                    continue
                
                size = s['life'] / 10
                self.canvas.create_oval(s['x']-size, s['y']-size,
                                       s['x']+size, s['y']+size,
                                       fill=s['color'], outline="",
                                       tags="levelup")
            
            if stars:
                self.canvas.after(50, animate)
        
        animate()
    
    def damage_text(self, x, y, damage, is_critical=False):
        """Текст урона"""
        color = "#ff0000" if not is_critical else "#ff8800"
        font_size = 16 if not is_critical else 24
        text = f"-{damage}" if not is_critical else f"⚡ КРИТ! -{damage} ⚡"
        
        text_id = self.canvas.create_text(x, y, text=text,
                                          fill=color,
                                          font=("Arial", font_size, "bold"),
                                          tags="damage")
        
        def animate(frame=0):
            if frame < 20:
                self.canvas.move(text_id, 0, -2)
                self.canvas.after(50, lambda: animate(frame+1))
            else:
                self.canvas.delete(text_id)
        
        animate()
    
    def heal_text(self, x, y, heal):
        """Текст лечения"""
        text_id = self.canvas.create_text(x, y, text=f"+{heal}",
                                          fill="#00ff00",
                                          font=("Arial", 16, "bold"),
                                          tags="healtext")
        
        def animate(frame=0):
            if frame < 20:
                self.canvas.move(text_id, 0, -2)
                self.canvas.after(50, lambda: animate(frame+1))
            else:
                self.canvas.delete(text_id)
        
        animate()
    
    def floating_text(self, x, y, text, color="#ffffff"):
        """Плавающий текст"""
        text_id = self.canvas.create_text(x, y, text=text,
                                          fill=color,
                                          font=("Arial", 12),
                                          tags="floating")
        
        def animate(frame=0):
            if frame < 30:
                self.canvas.move(text_id, 0, -1)
                self.canvas.after(50, lambda: animate(frame+1))
            else:
                self.canvas.delete(text_id)
        
        animate()
    
    def transition(self, callback):
        """Эффект перехода"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Затемнение
        overlay = self.canvas.create_rectangle(0, 0, width, height,
                                              fill="black", stipple="gray50",
                                              tags="transition")
        
        def fade_out(frame=0):
            alpha = frame / 20
            if alpha < 1:
                self.canvas.itemconfig(overlay, stipple=f"gray{int(alpha*100)}")
                self.canvas.after(20, lambda: fade_out(frame+1))
            else:
                callback()
                
                def fade_in(frame=0):
                    alpha = 1 - frame/20
                    if alpha > 0:
                        self.canvas.itemconfig(overlay, stipple=f"gray{int(alpha*100)}")
                        self.canvas.after(20, lambda: fade_in(frame+1))
                    else:
                        self.canvas.delete(overlay)
                
                fade_in()
        
        fade_out()