
from typing import List
import scrapy
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article
from bs4 import BeautifulSoup
import requests


class MITNewsScraper(scrapy.Spider):
    name = SCRAPERS_CONFIG['mit_news']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['mit_news'].get('start_urls', ['https://news.mit.edu/topic/artificial-intelligence2'])
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
        max_articles: int = SCRAPERS_CONFIG['mit_news']['max_articles'],
        source: str = SCRAPERS_CONFIG['mit_news'].get('source', 'MIT News'),
        rate_limit: float = SCRAPERS_CONFIG['mit_news']['rate_limit'],
        timeout: int = SCRAPERS_CONFIG['mit_news']['timeout'],
        enabled: bool = SCRAPERS_CONFIG['mit_news']['enabled']
    ):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        # Sélectionner le container principal
        container = response.css('div.page-term--views--list')
        all_articles = container.css('article.term-page--news-article--item')

        for article in all_articles:
            try:
                # Extraire le titre
                title = article.css('h3.term-page--news-article--item--title a span[itemprop="name headline"]::text').get()
                
                # Extraire l'URL
                url = article.css('h3.term-page--news-article--item--title a::attr(href)').get()
                
                # Extraire l'image
                image = article.css('div.term-page--news-article--item--cover-image img::attr(src)').get()
                if not image:
                    image = article.css('div.term-page--news-article--item--cover-image img::attr(data-src)').get()
                
                # Extraire la description
                description = article.css('p.term-page--news-article--item--dek span::text').get()
                
                # Extraire la date
                date = article.css('p.term-page--news-article--item--publication-date time::text').get()
                
                # Récupérer le contenu complet de la page
                content = ""
                if url:
                    try:
                        full_url = response.urljoin(url)
                        page_response = requests.get(full_url, timeout=self.timeout)
                        soup = BeautifulSoup(page_response.text, 'html.parser')
                        content = soup.get_text(separator=' ', strip=True)
                    except Exception as e:
                        self.logger.warning(f"Could not fetch content for {url}: {e}")
                        # Utiliser la description comme fallback
                        content = description.strip() if description else ""
                
                self.articles.append(Article(
                    title=title,
                    link=response.urljoin(url) if url else None,
                    date=date,
                    keywords=[],
                    source=self.source,
                    content=content,
                    img=response.urljoin(image) if image else None,
                    authors=[]
                ).to_dict())
                
                if len(self.articles) >= self.max_articles:
                    return

                yield {
                    'title': title.strip() if title else None,
                    'url': response.urljoin(url) if url else None,
                    'image': response.urljoin(image) if image else None,
                    'date': date.strip() if date else None,
                    'description': description.strip() if description else None,
                    'content': content
                }
            
            except Exception as e:
                self.logger.error(f"Error parsing article: {e}")
                continue

        # Gestion de la pagination
        if len(self.articles) < self.max_articles:
            next_page = response.css('a[rel="next"]::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(next_page_url, callback=self.parse)


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(
        settings={
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'DEFAULT_REQUEST_HEADERS': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
    )
    
    process.crawl(MITNewsScraper)
    process.start()

    with open('data/raw/mit_news_articles.json', 'w') as f:
        import json
        json.dump(MITNewsScraper.articles, f, indent=4)
        print(f"Saved {len(MITNewsScraper.articles)} articles to mit_news_articles.json")