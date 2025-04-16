import dlt
from pyairtable import Api

client: Api | None = None


def get_api_client(
    token: str = dlt.secrets["airtable_token"],
):
    global client

    if client is None:
        client = Api(token)
    return client
