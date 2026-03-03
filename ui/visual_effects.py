import tkinter as tk
import random
import math
import time

class VisualEffects:
    """Класс для визуальных эффектов"""
    
    def __init__(self, root):
        self.root = root
        self.effects = []
    
    def rain_effect(self, canvas, width, height):
        """Эффект дождя"""
        drops = []
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            length = random.randint(10, 20)
            drops.append([x, y, length])
        
        def animate():
            canvas.delete("rain")
            for drop in drops:
                drop[1] += random.randint(5, 10)
                if drop[1] > height:
                    drop[1] = 0
                    drop[0] = random.randint(0, width)
                
                canvas.create_line(drop[0], drop[1], 
                                  drop[0], drop[1] + drop[2],
                                  fill='#88ccff', width=1, tags="rain")
            canvas.after(50, animate)
        
        animate()
    
    def snow_effect(self, canvas, width, height):
        """Эффект снега"""
        flakes = []
        for _ in range(30):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 5)
            flakes.append([x, y, size])
        
        def animate():
            canvas.delete("snow")
            for flake in flakes:
                flake[1] += random.randint(1, 3)
                flake[0] += random.randint(-1, 1)
                if flake[1] > height:
                    flake[1] = 0
                    flake[0] = random.randint(0, width)
                
                canvas.create_oval(flake[0], flake[1],
                                  flake[0] + flake[2], flake[1] + flake[2],
                                  fill='white', outline='white', tags="snow")
            canvas.after(100, animate)
        
        animate()
    
    def fire_effect(self, canvas, x, y):
        """Эффект огня"""
        particles = []
        colors = ['#ff0000', '#ff4400', '#ff8800', '#ffaa00', '#ffff00']
        
        def create_particle():
            return {
                'x': x + random.randint(-10, 10),
                'y': y,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-3, -1),
                'size': random.randint(3, 8),
                'color': random.choice(colors),
                'life': random.randint(20, 40)
            }
        
        for _ in range(10):
            particles.append(create_particle())
        
        def animate():
            canvas.delete("fire")
            for p in particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= 1
                p['size'] *= 0.95
                
                if p['life'] <= 0 or p['size'] < 1:
                    particles.remove(p)
                    particles.append(create_particle())
                
                canvas.create_oval(p['x'] - p['size']/2,
                                  p['y'] - p['size']/2,
                                  p['x'] + p['size']/2,
                                  p['y'] + p['size']/2,
                                  fill=p['color'], outline='', tags="fire")
            
            if particles:
                canvas.after(50, animate)
        
        animate()
    
    def magic_effect(self, canvas, x, y, color='#4444ff'):
        """Магический эффект"""
        particles = []
        colors = [color, '#ffffff', '#8888ff']
        
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            particles.append({
                'x': x,
                'y': y,
                'angle': angle,
                'radius': 20,
                'speed': random.uniform(0.5, 1.5),
                'color': random.choice(colors),
                'size': random.randint(2, 5)
            })
        
        def animate():
            canvas.delete("magic")
            for p in particles:
                p['radius'] += p['speed']
                if p['radius'] > 50:
                    p['radius'] = 20
                
                px = p['x'] + math.cos(p['angle']) * p['radius']
                py = p['y'] + math.sin(p['angle']) * p['radius']
                
                canvas.create_oval(px - p['size']/2,
                                  py - p['size']/2,
                                  px + p['size']/2,
                                  py + p['size']/2,
                                  fill=p['color'], outline='', tags="magic")
            
            canvas.after(50, animate)
        
        animate()
    
    def level_up_effect(self, canvas, width, height):
        """Эффект повышения уровня"""
        stars = []
        for _ in range(50):
            stars.append({
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'size': random.randint(1, 3),
                'phase': random.uniform(0, 2*math.pi)
            })
        
        def animate(frame=0):
            canvas.delete("levelup")
            for star in stars:
                brightness = (math.sin(frame/10 + star['phase']) + 1) / 2
                color = f'#{int(255*brightness):02x}{int(255*brightness):02x}00'
                
                canvas.create_oval(star['x'] - star['size']/2,
                                  star['y'] - star['size']/2,
                                  star['x'] + star['size']/2,
                                  star['y'] + star['size']/2,
                                  fill=color, outline='', tags="levelup")
            
            # Текст
            canvas.create_text(width//2, height//2,
                              text="⚡ LEVEL UP! ⚡",
                              fill='#ffd700',
                              font=('Cinzel', 36, 'bold'),
                              tags="levelup")
            
            canvas.after(100, lambda: animate(frame+1))
        
        animate()
    
    def damage_effect(self, canvas, x, y, damage):
        """Эффект получения урона"""
        # Красная вспышка
        flash = canvas.create_rectangle(0, 0, 
                                        canvas.winfo_width(), 
                                        canvas.winfo_height(),
                                        fill='#ff0000', stipple='gray50')
        canvas.after(100, lambda: canvas.delete(flash))
        
        # Текст урона
        text = canvas.create_text(x, y, text=f"-{damage}",
                                   fill='#ff0000',
                                   font=('Arial', 24, 'bold'))
        
        def animate_text(frame=0):
            if frame < 20:
                canvas.move(text, 0, -2)
                canvas.after(50, lambda: animate_text(frame+1))
            else:
                canvas.delete(text)
        
        animate_text()
    
    def heal_effect(self, canvas, x, y, heal):
        """Эффект лечения"""
        # Зеленая вспышка
        flash = canvas.create_rectangle(0, 0,
                                        canvas.winfo_width(),
                                        canvas.winfo_height(),
                                        fill='#00ff00', stipple='gray50')
        canvas.after(100, lambda: canvas.delete(flash))
        
        # Текст лечения
        text = canvas.create_text(x, y, text=f"+{heal}",
                                   fill='#00ff00',
                                   font=('Arial', 24, 'bold'))
        
        def animate_text(frame=0):
            if frame < 20:
                canvas.move(text, 0, -2)
                canvas.after(50, lambda: animate_text(frame+1))
            else:
                canvas.delete(text)
        
        animate_text()
    
    def transition_effect(self, callback):
        """Эффект перехода между локациями"""
        overlay = tk.Toplevel(self.root)
        overlay.overrideredirect(True)
        overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")
        overlay.configure(bg='black')
        overlay.attributes('-alpha', 0.0)
        
        def animate(frame=0):
            alpha = frame / 20
            if alpha < 1:
                overlay.attributes('-alpha', alpha)
                overlay.after(20, lambda: animate(frame+1))
            else:
                callback()
                def fade_out(frame=0):
                    alpha = 1 - frame/20
                    if alpha > 0:
                        overlay.attributes('-alpha', alpha)
                        overlay.after(20, lambda: fade_out(frame+1))
                    else:
                        overlay.destroy()
                fade_out()
        
        animate()