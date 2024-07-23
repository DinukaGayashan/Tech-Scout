from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: int
    availability: bool
    link: str
    shop: str
    category: str


class Category(BaseModel):
    name: str
    path: str


class Selector(BaseModel):
    name: str
    component: str
    tag_class: Optional[str] = None


class Job(BaseModel):
    url: str
    shop: str
    category_path: str
    categories: List[Category]
    block_selector: Selector
    product_selectors: List[Selector]
    pagination_parameter_config: Optional[bool] = True
    pagination_parameter: Optional[str] = "page"
    pagination_path_config: Optional[bool] = False
    pagination_path: Optional[str] = "page"
    rate_limit: Optional[int] = 20  # Max concurrent requests
    dynamic: Optional[bool] = False
    max_pages: Optional[int] = 10


class Page(BaseModel):
    content: str | bytes
    category: Category


class PageCollection(BaseModel):
    pages: List[Page]


class URL(BaseModel):
    url: str
    category: Category
