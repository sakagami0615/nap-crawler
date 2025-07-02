import argparse
import asyncio
from napcrawler.crawler import NapCrawler
from napcrawler.create_logger import change_logger_level
from napcrawler.setting import LOGGER_NAME, LOGGER


def get_argument():
    def positive_int(value):
        value = int(value)
        if value <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
        return value

    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder_path")
    parser.add_argument("-t", "--output_type", help="HTML or Text", default="HTML",type=str, choices=["HTML", "Text"])
    parser.add_argument("-w", "--wait_time_sec", default=1, type=positive_int)
    parser.add_argument("--headless", default=False, type=bool)
    parser.add_argument("--log_level", default="WARNING", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    args = parser.parse_args()

    change_logger_level(LOGGER_NAME, args.log_level)

    return args


def main():
    args = get_argument()

    LOGGER.info(f"args: {args}")

    nap_crawler = NapCrawler(args.output_folder_path, args.output_type, args.wait_time_sec)
    asyncio.run(nap_crawler.crawl(args.headless))


if __name__ == "__main__":
    main()
