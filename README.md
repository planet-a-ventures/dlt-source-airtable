# dlt-source-airtable

[![PyPI version](https://img.shields.io/pypi/v/dlt-source-airtable)](https://pypi.org/project/dlt-source-airtable/)

[DLT](https://dlthub.com/) source for [airtable](https://www.airtable.com/).

Currently loads the following data:

| Table | Contains |
| -- | -- |
| `users` | Items of the `users` model that are users |
| `service_accounts` | Items of the `users` model that are service accounts |

## Why are you not using the `dlt-hub/verified-sources` airtable source / Differences

The [official verified source](https://github.com/dlt-hub/verified-sources/tree/master/sources/airtable)
has a few drawbacks:

- on usage of the verified source, a copy of the current state of
  the `dlt-hub/verified-sources` repository is copied into your project;
  Once you make changes to it, it effectively becomes a fork,
  making it hard to update after the fact.
- This makes use of a preexisting client implementation which uses Pydantic models

## Usage

Create a `.dlt/secrets.toml` with your API token:

```toml
airtable_token = "pat..."
```

You can create this token [here](https://airtable.com/create/tokens)
or as a Service **Admin** Account (preferred).

The scopes needed are as follows:

- `enterprise.user:read`
- `enterprise.account:read`

and then run the default source with optional list references:

```py
from dlt_source_airtable import source as airtable_source

pipeline = dlt.pipeline(
   pipeline_name="airtable_pipeline",
   destination="duckdb",
   dev_mode=True,
)
enterprise_id = "ent..."
airtable_data = airtable_source(enterprise_id)
pipeline.run(airtable_data)
```

### How to get your enterprise ID

Navigate to [your admin view](https://airtable.com/admin/) and you will see

> Account ID: ent...

in the sidebar and/or URL bar of your browser.

## Development

This project is using [devenv](https://devenv.sh/).

Commands:

| Command | What does it do? |
| -- | -- |
| `format` | Formats & lints all code |
| `sample-pipeline-run` | Runs the sample pipeline. |
| `sample-pipeline-show` | Starts the streamlit-based dlt hub |

### Run the sample

```sh
AIRTABLE_TOKEN=[pat...] \
  sample-pipeline-run
```

alternatively you can also create a `.dlt/secrets.toml`
(excluded from git) with the following content:

```toml
airtable_token = "pat..."
```
