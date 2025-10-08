# 🐍 Cours Complet SQLAlchemy - ORM Python

## 📚 **Introduction**

SQLAlchemy est un **ORM (Object-Relational Mapping)** Python qui fait le pont entre vos classes Python et votre base de données. Il vous permet de travailler avec des objets Python au lieu d'écrire du SQL brut.

## 📊 **11. Exemples Complets et Pratiques**

### **Exemple Complet : Blog**

```python
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import Session, select

# Base
class Base(DeclarativeBase):
    pass

# Modèles
class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "post"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship("User", back_populates="posts")

# Création de l'engine et des tables
engine = create_engine("sqlite:///blog.db")
Base.metadata.create_all(engine)

# Utilisation
with Session(engine) as session:
    # Créer des utilisateurs
    alice = User(username="alice", email="alice@blog.com")
    bob = User(username="bob", email="bob@blog.com")
    session.add_all([alice, bob])
    session.commit()
    
    # Créer des posts
    post1 = Post(title="Mon premier post", content="Contenu...", author=alice)
    post2 = Post(title="Hello World", content="Bonjour...", author=bob)
    session.add_all([post1, post2])
    session.commit()
    
    # Requêtes
    stmt = select(User).where(User.username == "alice")
    user = session.scalars(stmt).first()
    print(f"Posts d'Alice: {[p.title for p in user.posts]}")
    
    stmt = select(Post).where(Post.published == True)
    published_posts = session.scalars(stmt).all()
    print(f"Posts publiés: {[p.title for p in published_posts]}")
```

## 🏗️ **1. Architecture et Concepts Fondamentaux**

### **DeclarativeBase - Le Ciment de SQLAlchemy**

`DeclarativeBase` est une **métaclasse** qui transforme vos classes Python en entités de base de données.

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

**Important** : Toutes vos classes de modèles doivent hériter de `Base` !

### **Ce qui se passe lors de l'héritage :**

1. **Enregistrement automatique** dans le registre SQLAlchemy
2. **Création de métadonnées** de base de données
3. **Mapping automatique** des attributs vers des colonnes
4. **Activation des fonctionnalités ORM** (requêtes, relations, sessions)

## 🔑 **2. Définition des Modèles (DeclareModels)**

### **Les Deux Syntaxes de Définition**

#### **Syntaxe Moderne (Recommandée)**

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relation : tous les posts de cet utilisateur
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
```

#### **Syntaxe Legacy (Ancienne)**

```python
from sqlalchemy import Column, String, Integer

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
```

### **Types de Colonnes Essentiels**

```python
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text

class Product(Base):
    __tablename__ = "product"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    description: Mapped[str] = mapped_column(Text)  # Texte long
```

## 🔗 **3. Relations et Clés**

### **Clé Primaire (Primary Key)**

- **Identifiant unique** de chaque enregistrement
- **Auto-incrémenté** par défaut
- **Non-nullable** et **indexé**

```python
id: Mapped[int] = mapped_column(primary_key=True)
```

### **Clé Étrangère (Foreign Key)**

- **Lien** vers une autre table
- **Référence** une clé primaire
- **Garantit l'intégrité** des données

```python
author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
```

### **Relations Bidirectionnelles avec `back_populates`**

```python
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    
    # Relation : tous les posts de cet utilisateur
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "post"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    # Relation : l'utilisateur qui a créé ce post
    author: Mapped["User"] = relationship("User", back_populates="posts")
```

**Avantage** : Navigation dans les deux sens !

- `user.posts` → Liste des posts de l'utilisateur
- `post.author` → L'utilisateur qui a créé le post

## 🚀 **4. Création de l'Engine et Connexion**

### **Création de l'Engine**

```python
from sqlalchemy import create_engine

# SQLite (base de données locale)
engine = create_engine("sqlite:///database.db")

# PostgreSQL
engine = create_engine("postgresql://user:password@localhost/dbname")

# MySQL
engine = create_engine("mysql+pymysql://user:password@localhost/dbname")
```

### **Création des Tables**

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Créer toutes les tables
Base.metadata.create_all(engine)

# Ou créer une table spécifique
User.__table__.create(engine)
```

## 💾 **5. Sessions et Persistance des Objets**

### **Création d'une Session**

```python
from sqlalchemy.orm import Session

# Créer une session
session = Session(engine)

# Utiliser un contexte (recommandé)
with Session(engine) as session:
    # Votre code ici
    pass
```

### **Création et Persistance d'Objets**

```python
# Créer des objets
user1 = User(name="Alice", email="alice@example.com")
user2 = User(name="Bob", email="bob@example.com")

# Ajouter à la session
session.add(user1)
session.add(user2)

# Ou ajouter plusieurs objets
session.add_all([user1, user2])

# Persister en base de données
session.commit()

# Récupérer l'ID généré
print(f"ID d'Alice: {user1.id}")
```

## 🔍 **6. Requêtes SQL Simples**

### **Construction vs Exécution**

SQLAlchemy sépare deux étapes :

1. **Construction** de la requête (objet `stmt`)
2. **Exécution** via `session.scalars()`

```python
from sqlalchemy import select

# ÉTAPE 1 : Construction (pas d'exécution)
stmt = select(User).where(User.name == "Alice")

# ÉTAPE 2 : Exécution
for user in session.scalars(stmt):
    print(user.name)
```

### **Requêtes de Base**

```python
# Récupérer tous les utilisateurs
stmt = select(User)
users = session.scalars(stmt).all()

# Récupérer un utilisateur par ID
stmt = select(User).where(User.id == 1)
user = session.scalars(stmt).first()

# Récupérer avec conditions
stmt = select(User).where(User.name.in_(["Alice", "Bob"]))
users = session.scalars(stmt).all()

# Compter les utilisateurs
stmt = select(User)
count = session.scalars(stmt).count()

# Vérifier l'existence
stmt = select(User).where(User.email == "alice@example.com")
exists = session.scalars(stmt).first() is not None
```

### **Filtrage et Tri**

```python
from sqlalchemy import and_, or_, desc, asc

# Filtres complexes
stmt = select(User).where(
    and_(
        User.name.like("A%"),
        User.email.is_not(None)
    )
)

# Tri
stmt = select(User).order_by(desc(User.created_at))
stmt = select(User).order_by(asc(User.name))

# Limitation
stmt = select(User).limit(10).offset(20)  # Pagination
```

## 🔗 **7. Requêtes avec JOINs**

### **JOINs Implicites (via les Relations)**

```python
# Récupérer tous les posts avec leurs auteurs
stmt = select(Post).options(joinedload(Post.author))
posts = session.scalars(stmt).all()

for post in posts:
    print(f"Post: {post.title}")
    print(f"Auteur: {post.author.name}")  # Pas de requête supplémentaire !
```

### **JOINs Explicites**

```python
from sqlalchemy.orm import joinedload

# JOIN explicite
stmt = select(User, Post).join(Post, User.id == Post.author_id)
results = session.execute(stmt).all()

for user, post in results:
    print(f"Utilisateur: {user.name}, Post: {post.title}")
```

### **Requêtes avec Agrégations**

```python
from sqlalchemy import func

# Compter les posts par utilisateur
stmt = select(
    User.name,
    func.count(Post.id).label("post_count")
).join(Post).group_by(User.name)

results = session.execute(stmt).all()
for name, count in results:
    print(f"{name}: {count} posts")
```

## ✏️ **8. Mise à Jour (UPDATE)**

### **Mise à Jour d'Objets**

```python
# Récupérer un utilisateur
stmt = select(User).where(User.id == 1)
user = session.scalars(stmt).first()

# Modifier les attributs
user.name = "Alice Updated"
user.email = "alice.new@example.com"

# Persister les changements
session.commit()
```

### **Mise à Jour en Masse**

```python
from sqlalchemy import update

# Mettre à jour tous les utilisateurs avec un nom commençant par 'A'
stmt = update(User).where(User.name.like("A%")).values(email="updated@example.com")
session.execute(stmt)
session.commit()
```

## 🗑️ **9. Suppression (DELETE)**

### **Suppression d'Objets**

```python
# Récupérer et supprimer un utilisateur
stmt = select(User).where(User.id == 1)
user = session.scalars(stmt).first()

if user:
    session.delete(user)
    session.commit()
```

### **Suppression en Masse**

```python
from sqlalchemy import delete

# Supprimer tous les utilisateurs inactifs
stmt = delete(User).where(User.is_active == False)
session.execute(stmt)
session.commit()
```

### **Suppression en Cascade**

```python
class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    
    # Suppression en cascade des posts
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")
```

## 🔄 **10. Gestion des Sessions et Transactions**

### **Transactions**

```python
try:
    # Créer des objets
    user = User(name="Charlie", email="charlie@example.com")
    session.add(user)
    
    # Valider la transaction
    session.commit()
    
except Exception as e:
    # En cas d'erreur, annuler la transaction
    session.rollback()
    print(f"Erreur: {e}")
```

### **Contexte de Session**

```python
from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Utilisation
with get_session() as session:
    user = User(name="David", email="david@example.com")
    session.add(user)
    # Commit automatique à la fin du contexte
```

## 🎯 **12. Bonnes Pratiques et Conseils**

### **Performance**

```python
# Éviter le problème N+1
# ❌ Mauvaise approche
for user in session.scalars(select(User)):
    print(f"Posts de {user.name}: {[p.title for p in user.posts]}")  # Requête pour chaque utilisateur !

# ✅ Bonne approche
stmt = select(User).options(joinedload(User.posts))
for user in session.scalars(stmt):
    print(f"Posts de {user.name}: {[p.title for p in user.posts]}")  # Une seule requête !
```

### **Sécurité**

```python
# Éviter les injections SQL (SQLAlchemy le fait automatiquement)
stmt = select(User).where(User.name == user_input)  # Sécurisé !

# Validation des données
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

user_data = UserCreate(name="Eve", email="eve@example.com")
user = User(**user_data.dict())
```

### **Gestion des Erreurs**

```python
try:
    with Session(engine) as session:
        # Votre code ici
        session.commit()
except IntegrityError as e:
    print(f"Erreur d'intégrité: {e}")
except Exception as e:
    print(f"Erreur générale: {e}")
```

## 📝 **13. Résumé des Concepts Clés**

| Concept | Description | Exemple |
|---------|-------------|---------|
| **DeclarativeBase** | Métaclasse pour créer des modèles | `class Base(DeclarativeBase): pass` |
| **Mapped[]** | Type hint pour les colonnes | `id: Mapped[int] = mapped_column(primary_key=True)` |
| **Primary Key** | Identifiant unique | `id: Mapped[int] = mapped_column(primary_key=True)` |
| **Foreign Key** | Lien vers une autre table | `author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))` |
| **Relationship** | Navigation entre objets | `posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")` |
| **back_populates** | Relation bidirectionnelle | `back_populates="author"` |
| **Session** | Gestion des transactions | `with Session(engine) as session:` |
| **select()** | Construction de requêtes | `stmt = select(User).where(User.name == "Alice")` |
| **scalars()** | Exécution de requêtes | `users = session.scalars(stmt).all()` |

## 🚀 **14. Prochaines Étapes**

- **Migrations** : Alembic pour gérer les changements de schéma
- **Validation** : Pydantic pour la validation des données
- **Tests** : pytest avec des fixtures de base de données
- **Performance** : Monitoring et optimisation des requêtes
- **API** : FastAPI avec SQLAlchemy

---
