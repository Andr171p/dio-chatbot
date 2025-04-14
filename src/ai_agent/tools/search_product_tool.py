import logging

from typing import Any, Type, Optional, Union

from pathlib import Path

import pandas as pd

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


logger = logging.getLogger(__name__)


def format_search_product(product: dict) -> str:
    return (
        f"Артикул: {product["Код"]}\n"
        f"Наименование: {product["Наименование"]}\n"
        f"Цена: {product["Рекомендованная цена"]} руб."
    )


class SearchProductToolArgs(BaseModel):
    article_number: str = Field(..., description="Номер артикула")


class SearchProductTool(BaseTool):
    name: str = "SearchProductTool"
    description: str = "Ищет продукт по его артикулу"
    args_schema: Optional[Type[BaseModel]] = SearchProductToolArgs

    def __init__(self, file_path: Union[Path, str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._df = pd.read_csv(file_path)

    def _search_by_article_number(self, article_number: str) -> str:
        product_df: pd.DataFrame = self._df.loc[self._df["Код"] == article_number]
        product_dict = product_df.iloc[0].to_dict() if not product_df.empty else {}
        return format_search_product(product_dict)

    def _run(self, article_number: str) -> str:
        logger.info("---SEARCH PRODUCT---")
        return self._search_by_article_number(article_number)

    async def _arun(self, article_number: str) -> str:
        logger.info("---SEARCH PRODUCT---")
        return self._search_by_article_number(article_number)
