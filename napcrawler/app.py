import asyncio
import os
from dotenv import load_dotenv
from napcrawler.crawler import NapCrawler


load_dotenv()

OUTPUT_CRAWL_FOLDER_PATH = os.environ.get("NAP_CRAWLER_OUTPUT_CRAWL_FOLDER_PATH", ".crawl_data")
EXPORT_TYPE = os.environ.get("NAP_CRAWLER_EXPORT_TYPE", "Text")
SLEEP_TIME_SEC = eval(os.environ.get("NAP_CRAWLER_SLEEP_TIME_SEC", "1"))
HEADLESS = eval(os.environ.get("NAP_CRAWLER_HEADLESS", "False"))


def main():
    nap_crawler = NapCrawler(OUTPUT_CRAWL_FOLDER_PATH, EXPORT_TYPE, SLEEP_TIME_SEC)
    asyncio.run(nap_crawler.crawl(HEADLESS))


if __name__ == "__main__":
    main()
