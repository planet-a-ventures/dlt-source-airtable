"""A source loading entities from airtable (airtable.com)"""

from pyairtable.models.schema import UserInfo
from enum import StrEnum
from typing import Any, Iterable, List, Sequence
import dlt
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
from pydantic import BaseModel
from .api_client import get_api_client


class Table(StrEnum):
    USERS = "users"
    SERVICE_ACCOUNTS = "service_accounts"


def pydantic_model_dump(model: BaseModel, **kwargs):
    """
    Dumps a Pydantic model to a dictionary, using the model's field names as keys and NOT observing the field aliases,
    which is important for DLT to correctly map the data to the destination.
    """
    return model.model_dump(by_alias=True, **kwargs)


def use_id(entity: UserInfo, **kwargs) -> dict:
    return pydantic_model_dump(entity, **kwargs) | {"_dlt_id": __get_id(entity)}


@dlt.resource(
    selected=False,
    parallelized=True,
)
def user_ids(enterprise_id: str) -> Iterable[TDataItem]:
    api_client = get_api_client()
    enterprise = api_client.enterprise(enterprise_id)
    info = enterprise.info()
    yield info.user_ids


# TODO: Workaround for the fact that when `add_limit` is used, the yielded entities
# become dicts instead of first-class entities
def __get_id(obj):
    if isinstance(obj, dict):
        return obj.get("id")
    return getattr(obj, "id", None)


@dlt.transformer(
    parallelized=True,
    table_name="users",
)
async def user_details(users: List[Any], enterprise_id: str):
    api_client = get_api_client()
    enterprise = api_client.enterprise(enterprise_id)
    users = enterprise.users(ids_or_emails=users)
    for user in users:
        table_name = (
            Table.SERVICE_ACCOUNTS.value
            if user.is_service_account
            else Table.USERS.value
        )

        yield dlt.mark.with_hints(
            item=use_id(user, exclude=["is_service_account"]),
            hints=dlt.mark.make_hints(
                table_name=table_name,
                primary_key="id",
                merge_key="id",
                write_disposition="merge",
            ),
            # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
            create_table_variant=True,
        )


@dlt.source(name="airtable")
def source(enterprise_id: str, limit=-1) -> Sequence[DltResource]:
    my_user_ids = user_ids(enterprise_id)
    if limit > 0:
        my_user_ids = my_user_ids.add_limit(limit)

    return my_user_ids | user_details(enterprise_id)


__all__ = ["source"]
