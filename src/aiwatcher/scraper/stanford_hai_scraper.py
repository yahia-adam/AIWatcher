from typing import List
import scrapy
from aiwatcher.core.config import SCRAPERS_CONFIG
from aiwatcher.core.article import Article
from bs4 import BeautifulSoup
import requests


class StanfordHAIScraper(scrapy.Spider):
    name = SCRAPERS_CONFIG['stanford_hai']['source'] + "_scraper"
    start_urls = SCRAPERS_CONFIG['stanford_hai'].get('start_urls', ['https://hai.stanford.edu/research'])
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
        max_articles: int = SCRAPERS_CONFIG['stanford_hai']['max_articles'],
        source: str = SCRAPERS_CONFIG['stanford_hai'].get('source', 'Stanford HAI'),
        rate_limit: float = SCRAPERS_CONFIG['stanford_hai']['rate_limit'],
        timeout: int = SCRAPERS_CONFIG['stanford_hai']['timeout'],
        enabled: bool = SCRAPERS_CONFIG['stanford_hai']['enabled']
    ):
        super().__init__()
        self.max_articles = max_articles
        self.source = source
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.enabled = enabled

    def parse(self, response):
        # Sélectionner le container principal
        container = response.css('div.FilteredSearchIndex_resultsContainer__tqn1D')
        all_articles = container.css('div.FilteredSearchIndex_resultItem__0biE8')

        for article in all_articles:
            try:
                # Extraire le titre
                title = article.css('h5.ContentItem_title__tD342 a.ContentItem_titleLink__iBCUW::text').get().strip()
                
                # Extraire l'URL
                url = article.css('h5.ContentItem_title__tD342 a.ContentItem_titleLink__iBCUW::attr(href)').get()
                
                # Extraire l'image
                image = article.css('div.ContentItem_image__5_fLt img::attr(src)').get()
                if not image:
                    srcset = article.css('div.ContentItem_image__5_fLt img::attr(srcset)').get()
                    if srcset:
                        image = srcset.split()[0]
                
                # Extraire l'auteur
                author = article.css('div.ContentMeta_peopleOrAttribution__emzzk span a::text').get()
                
                # Extraire la date
                date_elements = article.css('div.ContentMeta_data__blERF span.Typography_mono-small__Avr8B::text').getall()
                date = None
                for elem in date_elements:
                    if any(month in elem for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                        date = elem.strip()
                        break

                # Extraire les topics/keywords
                topics = article.css('div.ContentItem_topics__tMeu3 a div.Tag_root__haHHI span::text').getall()
                keywords = [topic.strip() for topic in topics if topic.strip()]

                # Récupérer le contenu complet de la page
                content = BeautifulSoup(requests.get(response.urljoin(url), timeout=self.timeout).text, 'html.parser').get_text(separator=' ', strip=True)

                self.articles.append(Article(
                    title="title",
                    link="response.urljoin(url) if url else None",
                    date="date",
                    keywords="keywords",
                    source="self.source",
                    content="content",
                    img="image",
                    authors="[author] if author else []"
                ).to_dict())

                if len(self.articles) >= self.max_articles:
                    return

                yield {
                    'title': "title",
                    'url': "response.urljoin(url) if url else None",
                    'image': "image",
                    'author': "author.strip() if author else None",
                    'date': "date.strip() if date else None",
                    'keywords': "keywords",
                    'content': "content"
                }

            except Exception as e:
                self.logger.error(f"Error parsing article: {e}")
                continue

        if len(self.articles) < self.max_articles:
            next_page = response.css('a.Pagination_pageAdjacentLink__Irz7P::attr(href)').get()
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
    
    process.crawl(StanfordHAIScraper)
    process.start()

    with open('data/raw/stanford_hai_articles.json', 'w') as f:
        import json
        json.dump(StanfordHAIScraper.articles, f, indent=4)
        print(f"Saved {len(StanfordHAIScraper.articles)} articles to stanford_hai_articles.json")