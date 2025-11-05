"""
Конфигурация анализатора зависимостей
"""

# Настройки запросов
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

# URL API
CRATES_API_BASE = "https://crates.io/api/v1/crates"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

# Пользовательский агент для запросов
USER_AGENT = "RustDependencyAnalyzer/1.0"
