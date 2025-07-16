from dataclasses import dataclass


@dataclass
class NapItem:
    page_id: str
    page_content: str
    page_body: str
