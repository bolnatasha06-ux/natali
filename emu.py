#!/usr/bin/env python3
"""
Минимальное CLI-приложение для анализа пакетов с конфигурацией из XML-файла
"""

import xml.etree.ElementTree as ET
import sys
import os
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
            'package_name': '',
            'repository_url': '',
            'repository_mode': RepositoryMode.LOCAL.value,
            'package_version': '1.0.0',
            'filter_substring': ''
        }
        self.config = self.default_config.copy()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Загрузка конфигурации из XML-файла
        
        Returns:
            Dict[str, Any]: Словарь с настройками
            
        Raises:
            ConfigError: При ошибках загрузки или валидации конфигурации
        """
        try:
            # Проверка существования файла
            if not os.path.exists(self.config_file):
                raise ConfigError(f"Конфигурационный файл '{self.config_file}' не найден")
            
            # Парсинг XML
            tree = ET.parse(self.config_file)
            root = tree.getroot()
            
            # Извлечение параметров
            extracted_config = {}
            
            # Имя пакета
            package_name_elem = root.find('package_name')
            if package_name_elem is not None and package_name_elem.text:
                extracted_config['package_name'] = package_name_elem.text.strip()
            else:
                raise ConfigError("Параметр 'package_name' отсутствует или пуст")
            
            # URL репозитория или путь
            repo_elem = root.find('repository_url')
            if repo_elem is not None and repo_elem.text:
                extracted_config['repository_url'] = repo_elem.text.strip()
            else:
                raise ConfigError("Параметр 'repository_url' отсутствует или пуст")
            
            # Режим репозитория
            mode_elem = root.find('repository_mode')
            if mode_elem is not None and mode_elem.text:
                mode_value = mode_elem.text.strip().lower()
                if mode_value not in [mode.value for mode in RepositoryMode]:
                    raise ConfigError(f"Недопустимый режим репозитория: {mode_value}")
                extracted_config['repository_mode'] = mode_value
            else:
                extracted_config['repository_mode'] = self.default_config['repository_mode']
            
            # Версия пакета
            version_elem = root.find('package_version')
            if version_elem is not None and version_elem.text:
                extracted_config['package_version'] = version_elem.text.strip()
            else:
                extracted_config['package_version'] = self.default_config['package_version']
            
            # Подстрока для фильтрации
            filter_elem = root.find('filter_substring')
            if filter_elem is not None and filter_elem.text is not None:
                extracted_config['filter_substring'] = filter_elem.text.strip()
            else:
                extracted_config['filter_substring'] = self.default_config['filter_substring']
            
            self.config.update(extracted_config)
            return self.config
            
        except ET.ParseError as e:
            raise ConfigError(f"Ошибка парсинга XML: {e}")
        except Exception as e:
            raise ConfigError(f"Ошибка загрузки конфигурации: {e}")
    
    def validate_config(self) -> None:
        """Валидация загруженной конфигурации"""
        if not self.config['package_name']:
            raise ConfigError("Имя пакета не может быть пустым")
        
        if not self.config['repository_url']:
            raise ConfigError("URL или путь к репозиторию не может быть пустым")
        
        # Проверка существования локального пути для локального режима
        if (self.config['repository_mode'] == RepositoryMode.LOCAL.value and 
            not os.path.exists(self.config['repository_url'])):
            raise ConfigError(f"Локальный путь не существует: {self.config['repository_url']}")
        
        # Базовая валидация версии
        version = self.config['package_version']
        if not all(c.isdigit() or c == '.' for c in version.replace(' ', '')):
            raise ConfigError(f"Некорректный формат версии: {version}")
    
    def display_config(self) -> None:
        """Вывод конфигурации в формате ключ-значение"""
        print("=" * 50)
        print("Конфигурация приложения:")
        print("=" * 50)
        for key, value in self.config.items():
            print(f"{key:20}: {value}")
        print("=" * 50)


def create_sample_config() -> None:
    """Создание примерного конфигурационного файла"""
    sample_config = """<?xml version="1.0" encoding="UTF-8"?>
<config>
    <package_name>example-package</package_name>
    <repository_url>https://github.com/example/repo.git</repository_url>
    <repository_mode>remote</repository_mode>
    <package_version>1.2.3</package_version>
    <filter_substring>test</filter_substring>
</config>
"""
    
    with open("config.xml", "w", encoding="utf-8") as f:
        f.write(sample_config)
    print("Создан пример конфигурационного файла 'config.xml'")


def main():
    """Основная функция приложения"""
    
    # Проверяем аргументы командной строки
    config_file = "config.xml"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    # Если файл конфигурации не существует, создаем пример
    if not os.path.exists(config_file):
        print(f"Конфигурационный файл '{config_file}' не найден.")
        create_sample_config()
        print("Запустите приложение снова для использования примерной конфигурации.")
        return 1
    
    try:
        # Загрузка и валидация конфигурации
        config_manager = PackageAnalyzerConfig(config_file)
        config = config_manager.load_config()
        config_manager.validate_config()
        
        # Вывод конфигурации (требование этапа 1)
        config_manager.display_config()
        
        print("\nКонфигурация успешно загружена! Приложение готово к работе.")
        return 0
        
    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    exit(main())
