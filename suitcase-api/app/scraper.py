# src/scraper/run.py
import asyncio
from datetime import datetime
import signal
import sys
from prometheus_client import start_http_server
import structlog
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, asyncioreactor

from core.config import settings
from scraper.spider import LegalSpider

# logger = structlog.get_logger(__name__)
logger = structlog.PrintLogger()

class ScraperRunner:
    def __init__(self):
        self.settings = get_project_settings()
        self.configure_settings()
        self.runner = CrawlerRunner(self.settings)
        self.is_running = False
        
    def configure_settings(self):
        """Configure Scrapy settings."""
        self.settings.update({
            'REDIS_URL': settings.REDIS_URL,
            'RATE_LIMIT': 10,
            'RATE_LIMIT_WINDOW': 60,
            'LOG_LEVEL': 'INFO',
            'COOKIES_ENABLED': True,
            'CONCURRENT_REQUESTS': 8,
            'DOWNLOAD_DELAY': 1,
            'DOWNLOADER_MIDDLEWARES': {
                'scraper.middleware.RateLimitMiddleware': 450,
            },
        })
        
    async def run_spider(self, start_id: int, end_id: int):
        """Run the spider for a specific ID range."""
        try:
            self.is_running = True
            # logger.info(
            #     "starting_spider",
            #     start_id=start_id,
            #     end_id=end_id
            # )
            
            await self.runner.crawl(
                LegalSpider,
                start_id=start_id,
                end_id=end_id
            )
            
        except Exception as e:
            print(e)
            # logger.error(
            #     "spider_error",
            #     error=str(e),
            #     start_id=start_id,
            #     end_id=end_id
            # )
        finally:
            self.is_running = False

async def main():
    # Start Prometheus metrics server
    start_http_server(8000)

    scraper_runner = ScraperRunner()

    # Run the spider once
    print("Starting scraper")
    await scraper_runner.run_spider(1, 1000)

    # Keep the script running
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())