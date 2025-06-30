import asyncio
import os
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from playwright.async_api import Page, async_playwright
from tqdm import tqdm


@dataclass
class NapItem:
    page_id: str
    page_content: str
    page_body: str


class NapExporter:

    def __init__(self, output_crawl_folder_path: str, export_type: str = "Text"):
        self._output_crawl_folder_path = output_crawl_folder_path
        self._export_type = export_type

    def _export_raw_text(self, item: NapItem) -> None:
        os.makedirs(self._output_crawl_folder_path, exist_ok=True)
        file_path = os.path.join(self._output_crawl_folder_path, f"{item.page_id}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(item.page_body)

    def _export_html(self, item: NapItem) -> None:
        os.makedirs(self._output_crawl_folder_path, exist_ok=True)
        file_path = os.path.join(self._output_crawl_folder_path, f"{item.page_id}.html")
        with open(file_path, "wb") as f:
            f.write(item.page_content)

    def export(self, item: NapItem) -> None:
        print(self._export_type)
        if self._export_type == "Text":
            self._export_raw_text(item)
        elif self._export_type == "HTML":
            self._export_html(item)
        else:
            raise ValueError(f"export_type {self._export_type} is not enable")


class NapCrawler:
    BASE_URL = "https://www.nap-camp.com"
    REGION_NAMES = [
        "北海道・東北",
        "関東",
        "北陸・甲信越",
        "東海",
        "関西",
        "中国・四国",
        "九州・沖縄",
    ]

    def __init__(self, output_crawl_folder_path: str, export_type: str = "Text", sleep_time_sec: int = 1):
        self._exporter = NapExporter(output_crawl_folder_path, export_type)
        self._sleep_time_sec = sleep_time_sec

    async def _crawl_camp_site(self, url: str) -> None:
        """キャンプサイト情報を抽出し、ファイル出力"""
        response = requests.get(url)
        await asyncio.sleep(self._sleep_time_sec)

        async def get_camp_site_info(response):
            soup = BeautifulSoup(response.text, 'html.parser')

            page_id = os.path.basename(response.url)
            page_content = response.content
            page_body = soup.get_text()
            return NapItem(page_id, page_content, page_body)

        site_info = await get_camp_site_info(response)
        self._exporter.export(site_info)

    async def _crawl_region(self, page: Page) -> None:
        """地域ごとのキャンプ場のリンクを取得し、クローリングする"""

        # もっと見るボタンを押し、キャンプ場情報を全表示する
        async def load_page(page: Page):
            # キャンプ場数を取得
            num_text = await page.locator("span.SearchResult_num__mX0lP").inner_text()

            # もっと見るボタンが表示されなくなるまでクリック
            n_click_button = int(num_text) // 10
            bar = tqdm(total=n_click_button)
            bar.set_description("Load page")
            while True:
                more_button = page.locator("button", has_text="もっと見る")
                if not await more_button.is_visible():
                    break
                await more_button.click()
                await asyncio.sleep(self._sleep_time_sec)
                bar.update(1)

        # キャンプ場URLを取得
        async def get_camp_site_urls(page: Page) -> list:
            links = page.locator("a.CampsiteResultItem_campsite-item__csEWA")
            count = await links.count()
            urls = []
            for i in range(count):
                href = await links.nth(i).get_attribute("href")
                urls.append(NapCrawler.BASE_URL + href)
            return urls

        await load_page(page)
        urls = await get_camp_site_urls(page)

        # キャンプ場URLをクローリング
        bar = tqdm(total=len(urls))
        for url in urls:
            bar.set_description("Crawl")
            await self._crawl_camp_site(url)
            bar.update(1)

    async def crawl(self, headless: bool = False) -> None:
        """なっぷサイトの全キャンプ場をクローリング"""
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()

            bar = tqdm(total=len(NapCrawler.REGION_NAMES))
            for region_name in NapCrawler.REGION_NAMES:
                bar.set_description(f"region[{region_name}]")
                await page.goto(NapCrawler.BASE_URL)
                await page.get_by_role("link", name=region_name, exact=True).click()
                await page.get_by_role("button", name="キャンプ場を探す").click()
                await self._crawl_region(page)
                bar.update(1)

            await context.close()
            await browser.close()
