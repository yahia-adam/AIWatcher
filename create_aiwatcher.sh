#!/bin/bash

# Création du projet AIWatcher
echo "🚀 Création de la structure AIWatcher..."

# Structure principale src/
mkdir -p src/{scraper,database,preprocessing,ai_models,api,services,core}

# Scraper
touch src/scraper/{__init__.py,base_scraper.py,tech_scraper.py,cyber_scraper.py,scraper_factory.py}

# Database
mkdir -p src/database/migrations/versions
touch src/database/{__init__.py,models.py,connection.py}
touch src/database/migrations/{env.py}

# Preprocessing
touch src/preprocessing/{__init__.py,text_cleaner.py,tokenizer.py,utils.py}

# AI Models
mkdir -p src/ai_models/config
touch src/ai_models/{__init__.py,summarizer.py,ner_extractor.py,model_manager.py}
touch src/ai_models/config/model_configs.json

# API
mkdir -p src/api/{routers,schemas}
touch src/api/{__init__.py,main.py,dependencies.py,middleware.py}
touch src/api/routers/{__init__.py,articles.py,summarize.py,entities.py}
touch src/api/schemas/{__init__.py,article.py,summary.py,entity.py}

# Services
touch src/services/{__init__.py,article_service.py,ai_service.py,cache_service.py}

# Core
touch src/core/{__init__.py,config.py,exceptions.py,logging_config.py}

# Tests
mkdir -p tests/{unit,integration,fixtures}
touch tests/{__init__.py,conftest.py}
touch tests/unit/{test_scraper.py,test_preprocessing.py,test_ai_models.py,test_services.py}
touch tests/integration/{test_database.py,test_api_endpoints.py,test_workflow.py}
touch tests/fixtures/{sample_articles.json,mock_responses.py}

# Scripts
mkdir -p scripts
touch scripts/{run_scraper.py,batch_process.py,setup_db.py,benchmark.py}

# Docker
mkdir -p docker
touch docker/{Dockerfile,Dockerfile.dev,docker-compose.yml,docker-compose.dev.yml}

# Deployment
mkdir -p deployment/{kubernetes,terraform}
touch deployment/kubernetes/{deployment.yaml,service.yaml,ingress.yaml}
touch deployment/terraform/{main.tf,variables.tf}

# GitHub Actions
mkdir -p .github/workflows
touch .github/workflows/{ci.yml,cd.yml,codeql.yml}

# Documentation
mkdir -p docs/api
touch docs/{architecture.md,setup.md,deployment.md}
touch docs/api/openapi.json

# Monitoring
mkdir -p monitoring/{prometheus,grafana}
touch monitoring/prometheus/metrics.py
touch monitoring/grafana/dashboards.json

# Dossiers data
mkdir -p data/{raw,processed,models}

# Configuration
mkdir -p config/model_cache
touch config/{settings.yaml,logging.yaml}

# Fichiers racine
touch .env.example
touch .gitignore
touch .dockerignore
touch requirements.txt
touch requirements-dev.txt
touch pyproject.toml
touch alembic.ini
touch README.md
touch CHANGELOG.md
touch LICENSE

echo "✅ Structure AIWatcher créée avec succès !"
echo "📁 $(find . -type d | wc -l) dossiers créés"
echo "📄 $(find . -type f | wc -l) fichiers créés"

# Affichage de la structure (optionnel)
echo ""
echo "🌳 Structure du projet :"
tree -a -I '.git|__pycache__|*.pyc|.pytest_cache' || find . -type d | sort
