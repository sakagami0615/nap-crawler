import asyncio
import os

import requests
from bs4 import BeautifulSoup
from playwright.async_api import Page, async_playwright
from tqdm import tqdm

from napcrawler.core.exporter import NapExporter
from napcrawler.core.item import NapItem


class NapCrawler:
    BASE_URL = "https://www.nap-camp.com"
    REGION_MAP = {
        "北海道・東北": "hokkaido_tohoku",
        "関東": "kanto",
        "北陸・甲信越": "hokushinetsu",
        "東海": "tokai",
        "関西": "kansai",
        "中国・四国": "chugoku_shikoku",
        "九州・沖縄": "kyushu_okinawa",
    }

    def __init__(
        self,
        output_crawl_folder_path: str,
        output_type: str = "Text",
        wait_time_sec: int = 1,
        request_timeout: int = 10,
    ):
        self._exporter = NapExporter(output_crawl_folder_path, output_type)
        self._wait_time_sec = wait_time_sec
        self._request_timeout = request_timeout
        self._metadata_store = {}

    async def _crawl_camp_site(self, url: str) -> None:
        """キャンプサイト情報を抽出し、ファイル出力"""
        response = requests.get(url, timeout=self._request_timeout)
        await asyncio.sleep(self._wait_time_sec)

        async def inner_get_camp_site_info(response):
            soup = BeautifulSoup(response.text, "html.parser")

            page_id = os.path.basename(response.url)
            page_content = response.content
            page_body = soup.get_text()
            return NapItem(page_id, page_content, page_body)

        async def inner_get_metadata(response):
            soup = BeautifulSoup(response.text, "html.parser")

            name_soup = soup.find("h1", class_="CampsiteDetail_site-name__ON7Zs")
            address_soup = soup.find("div", class_="CampsiteDetail_site-address__5098_")
            location_soups = soup.find_all("a", class_="breadcrumbs-item")

            name = name_soup.get_text()
            address = address_soup.get_text().replace("地図を表示", "")
            # NOTE: 先頭要素は[キャンプ場検索予約]の文字のためスキップ
            locations = [location_soup.get_text() for location_soup in location_soups[1:]]

            return {
                "キャンプ場名": name,
                "住所": address,
                "場所(地方名)": locations[0],
                "場所(県名)": locations[1],
                "場所(市名)": locations[2],
            }

        # キャンプ場情報を取得し、エクスポート
        site_info = await inner_get_camp_site_info(response)
        self._exporter.export_site_data(site_info)

        # メタデータを取得し、ストア
        self._metadata_store[site_info.page_id] = await inner_get_metadata(response)

    async def _crawl_region(self, page: Page) -> None:
        """地域ごとのキャンプ場のリンクを取得し、クローリングする"""

        # もっと見るボタンを押し、キャンプ場情報を全表示する
        async def inner_load_page(page: Page):
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
                await asyncio.sleep(self._wait_time_sec)
                bar.update(1)

        # キャンプ場URLを取得
        async def inner_get_camp_site_urls(page: Page) -> list:
            links = page.locator("a.CampsiteResultItem_campsite-item__csEWA")
            count = await links.count()
            urls = []
            for i in range(count):
                href = await links.nth(i).get_attribute("href")
                urls.append(NapCrawler.BASE_URL + href)
            return urls

        await inner_load_page(page)
        urls = await inner_get_camp_site_urls(page)

        # キャンプ場URLをクローリング
        bar = tqdm(total=len(urls))
        for url in urls:
            bar.set_description("Crawl")
            await self._crawl_camp_site(url)
            bar.update(1)

    async def crawl(self, headless: bool = False, specify_regions: list[str] | None = None) -> None:
        """なっぷサイトの全キャンプ場をクローリング"""

        if specify_regions is None:
            specify_regions = list(NapCrawler.REGION_MAP.values())

        self._metadata_store = {}
        access_urls = [f"{NapCrawler.BASE_URL}/{region_name}/list?sortId=21" for region_name in specify_regions]

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()

            bar = tqdm(total=len(access_urls))
            for region_name, region_url in zip(specify_regions, access_urls, strict=False):
                bar.set_description(f"region[{region_name}]")
                await page.goto(region_url)
                await self._crawl_region(page)
                bar.update(1)

            self._exporter.export_metadata(self._metadata_store)

            await context.close()
            await browser.close()
