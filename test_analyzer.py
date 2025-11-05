#!/usr/bin/env python3
"""
Тестовый скрипт для проверки анализатора зависимостей
"""

from pupupu import CargoDependencyAnalyzer

def test_analyzer():
    """Тестирование на известных пакетах"""
    test_cases = [
        ("serde", "1.0.0"),
        ("tokio", "1.0.0"),
        ("reqwest", "0.11.0")
    ]
    
    analyzer = CargoDependencyAnalyzer()
    
    for package_name, version in test_cases:
        print(f"\nТестирование {package_name} {version}...")
        try:
            dependencies = analyzer.get_direct_dependencies(package_name, version)
            analyzer.display_dependencies(dependencies, package_name, version)
        except Exception as e:
            print(f"Ошибка при тестировании {package_name}: {e}")

if __name__ == "__main__":
    test_analyzer()
