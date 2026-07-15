import subprocess
import time
import threading
import os
from flask import Flask

# 1. Создаем веб-сервер, чтобы бесплатный Render не отключал наш проект
app = Flask(__name__)

@app.route('/')
def home():
    return "Сервер управления ботами работает в штатном режиме!", 200

@app.route('/healthz')
def health():
    return "OK", 200

def run_flask():
    # Render автоматически передает порт в переменную PORT. Если её нет — берем 8080.
    port = int(os.environ.get("PORT", 8080))
    print(f"[Сервер] Запуск веб-интерфейса на порту {port}...")
    app.run(host="0.0.0.0", port=port)


# 2. Умный запуск и контроль процессов ботов
def monitor_processes():
    print("[Сервер] Сканирование папки на наличие скриптов ботов...")
    
    # Сервер сам ищет файлы, которые начинаются на 'bot_' и заканчиваются на '.py'
    bot_scripts = [f for f in os.listdir('.') if f.startswith('bot_') and f.endswith('.py')]
    
    if not bot_scripts:
        print("[ВНИМАНИЕ] Не найдено ни одного файла бота (имена должны начинаться с bot_ , например: bot_first.py)!")
        print("[Сервер] Ожидание появления файлов ботов...")
    else:
        print(f"[Сервер] Найдено ботов для запуска: {len(bot_scripts)} ({', '.join(bot_scripts)})")

    processes = {}

    # Запускаем все найденные скрипты
    for script in bot_scripts:
        print(f"[Сервер] Фоновый запуск процесса: {script}")
        processes[script] = subprocess.Popen(["python", script])

    # Бесконечный цикл проверки: если бот упал — сервер его поднимает
    while True:
        time.sleep(10) # Проверка каждые 10 секунд
        
        # На случай, если ты добавишь новые файлы на лету при обновлении на Render
        current_scripts = [f for f in os.listdir('.') if f.startswith('bot_') and f.endswith('.py')]
        for script in current_scripts:
            if script not in processes:
                print(f"[Сервер] Обнаружен новый скрипт {script}. Запуск фонового процесса...")
                processes[script] = subprocess.Popen(["python", script])

        # Проверка существующих процессов
        for script, proc in list(processes.items()):
            poll = proc.poll()
            if poll is not None: # Если процесс завершился (упал)
                print(f"[АВАРЯ] Скрипт {script} отключился (код: {poll}). Перезапуск через 5 секунд...")
                time.sleep(5)
                processes[script] = subprocess.Popen(["python", script])

if __name__ == "__main__":
    # 1. Запускаем Flask-сервер в фоновом потоке, чтобы Render видел, что мы «живы»
    web_thread = threading.Thread(target=run_flask, daemon=True)
    web_thread.start()

    # 2. Запускаем вечный контроль за процессами ботов
    monitor_processes()
