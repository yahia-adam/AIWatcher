# Cours complet BeautifulSoup - Web Scraping avec Python

## 📚 Introduction

BeautifulSoup est une bibliothèque Python qui permet de parser et naviguer dans du HTML/XML. Elle facilite l'extraction de données depuis des pages web.

### Installation

```bash
pip install beautifulsoup4
```

### Import de base
```python
from bs4 import BeautifulSoup
import requests
```

---

## 🎯 1. Création et parsing d'un objet BeautifulSoup

### Depuis une chaîne HTML

```python
html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters...</p>
</body></html>"""

soup = BeautifulSoup(html_doc, "html.parser")
```

### Depuis une page web

```python
response = requests.get('https://example.com')
soup = BeautifulSoup(response.content, 'html.parser')
```

---

## 🔍 2. Sélecteurs CSS - Les méthodes de recherche

### 2.1 Sélection par tag HTML

```python
# Premier élément
soup.find('div')           # Premier div
soup.div                    # Raccourci pour le premier div

# Tous les éléments
soup.find_all('div')       # Tous les divs
soup.find_all(['div', 'p']) # Divs et paragraphes
```

### 2.2 Sélection par classe CSS

```python
# Un élément avec une classe spécifique
soup.find('div', class_='content')

# Tous les éléments avec une classe
soup.find_all('div', class_='item')

# Sélecteur CSS
soup.select('.content')     # Équivalent CSS
soup.select('div.content')  # Tag + classe
```

### 2.3 Sélection par ID

```python
# Par ID
soup.find('div', id='main')
soup.find('div', {'id': 'main'})  # Alternative avec dict

# Sélecteur CSS
soup.select('#main')
```

### 2.4 Sélection par attributs

```python
# Attribut href
soup.find('a', href='https://example.com')

# Attribut src
soup.find('img', {'src': 'image.jpg'})

# Attributs multiples
soup.find('a', href=True, class_='link')
```

---

## 🌳 3. Navigation dans l'arbre DOM

### 3.1 Relations parent-enfant

```python
# Parents
element.parent              # Élément parent direct
element.parent.name         # Nom du tag parent
element.parents             # Tous les parents (générateur)

# Enfants
element.children            # Enfants directs (générateur)
element.descendants         # Tous les descendants
element.find_children()     # Enfants avec critères
```

### 3.2 Relations entre frères

```python
# Frères
element.next_sibling        # Frère suivant
element.previous_sibling    # Frère précédent
element.next_siblings       # Tous les frères suivants
element.previous_siblings   # Tous les frères précédents
```

### 3.3 Navigation directe

```python
# Navigation chaînée
soup.body.div              # Body > premier div
soup.html.head.title       # HTML > head > title
soup.body.div.p            # Body > div > premier p
```

---

## 📝 4. Extraction de contenu

### 4.1 Extraction de texte

```python
# Méthodes d'extraction de texte
element.text               # Tout le texte (avec espaces)
element.get_text()         # Même chose que .text
element.get_text(strip=True)  # Texte sans espaces superflus
element.string             # Texte direct (sans enfants)
element.stripped_strings   # Liste des chaînes nettoyées
```

### 4.2 Extraction d'attributs

```python
# Accès aux attributs
element['href']            # Valeur de l'attribut href
element.get('src')         # Plus sûr (retourne None si absent)
element.get('src', 'default.jpg')  # Valeur par défaut
element.attrs              # Tous les attributs (dict)
```

### 4.3 Extraction de HTML

```python
# HTML
element.prettify()         # HTML formaté et indenté
str(element)               # HTML brut
element.encode()           # HTML encodé
```

---

## 🔎 5. Recherche avancée

### 5.1 Recherche avec fonctions

```python
# Recherche de texte contenant un mot
soup.find_all(text=lambda text: 'python' in text.lower())

# Recherche d'éléments avec conditions
soup.find_all('div', class_=lambda x: x and 'content' in x)
```

### 5.2 Recherche avec expressions régulières

```python
import re

# Texte contenant des années
soup.find_all(text=re.compile(r'\b\d{4}\b'))

# Liens avec pattern spécifique
soup.find_all('a', href=re.compile(r'^https://'))
```

### 5.3 Recherche combinée

```python
# Limite de résultats
soup.find_all('div', class_='item', limit=5)

# Recherche dans une zone spécifique
main_div = soup.find('div', id='main')
links = main_div.find_all('a')  # Liens seulement dans main
```

---

## 🛠️ 6. Modification du DOM

### 6.1 Modification de contenu

```python
# Modifier le texte
element.string = "Nouveau texte"

# Modifier les attributs
element['class'] = 'nouvelle-classe'
element['id'] = 'nouvel-id'
```

### 6.2 Ajout d'éléments

```python
# Créer un nouveau tag
new_tag = soup.new_tag('div')
new_tag.string = "Contenu du nouveau div"

# Ajouter à un élément
element.append(new_tag)
element.insert(0, new_tag)  # Insérer au début
```

### 6.3 Suppression d'éléments

```python
# Supprimer un élément
element.decompose()        # Supprime l'élément du DOM
element.extract()          # Extrait l'élément (peut être réutilisé)
element.clear()            # Vide le contenu mais garde le tag
```

---

## 💡 7. Exemples pratiques courants

### 7.1 Extraction de liens

```python
# Extraire tous les liens avec leur texte
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    text = link.get_text().strip()
    print(f"{text}: {href}")
```

### 7.2 Extraction de tableaux
```python

# Extraire le contenu des tableaux
tables = soup.find_all('table')
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all(['td', 'th'])
        row_data = [cell.get_text().strip() for cell in cells]
        print('\t'.join(row_data))
```

### 7.3 Extraction de listes

```python
# Extraire les éléments de listes
lists = soup.find_all(['ul', 'ol'])
for list_elem in lists:
    items = list_elem.find_all('li')
    for item in items:
        print(f"- {item.get_text().strip()}")
```

### 7.4 Recherche de contenu spécifique

```python
# Trouver des articles avec un mot-clé
articles = soup.find_all('article')
for article in articles:
    title = article.find('h1') or article.find('h2')
    if title and 'python' in title.get_text().lower():
        print(f"Article trouvé: {title.get_text()}")
```

---

## ⚠️ 8. Gestion des erreurs et bonnes pratiques

### 8.1 Vérification d'existence

```python
# Vérifier si un élément existe
title = soup.find('title')
if title:
    print(title.get_text())
else:
    print("Pas de titre trouvé")

# Vérifier les attributs de manière sûre
link = soup.find('a')
href = link.get('href', '')  # Valeur par défaut si href n'existe pas
```

### 8.2 Gestion des cas particuliers

```python
# Éviter les erreurs avec des éléments None
element = soup.find('div', class_='inexistant')
if element:
    text = element.get_text()
else:
    text = "Élément non trouvé"
```

### 8.3 Performance

```python
# Utiliser des sélecteurs CSS pour de meilleures performances
soup.select('div.content')  # Plus rapide que find_all
soup.select_one('div.content')  # Plus rapide que find
```

---

## 🚀 9. Exemple complet : Scraper une page web

```python
import requests
from bs4 import BeautifulSoup
import csv

def scraper_exemple():
    # Récupérer la page
    url = "https://example.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire les données
    articles = []
    for article in soup.find_all('article'):
        title = article.find('h2')
        content = article.find('p')
        
        if title and content:
            articles.append({
                'titre': title.get_text().strip(),
                'contenu': content.get_text().strip()
            })
    
    # Sauvegarder en CSV
    with open('articles.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['titre', 'contenu'])
        writer.writeheader()
        writer.writerows(articles)
    
    return articles
```

---

## 📋 10. Résumé des méthodes principales

| Méthode | Description | Exemple |
|---------|-------------|---------|
| `find()` | Premier élément correspondant | `soup.find('div')` |
| `find_all()` | Tous les éléments correspondants | `soup.find_all('p')` |
| `select()` | Sélecteur CSS | `soup.select('.class')` |
| `select_one()` | Premier élément avec CSS | `soup.select_one('#id')` |
| `.text` | Texte de l'élément | `element.text` |
| `.get()` | Attribut de manière sûre | `element.get('href')` |
| `.parent` | Élément parent | `element.parent` |
| `.children` | Enfants directs | `element.children` |

---

## 🎓 Conclusion

BeautifulSoup est un outil puissant pour le web scraping. Les concepts clés à retenir :

1. **Sélecteurs** : Utilisez `find()`, `find_all()`, `select()` selon vos besoins
2. **Navigation** : Maîtrisez les relations parent-enfant-frères
3. **Extraction** : Choisissez la bonne méthode pour extraire texte/attributs
4. **Gestion d'erreurs** : Vérifiez toujours l'existence des éléments
5. **Performance** : Privilégiez les sélecteurs CSS pour de grandes pages
