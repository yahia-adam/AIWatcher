from typing import List
import scrapy
import requests
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article
from bs4 import BeautifulSoup

class MetaAIScraper(scrapy.Spider):
    name = SCRAPERS_CONFIG['meta_ai']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['meta_ai'].get('base_url', ['https://research.facebook.com/blog/#all-the-latest--blog---'])
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
                max_articles: int = SCRAPERS_CONFIG['meta_ai']['max_articles'],
                source: str = SCRAPERS_CONFIG['meta_ai'].get('source', 'Meta AI'),
                rate_limit: float = SCRAPERS_CONFIG['meta_ai']['rate_limit'],
                timeout: int = SCRAPERS_CONFIG['meta_ai']['timeout'],
                enabled: bool = SCRAPERS_CONFIG['meta_ai']['enabled']
                ):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        container = response.css('div._9z57')
        all_articles = container.css('article._9z5n')

        for a in all_articles:
            try:
                title = a.css('h3._9z5r a._9z5s div._8l_f p::text').get()
                if title:
                    title = title.strip()

                link = a.css('h3._9z5r a._9z5s::attr(href)').get()
                if link:
                    link = link.strip()
                    if not link.startswith('http'):
                        link = response.urljoin(link)

                date = a.css('div._9z5t p::text').get()
                if date:
                    date = date.strip()
                content = BeautifulSoup(requests.get(link, timeout=self.timeout).text, 'html.parser').get_text(separator=' ', strip=True)
                content = ' '.join(content.split())

                img = a.css('div._9z5o img._90f0::attr(src)').get()
                if not img or 'rsrc.php' in img:
                    style = a.css('div._9z5o img._90f0::attr(style)').get()
                    if style and 'background-image: url(' in style:
                        img = style.split('background-image: url("')[1].split('"')[0] if 'background-image: url("' in style else None

                if img and not img.startswith('http'):
                    img = response.urljoin(img)

                keywords = []

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

        next_button = response.css('a._9ran._aism')
        if next_button and len(self.articles) < self.max_articles:
            next_page_num = next_button.css('::attr(data-next-page)').get()
            next_offset = next_button.css('::attr(data-next-offset)').get()

            if next_page_num and next_offset:
                base_url = response.url.split('#')[0]
                next_page = f"{base_url}#all-the-latest--blog---page-{next_page_num}"
                yield scrapy.Request(next_page, callback=self.parse)

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(MetaAIScraper)
    process.start()

    with open('data/raw/meta_ai_articles.json', 'w') as f:
        import json
        json.dump(MetaAIScraper.articles, f, indent=4)
        print(f"Saved {len(MetaAIScraper.articles)} articles to meta_ai_articles.json") 