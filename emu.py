#!/usr/bin/env python3
"""
Эмулятор командной оболочки ОС - Этап 2: Конфигурация
"""

import shlex
import sys
import os
import argparse

class ShellEmulator:
    def __init__(self, vfs_path=None, script_path=None):
        self.vfs_path = vfs_path or "/default/vfs"
        self.script_path = script_path
        self.vfs_name = os.path.basename(self.vfs_path)
        self.current_dir = "/"
        self.verbose = True

    def debug_print(self, message):
        """Отладочный вывод"""
        if self.verbose:
            print(f"[DEBUG] {message}")
    
    def get_prompt(self):
        """Формирование приглашения к вводу"""
        return f"{self.vfs_name}:{self.current_dir}$ "
    
    def execute_script(self, script_path):
        """Выполнение скрипта с имитацией диалога"""
        self.debug_print(f"Запуск скрипта: {script_path}")
        
        try:
            with open(script_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue
                    
                self.debug_print(f"Обработка строки {line_num}: {line}")
                
                # Имитируем ввод пользователя
                print(f"{self.get_prompt()}{line}")
                
                # Выполняем команду
                b = shlex.split(line)
                
                if len(b) == 0:
                    continue
                    
                if b[0] == "ls":
                    print(f"ls: {b[1:] if len(b) > 1 else 'текущая директория'}")
                elif b[0] == "cd":
                    if len(b) > 1:
                        self.current_dir = b[1]
                        print(f"cd: переход в {b[1]}")
                    else:
                        self.current_dir = "/"
                        print("cd: переход в корневую директорию")
                elif b[0] == "exit":
                    print("exit: завершение работы")
                    return True
                else:
                    print(f'{b[0]}: command not found')
                    
        except FileNotFoundError:
            print(f"Ошибка: скрипт '{script_path}' не найден")
            return False
        except Exception as e:
            print(f"Ошибка выполнения скрипта: {e}")
            return False
            
        return False
    
    def run_interactive(self):
        """Запуск интерактивного режима"""
        print("Эмулятор командной оболочки ОС")
        print("Введите 'exit' для выхода")
        print("-" * 40)
        
        while True:
            try:
                a = input(self.get_prompt())
                b = shlex.split(a)
                
                if a == "exit":
                    break
                if len(b) == 0:
                    continue
                    
                if b[0] == "ls":
                    print(b)
                elif b[0] == "cd":
                    print(b)
                else:
                    print(f'{b[0]}: command not found')
                    
            except EOFError:
                print("\nВыход из эмулятора")
                break
            except KeyboardInterrupt:
                print("\nПрервано пользователем")
                break
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")

def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Эмулятор командной оболочки ОС',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  %(prog)s                            # Интерактивный режим
  %(prog)s --vfs-path /my/vfs         # С указанием пути VFS
  %(prog)s --script test.txt          # Со скриптом
  %(prog)s --vfs-path /custom --script test.txt --verbose
        '''
    )
    parser.add_argument('--vfs-path', 
                       type=str, 
                       help='Путь к физическому расположению VFS')
    parser.add_argument('--script', 
                       type=str, 
                       help='Путь к стартовому скрипту')
    parser.add_argument('--verbose', 
                       action='store_true',
                       default=True,
                       help='Включить отладочный вывод (по умолчанию: True)')
    
    return parser.parse_args()

def print_startup_info(args):
    """Вывод информации о параметрах запуска"""
    print("=== Параметры запуска эмулятора ===")
    print(f"VFS путь: {args.vfs_path or 'не указан (используется по умолчанию)'}")
    print(f"Скрипт: {args.script or 'не указан'}")
    print(f"Отладочный вывод: {'включен' if args.verbose else 'выключен'}")
    print("=" * 40)

def main():
    """Главная функция"""
    args = parse_arguments()
    
    # Отладочный вывод параметров
    print_startup_info(args)
    
    # Создание эмулятора
    emulator = ShellEmulator(args.vfs_path, args.script)
    emulator.verbose = args.verbose
    
    # Если указан скрипт - выполняем его
    if args.script:
        should_exit = emulator.execute_script(args.script)
        if should_exit:
            return
    
    # Запуск интерактивного режима
    emulator.run_interactive()

if __name__ == "__main__":
    main()

