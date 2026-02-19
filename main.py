import sys
import os
import tkinter as tk
from tkinter import messagebox

# путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

required_folders = ['ui', 'entities', 'systems', 'core']
for folder in required_folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

        with open(os.path.join(folder, '__init__.py'), 'w') as f:
            f.write('# Auto-generated')

try:
    from ui.main_window import RPGameWindow
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\n📁 Текущая структура папок:")
    for item in os.listdir('.'):
        if os.path.isdir(item):
            print(f"  📂 {item}/")
            for sub in os.listdir(item):
                print(f"     📄 {sub}")
    print("\n🔧 Решение:")
    print("1. Создай файл ui/main_window.py")
    print("2. Создай файл entities/npc.py")
    print("3. Во всех папках должен быть __init__.py")
    input("\nНажми Enter для выхода...")
    sys.exit(1)

def main():
    root = tk.Tk()
    root.title("The Life and Suffering of Prince Jerian")
    root.geometry("1200x800")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 1200) // 2
    y = (screen_height - 800) // 2
    root.geometry(f"1200x800+{x}+{y}")
    
    for folder in ['saves', 'logs', 'data']:
        os.makedirs(folder, exist_ok=True)
    
    try:
        game = RPGameWindow(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        with open("logs/error.log", "w", encoding="utf-8") as f:
            import traceback
            f.write(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()