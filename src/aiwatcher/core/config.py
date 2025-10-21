# src/aiwatcher/core/config.py
"""
Configuration module for AIWatcher.

This module defines the global application settings using Pydantic's BaseSettings,
and provides a dictionary for per-scraper configuration.

- The `Settings` class loads environment variables from a `.env` file if present,
    and exposes configuration for the database, Redis, API, and model cache.
- The `SCRAPERS_CONFIG` dictionary contains per-source scraping parameters
    (rate limits, URLs, categories, etc.) for each supported news or research source.

This module is intended to be imported wherever configuration is needed
throughout the AIWatcher project.
"""

from typing import Dict, Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration globale de l'application AIWatcher."""

    # Base de données
    DATABASE_URL: str = "postgresql://user:password@localhost/aiwatcher"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    # Modèles IA
    TRANSFORMERS_CACHE_DIR: str = "./config/model_cache"

    class Config:
        env_file = ".env"

# Configuration des scrapers
SCRAPERS_CONFIG: Dict[str, Dict[str, Any]] = {
    'arxiv': {
        'start_urls': ['https://arxiv.org/list/cs.AI/recent'],
        'rate_limit': 1.0,
        'max_articles': 5,
        'timeout': 10,
        'enabled': True,
        'source': 'arxiv_Blog'
    },
    'papers_with_code': {
        'start_urls': ['https://huggingface.co/papers/trending'],
        'rate_limit': 0.5,
        'max_articles': 5,
        'timeout': 15,
        'enabled': True,
        'source': 'Paper_with_code'
    },
    'google_blog': {
        'start_urls': ['https://research.google/blog/label/generative-ai/'],
        'rate_limit': 2.0,
        'max_articles': 5,
        'timeout': 10,
        'enabled': True,
        'source': 'Google_AI_Blog'
    },
    'huggingface': {
        'start_urls': ['https://huggingface.co/blog'],
        'rate_limit': 1.0,
        'max_articles': 5,
        'timeout': 10,
        'enabled': True,
        'source': 'huggingface'
    },
    'mit_news': {
        'base_url': ['https://news.mit.edu/topic/artificial-intelligence2'],
        'rate_limit': 2.0,
        'max_articles': 5,
        'timeout': 10,
        'enabled': True,
        'source': 'MIT_News'
    },
    'berkeley_ai': {
        'base_url': 'https://bair.berkeley.edu/blog',
        'rate_limit': 1.0,
        'max_articles': 15,
        'timeout': 5,
        'enabled': True,
        'source': 'Berkeley_AI'
    },

    'meta_ai': {
        'base_url': ['https://research.facebook.com/blog/#all-the-latest--blog---'],
        'rate_limit': 1.0,
        'max_articles': 15,
        'timeout': 10,
        'enabled': False,
        'source': 'Meta_AI'
    },

    'stanford_hai': {
        'base_url': ['https://hai.stanford.edu/research/publications'],
        'rate_limit': 1.5,
        'max_articles': 10,
        'timeout': 10,
        'enabled': False,
        'source': 'Standford_HAI'
    },
    'openai_blog': {
        'start_urls': ['https://openai.com/research/index/'],
        'rate_limit': 1.5,
        'max_articles': 15,
        'timeout': 10,
        'enabled': False,
        'source': 'OpenAI_News'
    }
}

# User agents pour éviter la détection de bot
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Headers communs
DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Singleton pour la configuration
settings = Settings()
