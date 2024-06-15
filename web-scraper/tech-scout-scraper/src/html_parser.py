from typing import List

from selectolax.parser import HTMLParser, Node

from .schemas import Job, Page, PageCollection, Product, Selector


class ParseError(Exception):
    pass


class Parser:

    def __init__(self, page_collection: PageCollection, job: Job) -> None:
        self.page_collection = page_collection
        self.products = []
        self.total_blocks = 0
        self.job = job

    @property
    def total_products(self):
        return len(self.products)

    def parse_products(self) -> List[Product]:
        for page in self.page_collection.pages:
            self.parse_page(page=page)
        parsed_percentage = (self.total_products * 100) / self.total_blocks
        print(f"Total Blocks: {self.total_blocks}", end=" | ")
        print(f"Total Products: {self.total_products}", end=" | ")
        print(f"Percentage: {parsed_percentage}%")
        return self.products

    def parse_page(self, page: Page) -> None:

        html = HTMLParser(page.content)
        blocks = html.css(
            f"{self.job.block_selector.component}.{self.job.block_selector.tag_class}"
        )
        total_blocks = len(blocks)
        self.total_blocks += total_blocks
        if total_blocks == 0:
            return []
        for block in blocks:
            product = self.parse_product(block, page.category.name)
            if (
                product.name == "NameNotFound"
                or product.price == -1
                or product.link == "NoURLFound"
            ):
                continue
            self.products.append(product)

    def parse_product(self, block: Node, category: str) -> Product:
        for selector in self.job.product_selectors:
            selector_name = selector.name
            if selector_name == "availability":
                availability = Parser.parse_availability(block, selector)
            elif selector_name == "link":
                link = Parser.parse_link(block, selector)
            elif selector_name == "name":
                name = Parser.parse_name(block, selector)
            elif selector_name == "price":
                price = Parser.parse_price(block, selector)
        return Product(
            name=name,
            price=price,
            availability=availability,
            link=link,
            shop=self.job.shop,
            category=category,
        )

    @staticmethod
    def parse_name(block: Node, selector: Selector) -> str:
        css_selector = f"{selector.component}.{selector.tag_class}"
        matches = {match.text(strip=True).lower() for match in block.css(css_selector)}
        if not matches:
            return "NameNotFound"

        if len(matches) != 1:
            raise ParseError("Contains more than 1 matches")

        return matches.pop()

    @staticmethod
    def parse_price(block: Node, selector: Selector) -> int:
        css_selector = f"{selector.component}.{selector.tag_class}"
        matches = {
            int(
                float(
                    match.text(strip=True).lower().replace(",", "").replace("lkr", "")
                )
            )
            for match in block.css(css_selector)
        }
        if not matches:
            return -1

        if len(matches) > 1:
            matches = sorted(matches)
            return matches[0]

        return matches.pop()

    @staticmethod
    def parse_availability(block: Node, selector: Selector) -> bool:
        css_selector = f"{selector.component}.{selector.tag_class}"
        matches = block.css(css_selector)

        if not matches:
            return False

        if len(matches) != 1:
            raise ParseError("Contains more than 1 matches")

        availability_message = (
            matches[0].text(strip=True).lower().replace(" ", "").replace("-", "")
        )
        if "instock" in availability_message:
            return True
        if "outofstock" in availability_message:
            return False
        if "preorder" in availability_message:
            return False
        raise ParseError(f"Cannot parse availability message - {availability_message}")

    @staticmethod
    def parse_link(block: Node, selector: Selector) -> str:
        css_selector = f"{selector.component}.{selector.tag_class}"
        if selector.tag_class == "":
            css_selector = f"{selector.component}"

        matches = {
            match.attributes["href"].strip() for match in block.css(css_selector)
        }

        if not matches:
            return "NoURLFound"

        if len(matches) != 1:
            raise ParseError("Contains more than 1 matches")

        return matches.pop()
