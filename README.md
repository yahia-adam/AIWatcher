# AIWatcher - Architecture du projet

## **AIWatcher**

**Pitch :** Un scraper intelligent qui collecte les derniers articles sur l’intelligence artificielle (recherches, actualités, innovations), les résume automatiquement, détecte les entités clés (NER) comme auteurs, laboratoires et modèles, puis expose le tout via une API prête pour la production.
*(Stack : Python, scrapy, Hugging Face, FastAPI, Docker)*

| Jour | Objectifs / Tâches                                                       | 📚 Concepts à réviser                                  | 🔗 Ressources rapides                                                                                                                                       | 🎯 Livrable                   |
| ---- | ------------------------------------------------------------------------ | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| 1    | Scraper articles IA (blogs, revues, sites tech) + stockage en PostgreSQL | HTTP, HTML parsing, JSON vs SQL                        | [BeautifulSoup Doc](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [SQLAlchemy Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) | Script scraping + stockage DB |
| 2    | Nettoyage texte & tokenization                                           | Tokenization (BPE/WordPiece), lemmatisation, stopwords | [HF Tokenizers](https://huggingface.co/docs/tokenizers/index)                                                                                               | Script preprocessing          |
| 3    | Résumé + NER ciblé IA                                                    | Seq2Seq, Transformers, Attention                       | [BART Summarization](https://huggingface.co/transformers/task_summary.html), [NER HF](https://huggingface.co/course/chapter7/3?fw=pt)                       | Script résumé + NER           |
| 4    | API FastAPI pour résumé + NER                                            | REST, Swagger/OpenAPI                                  | [FastAPI Docs](https://fastapi.tiangolo.com/)                                                                                                               | API fonctionnelle             |
| 5    | Dockerisation + CI/CD GitHub Actions                                     | Dockerfile, workflow basique                           | [Docker Guide](https://docs.docker.com/get-started/), [GitHub Actions](https://docs.github.com/en/actions)                                                  | Image Docker + CI/CD          |
| 6    | Tests & optimisation                                                     | Batch processing, lazy loading                         | [Profiling Python](https://docs.python.org/3/library/profile.html)                                                                                          | Benchmarks API                |
| 7    | Documentation                                                            | Structuration README                                   | [Readme Best Practices](https://www.makeareadme.com/)                                                                                                       | README + démo vidéo           |

## 📁 Structure des dossiers et fichiers

```md
aiwatcher/
├── 📁 src/
│   ├── 📁 scraper/
│   │   ├── __init__.py                        # Initialisation du module scraper
│   │   ├── models.py                          # Classes dédiées pour stocker les données scrapées
│   │   ├── base_scraper.py                    # Classe abstraite pour tous les scrapers
│   │   ├── arxiv_scraper.py                   # Scraper ArXiv (papers IA)
│   │   ├── google_ai_scraper.py               # Scraper Google AI Blog
│   │   ├── openai_scraper.py                  # Scraper OpenAI Blog
│   │   ├── huggingface_scraper.py             # Scraper Hugging Face Blog
│   │   ├── papers_with_code_scraper.py        # Scraper Papers With Code
│   │   ├── towards_datascience_scraper.py     # Scraper Towards Data Science
│   │   ├── venturebeat_scraper.py             # Scraper VentureBeat AI
│   │   ├── meta_ai_scraper.py                 # Scraper Meta AI Blog
│   │   ├── reddit_ml_scraper.py               # Scraper Reddit r/MachineLearning
│   │   ├── mit_news_scraper.py                # Scraper MIT News AI
│   │   ├── stanford_hai_scraper.py            # Scraper Stanford HAI
│   │   ├── berkeley_ai_scraper.py             # Scraper Berkeley AI Research
│   │   ├── scraper_factory.py                 # Factory pattern pour créer scrapers
│   │   ├── scraper_config.py                  # Configuration des scrapers
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── html_parser.py                 # Utilitaires parsing HTML
│   │       ├── rate_limiter.py                # Gestion rate limiting
│   │       ├── user_agents.py                 # User agents rotation
│   │       └── validators.py                  # Validation des données
│   │
│   ├── 📁 database/
│   │   ├── __init__.py
│   │   ├── models.py                # Modèles SQLAlchemy
│   │   ├── connection.py            # Configuration DB
│   │   └── migrations/              # Scripts migration Alembic
│   │       ├── env.py
│   │       └── versions/
│   │
│   ├── 📁 preprocessing/
│   │   ├── __init__.py
│   │   ├── text_cleaner.py          # Nettoyage et normalisation
│   │   ├── tokenizer.py             # Tokenization HuggingFace
│   │   └── utils.py                 # Utilitaires preprocessing
│   │
│   ├── 📁 ai_models/
│   │   ├── __init__.py
│   │   ├── summarizer.py            # Modèle résumé (BART/T5)
│   │   ├── ner_extractor.py         # Extraction entités nommées
│   │   ├── model_manager.py         # Gestion cache et optimisation
│   │   └── config/
│   │       └── model_configs.json   # Configuration modèles
│   │
│   ├── 📁 api/
│   │   ├── __init__.py
│   │   ├── main.py                  # Point d'entrée FastAPI
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── articles.py          # Endpoints articles
│   │   │   ├── summarize.py         # Endpoints résumé
│   │   │   └── entities.py          # Endpoints NER
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── article.py           # Pydantic models articles
│   │   │   ├── summary.py           # Pydantic models résumés
│   │   │   └── entity.py            # Pydantic models entités
│   │   ├── dependencies.py          # Dépendances FastAPI
│   │   └── middleware.py            # Middleware custom
│   │
│   ├── 📁 services/
│   │   ├── __init__.py
│   │   ├── article_service.py       # Logique métier articles
│   │   ├── ai_service.py            # Orchestration modèles IA
│   │   └── cache_service.py         # Gestion cache Redis
│   │
│   └── 📁 core/
│       ├── __init__.py
│       ├── config.py                # Configuration globale
│       ├── exceptions.py            # Exceptions personnalisées
│       └── logging_config.py        # Configuration logs
│
├── 📁 tests/
│   ├── __init__.py
│   ├── conftest.py                  # Configuration pytest
│   ├── 📁 unit/
│   │   ├── test_scraper.py
│   │   ├── test_preprocessing.py
│   │   ├── test_ai_models.py
│   │   └── test_services.py
│   ├── 📁 integration/
│   │   ├── test_database.py
│   │   ├── test_api_endpoints.py
│   │   └── test_workflow.py
│   └── 📁 fixtures/
│       ├── sample_articles.json
│       └── mock_responses.py
│
├── 📁 scripts/
│   ├── run_scraper.py               # Script autonome scraping
│   ├── batch_process.py             # Traitement par lots
│   ├── setup_db.py                  # Initialisation base de données
│   └── benchmark.py                 # Scripts de performance
│
├── 📁 docker/
│   ├── Dockerfile                   # Image principale
│   ├── Dockerfile.dev               # Image développement
│   ├── docker-compose.yml           # Orchestration services
│   └── docker-compose.dev.yml       # Configuration dev
│
├── 📁 deployment/
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   └── terraform/                   # Infrastructure as Code
│       ├── main.tf
│       └── variables.tf
│
├── 📁 .github/
│   └── workflows/
│       ├── ci.yml                   # Tests automatisés
│       ├── cd.yml                   # Déploiement continu
│       └── codeql.yml               # Analyse sécurité
│
├── 📁 docs/
│   ├── api/
│   │   └── openapi.json             # Spécification OpenAPI
│   ├── architecture.md              # Documentation architecture
│   ├── setup.md                     # Guide installation
│   └── deployment.md                # Guide déploiement
│
├── 📁 monitoring/
│   ├── prometheus/
│   │   └── metrics.py               # Métriques custom
│   └── grafana/
│       └── dashboards.json          # Dashboards monitoring
│
├── 📁 data/
│   ├── raw/                         # Données brutes scraping
│   ├── processed/                   # Données preprocessées
│   └── models/                      # Modèles entraînés/fine-tunés
│
├── 📁 config/
│   ├── settings.yaml                # Configuration par environnement
│   ├── logging.yaml                 # Configuration logs
│   └── model_cache/                 # Cache modèles HuggingFace
│
├── .env.example                     # Variables d'environnement exemple
├── .gitignore                       # Fichiers à ignorer Git
├── .dockerignore                    # Fichiers à ignorer Docker
├── requirements.txt                 # Dépendances production
├── requirements-dev.txt             # Dépendances développement
├── pyproject.toml                   # Configuration projet Python
├── alembic.ini                      # Configuration migrations DB
├── README.md                        # Documentation principale
├── CHANGELOG.md                     # Journal des modifications
└── LICENSE                          # Licence du projet
```

## 🏗️ Architecture logicielle

### **Couche de données**

- **PostgreSQL** : Stockage articles, résumés, entités
- **Redis** : Cache modèles IA et résultats
- **Système de fichiers** : Modèles HuggingFace en local

### **Couche service**

- **Scraper Layer** : Collecte multi-sources avec factory pattern
- **AI Processing Layer** : Pipeline résumé + NER avec optimisations
- **API Layer** : FastAPI avec documentation automatique

### **Couche infrastructure**

- **Docker** : Conteneurisation application + dépendances
- **CI/CD** : Tests automatisés + déploiement
- **Monitoring** : Métriques Prometheus + dashboards Grafana

## 📊 Flux de données

```
Sources Web → Scrapers → DB → Preprocessing → Modèles IA → API → Clients
     ↓            ↓         ↓        ↓            ↓        ↓
   [Tech]     [Factory]  [PostgreSQL] [HF]    [Cache]   [REST]
   [Cyber]    [Pattern]                [Tokens]  [Redis]  [JSON]
```

## 🎯 Points clés architecture

**Modularité** : Chaque composant est indépendant et testable
**Scalabilité** : Cache intelligent + batch processing
**Maintainabilité** : Separation of concerns + documentation
**Observabilité** : Logs structurés + métriques + monitoring
**Sécurité** : Variables d'env + validation + rate limiting