from typing import Optional

from api.datamodels.api_inputs import StockQueryTypeModel, PaginationTypeBaseModel

from typing import List
from fastapi import Query


def get_prepared_query(
    name: Optional[str] = None,
    artist: Optional[str] = None,
    stock_type: Optional[str] = None,
    style: Optional[str] = None,
    year: Optional[List[float]] = Query(None),
    price: Optional[float] = None,
):
    def value_wrapper(value):
        return {"value": value}

    initialize_json = {}

    if name is not None:
        initialize_json["name"] = value_wrapper(name)
    if artist is not None:
        initialize_json["artist"] = value_wrapper(artist)
    if stock_type is not None:
        initialize_json["stock_type"] = value_wrapper(stock_type)
    if style is not None:
        initialize_json["style"] = value_wrapper(style)
    if year is not None:
        initialize_json["year"] = value_wrapper(year)
    if price is not None:
        initialize_json["price"] = value_wrapper(price)

    query_object = StockQueryTypeModel(**initialize_json)

    my_query = {}
    for key, item in query_object:
        try:
            my_query = {**my_query, **item.query(key)}
            pass
        except Exception as e:
            pass

    return my_query


def get_pagination(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
):

    json_data = {}

    if page is not None:
        json_data["page"] = page
    if per_page is not None:
        json_data["per_page"] = per_page

    return PaginationTypeBaseModel(**json_data)
