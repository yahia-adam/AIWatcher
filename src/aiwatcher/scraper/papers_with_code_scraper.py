from typing import List
import scrapy
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article
from bs4 import BeautifulSoup
import requests


class PapersWithCodeScraper(scrapy.Spider):
    name = SCRAPERS_CONFIG['papers_with_code']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['papers_with_code'].get('start_urls', ['https://huggingface.co/papers'])
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
        max_articles: int = SCRAPERS_CONFIG['papers_with_code']['max_articles'],
        source: str = SCRAPERS_CONFIG['papers_with_code'].get('source', 'Papers with Code'),
        rate_limit: float = SCRAPERS_CONFIG['papers_with_code']['rate_limit'],
        timeout: int = SCRAPERS_CONFIG['papers_with_code']['timeout'],
        enabled: bool = SCRAPERS_CONFIG['papers_with_code']['enabled']
    ):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        # Sélectionner le container principal
        container = response.css('div.relative.grid.gap-5')
        all_articles = container.css('article.relative.overflow-hidden.rounded-xl.border')

        for article in all_articles:
            try:
                # Extraire le titre
                title = article.css('h3.text-xl.font-semibold a::text').get()
                if not title:
                    title = article.css('h3.text-lg.font-semibold a::text').get()
                
                # Extraire l'URL de l'article
                url = article.css('h3 a::attr(href)').get()

                # Extraire l'image
                image = article.css('img::attr(src)').get()
                
                # Extraire l'auteur/organisation
                author = article.css('a[href*="/"] span.block.min-w-0.truncate.font-medium::text').get()
                
                # Extraire la date de publication
                date = None
                date_spans = article.css('span:contains("Published on")::text, span:contains("Sep"), span:contains("Oct")').getall()
                for span in date_spans:
                    if any(month in span for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                        date = span.strip()
                        break
                full_url = response.urljoin(url) if url else None
                content = BeautifulSoup(requests.get(full_url, timeout=self.timeout).text, 'html.parser').get_text(separator=' ', strip=True)

                self.articles.append(Article(
                    title=title.strip() if title else None,
                    link=full_url,
                    date=date,
                    keywords=[],
                    source=self.source,
                    content=content,
                    img=image,
                    authors=[author] if author else []
                ).to_dict())
                
                if len(self.articles) >= self.max_articles:
                    return

                yield {
                    'title': title.strip() if title else None,
                    'url': full_url,
                    'image': image,
                    'author': author.strip() if author else None,
                    'date': date,
                    'content': content
                }
            
            except Exception as e:
                self.logger.error(f"Error parsing article: {e}")
                continue

        # Gestion de la pagination si nécessaire
        next_button = response.css('a:contains("Next")::attr(href)').get()
        if next_button and len(self.articles) < self.max_articles:
            next_page = response.urljoin(next_button)
            yield scrapy.Request(next_page, callback=self.parse)


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
    
    process.crawl(PapersWithCodeScraper)
    process.start()

    with open('data/raw/papers_with_code_articles.json', 'w') as f:
        import json
        json.dump(PapersWithCodeScraper.articles, f, indent=4)
        print(f"Saved {len(PapersWithCodeScraper.articles)} articles to papers_with_code_articles.json")