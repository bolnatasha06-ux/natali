# test_serde.py - тестовый скрипт для проверки с serde
import subprocess
import sys

def test_serde():
    """Тестируем с пакетом serde"""
    print("Тестирование с пакетом serde...")
    
    # Запускаем основной скрипт с тестовыми данными
    process = subprocess.Popen([
        sys.executable, "dependency_scanner.py"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Вводим тестовые данные
    input_data = "serde\n1.0.0\nhttps://github.com/serde-rs/serde\n"
    stdout, stderr = process.communicate(input=input_data)
    
    print("Результат:")
    print(stdout)
    if stderr:
        print("Ошибки:")
        print(stderr)

if __name__ == "__main__":
    test_serde()
