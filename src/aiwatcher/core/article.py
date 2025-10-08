class Article:
    def __init__(self,
            title,
            link,
            date,
            source,
            content,
            img=None,
            summary=None,
            keywords= [],
            authors= [],
            ):
        self.title = title
        self.link = link
        self.date = date
        self.source = source
        self.content = content
        self.img = img
        self.summary = summary
        self.keywords = keywords
        self.authors = authors

    def to_dict(self):
        return {
            'title': self.title,
            'link': self.link,
            'date': self.date,
            'img': self.img,
            'source': self.source,
            'summary': self.summary,
            'keywords': self.keywords,
            'authors': self.authors,
            'content': self.content
        }
    
    def gen_summary(self):
        """Génère un résumé de l'article en utilisant un modèle de langage."""
        pass

    def extract_keywords(self):
        """Extrait les mots-clés de l'article en utilisant un modèle de langage."""
        pass

    def categorize(self):
        """Catégorise l'article en utilisant un modèle de langage."""
        pass
