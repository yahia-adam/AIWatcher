from typing import List
import scrapy
import requests
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article
from bs4 import BeautifulSoup

class GoogleBlogScraper(scrapy.Spider):
    name = name = SCRAPERS_CONFIG['google_blog']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['google_blog'].get('start_urls', ['https://research.google/blog/label/generative-ai/'])
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
        max_articles: int = SCRAPERS_CONFIG['google_blog']['max_articles'],
        source: str = SCRAPERS_CONFIG['google_blog'].get('source', 'Google AI Blog'),
        rate_limit: float = SCRAPERS_CONFIG['google_blog']['rate_limit'],
        timeout: int = SCRAPERS_CONFIG['google_blog']['timeout'],
        enabled: bool = SCRAPERS_CONFIG['google_blog']['enabled']
    ):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        container = response.css('ul.blog-posts-grid__cards')
        all_articles = container.css('li.glue-grid__col')
        for a in all_articles:
            try:
                title =  a.css('span.headline-5::text').get().strip(),
                link = response.urljoin(a.css('a.glue-card::attr(href)').get().strip())
                date = a.css('p.glue-label::text').get().strip()
                content = BeautifulSoup(requests.get(link, timeout=self.timeout).text, 'html.parser').get_text(separator=' ', strip=True)
                content = ' '.join(content.split())
                keywords = [tag.strip() for tag in a.css('li.glue-card__link-list__item span.caption::text').getall() if tag.strip() != '']
                img = a.css('div.related-posts__image img::attr(src)').get()

                self.articles.append(Article(title=title, link=link, date=date, keywords=keywords, source=self.source, content=content, img=img).to_dict())
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

        next_button = response.css('a.pagination__next-button:not(.pagination__next-button--disabled)')
        if next_button:
            next_page_num = next_button.css('::attr(data-page)').get()
            next_page = response.url.split('?')[0] + f'?page={next_page_num}'
            yield scrapy.Request(next_page, callback=self.parse)

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(GoogleBlogScraper)
    process.start()

    with open('data/raw/google_ai_articles.json', 'w') as f:
        import json
        json.dump(GoogleBlogScraper.articles, f, indent=4)
        print(f"Saved {len(GoogleBlogScraper.articles)} articles to google_ai_articles.json")