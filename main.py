"""
The Life and Suffering of Prince Jerian
Главный файл запуска игры
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_structure():
    """Проверка структуры папок"""
    required_folders = [
        'ui', 'entities', 'systems', 'core', 
        'assets', 'saves', 'logs', 'data'
    ]
    
    for folder in required_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Создана папка: {folder}")
        
        if folder in ['ui', 'entities', 'systems', 'core']:
            init_file = os.path.join(folder, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write('# Auto-generated package file\n')
                print(f"📄 Создан файл: {init_file}")

def setup_logging():
    """Настройка логирования"""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    import logging
    logging.basicConfig(
        filename=os.path.join(log_dir, 'game.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )
    return logging.getLogger(__name__)

def main():
    """Главная функция"""
    print("🚀 Запуск игры...")
    
    # проверка структуры
    check_structure()
    
    # настройка логирования
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("Запуск игры The Life and Suffering of Prince Jerian")
    logger.info("=" * 50)
    
    try:
        # импорт главного окна
        from ui.main_window import RPGameWindow
        
        root = tk.Tk()
        root.title("The Life and Suffering of Prince Jerian - Кровь и Пепел")
        
        icon_path = os.path.join('assets', 'icon.ico')
        if os.path.exists(icon_path):
            try:
                root.iconbitmap(default=icon_path)
            except:
                pass

        window_width = 1400
        window_height = 900
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        root.minsize(1024, 768)
        
        def on_closing():
            if messagebox.askyesno("Выход", "Точно хочешь выйти? Несохраненный прогресс будет потерян."):
                logger.info("Игра завершена пользователем")
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("🎮 Создание игрового окна...")
        game = RPGameWindow(root)
        
        print("✅ Игра запущена!")
        
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"Ошибка импорта: {e}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        print("\n📁 Проверьте структуру папок:")
        for item in os.listdir('.'):
            if os.path.isdir(item):
                print(f"  📂 {item}/")
                try:
                    for sub in os.listdir(item):
                        if sub.endswith('.py'):
                            print(f"     📄 {sub}")
                except:
                    pass
        
        input("\nНажми Enter для выхода...")
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Критическая ошибка: {e}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        # запись ошибки в файл
        with open(os.path.join('logs', 'crash.log'), 'w', encoding='utf-8') as f:
            f.write(f"Время: {datetime.now()}\n")
            f.write(f"Ошибка: {e}\n")
            f.write(traceback.format_exc())
        
        # показ сообщения пользователю
        messagebox.showerror(
            "Критическая ошибка",
            f"Произошла ошибка:\n{e}\n\nПодробности записаны в logs/crash.log"
        )
        print(f"❌ {error_msg}")
        raise

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))










#ПРОВЕРКА НА ВШИВОСТЬ
def main():
    """Главная функция"""
    print("=" * 50)
    print("🚀 ЗАПУСК ИГРЫ")
    print("=" * 50)
    
    # Проверка Python
    print(f"🐍 Python version: {sys.version}")
    print(f"📂 Working directory: {os.getcwd()}")
    
    try:
        print("\n[1/6] Создание корневого окна...")
        root = tk.Tk()
        root.title("The Life and Suffering of Prince Jerian")
        root.geometry("1400x900")
        root.configure(bg='#0a0a0a')
        print("   ✅ Корневое окно создано")
        
        print("\n[2/6] Первичное обновление...")
        root.update()
        print("   ✅ Окно обновлено")
        
        print("\n[3/6] Импорт RPGameWindow...")
        try:
            from ui.main_window import RPGameWindow
            print("   ✅ Импорт успешен")
        except ImportError as e:
            print(f"   ❌ Ошибка импорта: {e}")
            print("\nПроверьте наличие файлов:")
            for folder in ['ui', 'entities', 'systems', 'core']:
                if os.path.exists(folder):
                    print(f"   📂 {folder}/")
                    for f in os.listdir(folder):
                        if f.endswith('.py'):
                            print(f"      📄 {f}")
            raise
        print("\n[4/6] Создание экземпляра игры...")
        try:
            game = RPGameWindow(root)
            print("   ✅ Игра создана")
        except Exception as e:
            print(f"   ❌ Ошибка создания игры: {e}")
            traceback.print_exc()
            raise
        
        print("\n[5/6] Финальное обновление...")
        root.update()
        print("   ✅ Готово")
        
        print("\n[6/6] Запуск главного цикла...")
        print("=" * 50)
        print("✅ ИГРА УСПЕШНО ЗАПУЩЕНА!")
        print("=" * 50)
        
        root.mainloop()
        
    except Exception as e:
        print("\n" + "=" * 50)
        print("❌ КРИТИЧЕСКАЯ ОШИБКА")
        print("=" * 50)
        print(f"Ошибка: {e}")
        print("\nПолный traceback:")
        traceback.print_exc()
        
        with open('crash_log.txt', 'w', encoding='utf-8') as f:
            f.write(f"Ошибка: {e}\n")
            f.write(traceback.format_exc())
        
        print(f"\n📝 Лог сохранен в crash_log.txt")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)

if __name__ == "__main__":
    main()
