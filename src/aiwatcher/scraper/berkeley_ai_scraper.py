from typing import List
import scrapy
import requests
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article
from bs4 import BeautifulSoup

class BairScraper(scrapy.Spider):
    name = SCRAPERS_CONFIG['berkeley_ai']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['berkeley_ai'].get('start_urls', ['https://bair.berkeley.edu/blog/'])
    articles: List[Article] = []

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    }

    def __init__(self,
                max_articles: int = SCRAPERS_CONFIG['berkeley_ai']['max_articles'],
                source: str = SCRAPERS_CONFIG['berkeley_ai'].get('source', 'BAIR Blog'),
                rate_limit: float = SCRAPERS_CONFIG['berkeley_ai']['rate_limit'],
                timeout: int = SCRAPERS_CONFIG['berkeley_ai']['timeout'],
                enabled: bool = SCRAPERS_CONFIG['berkeley_ai']['enabled']
                ):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        container = response.css('div.posts')
        all_articles = container.css('div.post')

        for a in all_articles:
            try:
                title = a.css('h1.post-title a.post-link::text').get()
                if title:
                    title = title.strip()

                link = a.css('h1.post-title a.post-link::attr(href)').get()
                if link:
                    link = response.urljoin(link.strip())

                date = a.css('span.post-meta::text').getall()
                date = date[-1].strip() if date else ''

                # Récupérer le contenu complet de l'article
                content = BeautifulSoup(requests.get(link, timeout=self.timeout).text, 'html.parser').get_text(separator=' ', strip=True)
                content = ' '.join(content.split())

                # Extraire les auteurs comme keywords
                authors = [author.strip() for author in a.css('span.post-meta a::text').getall()]
                keywords = authors if authors else []

                # Extraire l'image si disponible
                img = a.css('img::attr(src)').get()
                if img:
                    img = response.urljoin(img)

                self.articles.append(Article(
                    title=title,
                    link=link,
                    date=date,
                    keywords=keywords,
                    source=self.source,
                    content=content,
                    img=img
                ).to_dict())

                if len(self.articles) >= self.max_articles:
                    return

                yield {
                    'title': title,
                    'link': link,
                    'date': date,
                    'img': img,
                    'keywords': keywords,
                    'source': self.source,
                    'content': content
                }
            except Exception as e:
                self.logger.error(f"Error parsing article: {e}")

        # Pagination - chercher le lien "Older"
        next_page = response.css('a.pagination-item:contains("Older")::attr(href)').get()
        if next_page and len(self.articles) < self.max_articles:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess()
    process.crawl(BairScraper)
    process.start()
    
    with open('data/raw/bair_ai_articles.json', 'w') as f:
        import json
        json.dump(BairScraper.articles, f, indent=4)
        print(f"Saved {len(BairScraper.articles)} articles to bair_ai_articles.json")