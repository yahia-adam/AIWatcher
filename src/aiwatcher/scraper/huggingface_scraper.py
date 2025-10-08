from typing import List
import scrapy
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article
from bs4 import BeautifulSoup
import requests

class HuggingFaceScraper(scrapy.Spider):
    name = name = SCRAPERS_CONFIG['huggingface']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['huggingface'].get('start_urls', ['https://huggingface.co/blog'])
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
        max_articles: int = SCRAPERS_CONFIG['huggingface']['max_articles'],
        source: str = SCRAPERS_CONFIG['huggingface'].get('source', 'Google AI Blog'),
        rate_limit: float = SCRAPERS_CONFIG['huggingface']['rate_limit'],
        timeout: int = SCRAPERS_CONFIG['huggingface']['timeout'],
        enabled: bool = SCRAPERS_CONFIG['huggingface']['enabled']
    ):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        container = response.css('div.grid.grid-cols-1.gap-12.pt-8.lg\:grid-cols-2')
        all_articles = container.css('a.flex.lg\:col-span-1')

        for article in all_articles:
            title = article.css('h2.font-serif.font-semibold.group-hover\:underline.text-xl::text').get()
            url = article.css('::attr(href)').get()
            image = f"https://huggingface.co{article.css('img::attr(src)').get()}"
            author = article.css('a.hover\:underline::text').get()
            date = article.css('span.truncate::text').get()
            content = BeautifulSoup(requests.get(response.urljoin(url), timeout=self.timeout).text, 'html.parser').get_text(separator=' ', strip=True)
            self.articles.append(Article(title=title, link=response.urljoin(url) if url else None, date=date, keywords=[], source=self.source, content=content, img=image, authors=[author] if author else []).to_dict())
            if len(self.articles) >= self.max_articles:
                return

            yield {
                'title': title.strip() if title else None,
                'url': response.urljoin(url) if url else None,
                'image': image,
                'author': author.strip() if author else None,
                'date': date.strip() if date else None,
                'content': content
            }

        next_button = response.css('a.flex.items-center.rounded-lg:contains("Next")')
        if next_button:
            next_page_url = next_button.css('::attr(href)').get()
            if next_page_url:
                next_page = response.urljoin(next_page_url)
                yield scrapy.Request(next_page, callback=self.parse)

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
    
    process.crawl(HuggingFaceScraper)
    process.start()

    with open('data/raw/huggingface_ai_articles.json', 'w') as f:
        import json
        json.dump(HuggingFaceScraper.articles, f, indent=4)
        print(f"Saved {len(HuggingFaceScraper.articles)} articles to huggingface_ai_articles.json")