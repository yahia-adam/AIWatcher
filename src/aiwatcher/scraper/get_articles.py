from scrapy.crawler import CrawlerProcess
from aiwatcher.scraper.arxiv_scraper import ArxivScraper
from aiwatcher.scraper.papers_with_code_scraper import PapersWithCodeScraper
from aiwatcher.scraper.openai_scraper import OpenAIScraper
from aiwatcher.scraper.google_ai_scraper import GoogleBlogScraper
from aiwatcher.scraper.huggingface_scraper import HuggingFaceScraper
from aiwatcher.scraper.mit_news_scraper import MITNewsScraper
from aiwatcher.scraper.stanford_hai_scraper import StanfordHAIScraper
from aiwatcher.scraper.berkeley_ai_scraper import BairScraper
from aiwatcher.scraper.meta_ai_scraper import MetaAIScraper
import json

def get_all_articles():
    scrapers = [
        ArxivScraper,
        PapersWithCodeScraper,
        OpenAIScraper,
        GoogleBlogScraper,
        HuggingFaceScraper,
        MITNewsScraper,
        StanfordHAIScraper,
        BairScraper,
        MetaAIScraper
    ]

    process = CrawlerProcess(
        settings={
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'DEFAULT_REQUEST_HEADERS': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 1,
        }
    )

    for scraper_class in scrapers:
        try:
            process.crawl(scraper_class)
        except Exception as e:
            print(f"Error adding scraper: {scraper_class.__name__} - {e}")

    process.start()

    all_articles = []
    for scraper_class in scrapers:
        try:
            all_articles.extend(scraper_class.articles)
        except Exception as e:
            print(f"Error collecting articles from: {scraper_class.__name__} - {e}")
    
    return all_articles

if __name__ == "__main__":
    articles = get_all_articles()
    
    with open('data/raw/all_ai_articles.json', 'w') as f:
        json.dump(articles, f, indent=4)
        print(f"Saved {len(articles)} articles to all_ai_articles.json")