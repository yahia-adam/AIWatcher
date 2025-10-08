from typing import List
import scrapy
import requests
from bs4 import BeautifulSoup
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article

class OpenAIScraper(scrapy.Spider):
    name = SCRAPERS_CONFIG['openai_blog']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['openai_blog'].get('start_urls', ['https://openai.com/index/'])
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
                max_articles: int = SCRAPERS_CONFIG['openai_blog']['max_articles'],
                source: str = SCRAPERS_CONFIG['openai_blog'].get('source', 'OpenAI Blog'),
                rate_limit: float = SCRAPERS_CONFIG['openai_blog']['rate_limit'],
                timeout: int = SCRAPERS_CONFIG['openai_blog']['timeout'],
                enabled: bool = SCRAPERS_CONFIG['openai_blog']['enabled']):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        all_articles = response.css('div.py-md.border-primary-12')

        for article_div in all_articles:
            if len(self.articles) >= self.max_articles:
                return

            try:
                category = article_div.css('div.text-meta div.me-2xs::text').get()
                if category:
                    category = category.strip()

                date_str = article_div.css('time::attr(datetime)').get()
                if date_str:
                    date_str = date_str.strip()

                title = article_div.css('div.mb-2xs.text-h5::text').get()
                if title:
                    title = title.strip()

                link = article_div.css('a::attr(href)').get()
                if link:
                    link = response.urljoin(link.strip())

                if not title or not link:
                    self.logger.warning(f"Skipping article with missing title or link")
                    continue
                
                self.articles.append(Article(title=title, link=link, date=date_str, source=self.source, content='', keywords=[category] if category else []).to_dict())

                yield {
                    'title': title,
                    'link': link,
                    'date': date_str,
                    'img': None,
                    'keywords': [category] if category else [],
                    'source': self.source,
                    'content': ''
                }

            except Exception as e:
                self.logger.error(f"Error parsing article: {e}")

        load_more_button = response.css('button:contains("Load more")')
        if load_more_button and len(self.articles) < self.max_articles:
            self.logger.info("Load more button found, but requires JavaScript interaction")

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    import json

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

    process.crawl(OpenAIScraper)
    process.start()

    output_file = 'data/raw/openai_articles.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(OpenAIScraper.articles, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(OpenAIScraper.articles)} articles to {output_file}")
