import json
import os

from napcrawler.core.item import NapItem


class NapExporter:
    def __init__(self, output_crawl_folder_path: str, output_item_type: str = "Text"):
        self._output_metadata_file_path = os.path.join(output_crawl_folder_path, "metadata.json")
        self._output_item_folder_path = os.path.join(output_crawl_folder_path, "data")
        self._output_item_type = output_item_type

    def _export_raw_text(self, item: NapItem) -> None:
        file_path = os.path.join(self._output_item_folder_path, f"{item.page_id}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(item.page_body)

    def _export_html(self, item: NapItem) -> None:
        file_path = os.path.join(self._output_item_folder_path, f"{item.page_id}.html")
        with open(file_path, "wb") as f:
            f.write(item.page_content)

    def export_site_data(self, item: NapItem) -> None:
        if self._output_item_type == "Text":
            os.makedirs(self._output_item_folder_path, exist_ok=True)
            self._export_raw_text(item)
        elif self._output_item_type == "HTML":
            os.makedirs(self._output_item_folder_path, exist_ok=True)
            self._export_html(item)
        else:
            raise ValueError(f"output_type {self._output_type} is not enable")

    def export_metadata(self, metadata: dict) -> None:
        os.makedirs(self._output_item_folder_path, exist_ok=True)
        with open(self._output_metadata_file_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
