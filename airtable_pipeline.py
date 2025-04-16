import dlt
from dlt_source_airtable import source

DEV_MODE = True


def load_airtable_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="airtable_pipeline", destination="duckdb", dev_mode=DEV_MODE
    )

    data = source(
        enterprise_id="ent...",
        limit=-1 if not DEV_MODE else 1,
    )
    info = pipeline.run(
        data,
        refresh="drop_sources" if DEV_MODE else None,
        # we need this in case new resources, etc. are added
        schema_contract={"columns": "evolve"},
    )
    print(info)  # noqa: T201


if __name__ == "__main__":
    load_airtable_data()
