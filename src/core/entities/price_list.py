from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    article_number: str
    name: str
    price: int

    def __str__(self) -> str:
        return (
            f"Артикул: {self.article_number}\n"
            f"Наименование: {self.name}\n"
            f"Цена: {self.price} руб."
        )


class PriceList(BaseModel):
    products: List[Product]
