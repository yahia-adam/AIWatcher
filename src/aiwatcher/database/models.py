"""SQLAlchemy ORM models for the aiwatcher database.

Defines the main data structures for articles, summaries, entities, daily digests, and trends.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, Integer, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

class Article(Base):
    """Represents a news or research article ingested by the system."""
    __tablename__ = "articles"

    # Identifiants
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Métadonnées de base
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Auteurs et dates
    authors: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    published_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True)
    scraped_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    # Contenu
    raw_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cleaned_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    # Métadonnées de contenu
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    word_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reading_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Status et qualité
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Timestamps
    created_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False)
    updated_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)

    # Relations
    summaries: Mapped[List["Summary"]] = relationship("Summary", back_populates="article", cascade="all, delete-orphan")
    entities: Mapped[List["Entity"]] = relationship("Entity", back_populates="article", cascade="all, delete-orphan")

class Summary(Base):
    """Summarization results for an article, including different summary lengths and key points."""
    __tablename__ = "summaries"

    # Identifiants
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey('articles.id'), nullable=False, index=True)

    # Résumés de différentes tailles
    short_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)      # 1-2 phrases
    medium_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)     # 1 paragraphe
    long_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)       # 2-3 paragraphes

    # Points clés extraits
    key_points: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    conclusions: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    # Métadonnées du modèle
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Timestamps
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relations
    article: Mapped["Article"] = relationship("Article", back_populates="summaries")

class Entity(Base):
    """Named entity extracted from an article, with context and normalization info."""
    __tablename__ = "entities"

    # Identifiants
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey('articles.id'), nullable=False, index=True)

    # Entité détectée
    entity_text: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # Contexte dans l'article
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    position_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    position_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sentence_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Scores
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    importance_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Normalisation
    canonical_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    aliases: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    wikipedia_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Métadonnées techniques
    model_used: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    extraction_method: Mapped[str] = mapped_column(String(50), default="NER", nullable=False)

    # Timestamps
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, index=True)
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relations
    article: Mapped["Article"] = relationship("Article", back_populates="entities")

class DailyDigest(Base):
    """Aggregated daily statistics and highlights for ingested articles."""
    __tablename__ = "daily_digests"

    # Identifiants
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime, unique=True, nullable=False, index=True)

    # Statistiques
    total_articles: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    articles_by_source: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    articles_by_category: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Top entités
    top_researchers: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    top_organizations: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    top_models: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    trending_topics: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    # Résumé global
    daily_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    highlights: Mapped[Optional[List[int]]] = mapped_column(JSON, nullable=True)  # IDs articles

    # Timestamps
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

class Trend(Base):
    """Tracks trending keywords and their statistics over time."""
    __tablename__ = "trends"

    # Identifiants
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    keyword: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Métriques temporelles
    week_mentions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    month_mentions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    growth_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Contexte
    related_articles: Mapped[Optional[List[int]]] = mapped_column(JSON, nullable=True)
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Timestamps
    updated_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, index=True)
