from typing import List
import scrapy
import requests
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article
from bs4 import BeautifulSoup

class ArxivScraper(scrapy.Spider):
    name = name = SCRAPERS_CONFIG['arxiv']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['arxiv'].get('start_urls', ['https://research.google/blog/label/generative-ai/'])
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
        max_articles: int = SCRAPERS_CONFIG['arxiv']['max_articles'],
        source: str = SCRAPERS_CONFIG['arxiv'].get('source', 'Google AI Blog'),
        rate_limit: float = SCRAPERS_CONFIG['arxiv']['rate_limit'],
        timeout: int = SCRAPERS_CONFIG['arxiv']['timeout'],
        enabled: bool = SCRAPERS_CONFIG['arxiv']['enabled']
    ):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        container = response.css('dl#articles')
        all_articles = container.css('dd')
        
        for article in all_articles:
            try:
                # Extraire le titre
                title = article.css('div.list-title.mathjax::text').getall()
                title = ' '.join([t.strip() for t in title if t.strip() and t.strip() != 'Title:'])
                
                # Extraire l'ID de l'article depuis le dt précédent
                article_id = article.xpath('preceding-sibling::dt[1]//a[contains(@href, "/abs/")]/@href').get()
                if article_id:
                    article_id = article_id.split('/')[-1]
                
                # Construire le lien HTML
                link = f"https://arxiv.org/html/{article_id}v1"
                
                # Extraire la date (depuis le h3 au début de la page)
                date = response.css('h3::text').get()
                if date:
                    # Extraire juste la date du format "Tue, 7 Oct 2025"
                    date = date.split('(')[0].strip()
                
                # Extraire les mots-clés (subjects)
                keywords = article.css('div.list-subjects span:not(.descriptor)::text').getall()
                keywords = [k.strip() for k in keywords if k.strip()]
                
                # Extraire les auteurs
                authors = article.css('div.list-authors a::text').getall()
                
                content = BeautifulSoup(requests.get(link, timeout=self.timeout).text, 'html.parser').get_text(separator=' ', strip=True)

                self.articles.append(Article(
                    title=title,
                    link=link,
                    date=date,
                    keywords=keywords,
                    source=self.source,
                    content=content,
                    authors=authors,
                ).to_dict())
                
                if len(self.articles) >= self.max_articles:
                    return
                    
                yield {
                    'title': title,
                    'link': link,
                    'date': date,
                    'keywords': keywords,
                    'source': self.source,
                    'content': content,
                    'authors': authors,
                    'article_id': article_id
                }
                
            except Exception as e:
                self.logger.error(f"Error parsing article: {e}")
                continue

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(
        settings = {
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

    process.crawl(ArxivScraper)
    process.start()

    with open('data/raw/arxiv_ai_articles.json', 'w') as f:
        import json
        json.dump(ArxivScraper.articles, f, indent=4)
        print(f"Saved {len(ArxivScraper.articles)} articles to arxiv_ai_articles.json")