#!/usr/bin/env python3
"""
Минимальное CLI-приложение для анализа пакетов с конфигурацией в XML
"""

import sys
import os
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
from enum import Enum


class RepositoryMode(Enum):
    """Режимы работы с репозиторием"""
    LOCAL = "local"
    REMOTE = "remote"


class ConfigError(Exception):
    """Исключение для ошибок конфигурации"""
    pass


class PackageAnalyzerConfig:
    """Класс для работы с конфигурацией приложения"""
    
    def __init__(self, config_file: str = "config.xml"):
        self.config_file = config_file
        self.default_config = {
            'package_name': 'example-package',
            'repository_url': './test-repo',
            'repository_mode': RepositoryMode.LOCAL.value,
            'package_version': '1.0.0',
            'filter_substring': ''
        }
        self.config = self.default_config.copy()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Загрузка конфигурации из XML-файла
        """
        try:
            if not os.path.exists(self.config_file):
                raise ConfigError(f"Конфигурационный файл '{self.config_file}' не найден")
            
            tree = ET.parse(self.config_file)
            root = tree.getroot()
            
            config_data = {}
            
            # Имя пакета
            package_name_elem = root.find('package_name')
            if package_name_elem is not None:
                config_data['package_name'] = package_name_elem.text.strip()
            
            # URL репозитория или путь к файлу
            repository_url_elem = root.find('repository_url')
            if repository_url_elem is not None:
                config_data['repository_url'] = repository_url_elem.text.strip()
            
            # Режим работы с репозиторием
            repository_mode_elem = root.find('repository_mode')
            if repository_mode_elem is not None:
                mode_value = repository_mode_elem.text.strip().lower()
                if mode_value not in [mode.value for mode in RepositoryMode]:
                    raise ConfigError(f"Недопустимый режим репозитория: {mode_value}. "
                                    f"Допустимые значения: {[mode.value for mode in RepositoryMode]}")
                config_data['repository_mode'] = mode_value
            
            # Версия пакета
            package_version_elem = root.find('package_version')
            if package_version_elem is not None:
                config_data['package_version'] = package_version_elem.text.strip()
            
            # Подстрока для фильтрации
            filter_substring_elem = root.find('filter_substring')
            if filter_substring_elem is not None:
                config_data['filter_substring'] = filter_substring_elem.text.strip() if filter_substring_elem.text else ''
            
            # Обновляем конфигурацию
            self.config.update(config_data)
            
            # Валидация параметров
            self._validate_config()
            
            return self.config
            
        except ET.ParseError as e:
            raise ConfigError(f"Ошибка парсинга XML файла: {e}")
        except Exception as e:
            raise ConfigError(f"Ошибка загрузки конфигурации: {e}")
    
    def _validate_config(self) -> None:
        """Валидация параметров конфигурации"""
        # Проверка имени пакета
        if not self.config['package_name'] or not isinstance(self.config['package_name'], str):
            raise ConfigError("Имя пакета должно быть непустой строкой")
        
        # Проверка URL/пути репозитория
        if not self.config['repository_url'] or not isinstance(self.config['repository_url'], str):
            raise ConfigError("URL/путь репозитория должен быть непустой строкой")
        
        # Проверка версии пакета
        if not self.config['package_version'] or not isinstance(self.config['package_version'], str):
            raise ConfigError("Версия пакета должна быть непустой строкой")
        
        # Проверка подстроки фильтрации
        if not isinstance(self.config['filter_substring'], str):
            raise ConfigError("Подстрока фильтрации должна быть строкой")
    
    def create_sample_config(self) -> None:
        """
        Создание примерного конфигурационного файла
        """
        sample_config = '''<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <!-- Имя анализируемого пакета -->
    <package_name>example-package</package_name>
    
    <!-- URL-адрес репозитория или путь к файлу тестового репозитория -->
    <repository_url>./test-repo</repository_url>
    
    <!-- Режим работы с тестовым репозиторием (local/remote) -->
    <repository_mode>local</repository_mode>
    
    <!-- Версия пакета -->
    <package_version>1.0.0</package_version>
    
    <!-- Подстрока для фильтрации пакетов -->
    <filter_substring>test</filter_substring>
</configuration>
'''
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write(sample_config)
            print(f"Создан пример конфигурационного файла: {self.config_file}")
        except Exception as e:
            raise ConfigError(f"Ошибка создания примерного конфигурационного файла: {e}")


def print_config(config: Dict[str, Any]) -> None:
    """
    Вывод конфигурации в формате ключ-значение
    """
    print("=" * 50)
    print("КОНФИГУРАЦИЯ ПРИЛОЖЕНИЯ")
    print("=" * 50)
    
    for key, value in config.items():
        print(f"{key:20} : {value}")
    
    print("=" * 50)


def main():
    """
    Основная функция приложения
    """
    config_file = "config.xml"
    config_manager = PackageAnalyzerConfig(config_file)
    
    try:
        # Проверяем существование конфигурационного файла
        if not os.path.exists(config_file):
            print(f"Конфигурационный файл '{config_file}' не найден.")
            create_sample = input("Создать пример конфигурационного файла? (y/n): ").strip().lower()
            if create_sample == 'y':
                config_manager.create_sample_config()
                print("Отредактируйте config.xml и запустите приложение снова.")
                return
            else:
                print("Завершение работы.")
                return
        
        # Загружаем конфигурацию
        config = config_manager.load_config()
        
        print_config(config)

        print("\nПриложение запущено!")
        
    except ConfigError as e:
        print(f"ОШИБКА КОНФИГУРАЦИИ: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nРабота приложения прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"ОШИБКА: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
