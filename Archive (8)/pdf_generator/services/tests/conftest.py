import os
import pytest

import main
from pdf_generator.services.JsonAggregateDAL import JsonAggregateDAL
from pdf_generator.services.ReportMetaDataRepository import ReportMetaDataRepository
from pdf_generator.services.dataRepository import DataRepository


@pytest.fixture(scope="module")
def data_repositories():
    data_path = os.path.join(
        os.getcwd(),
        "src/pdf_generator/services/tests/sample_data",
    )
    return {
        "right_handed": DataRepository(
            JsonAggregateDAL(
                f"{data_path}/right-handed.json",
            )
        ),
        "left_handed": DataRepository(
            JsonAggregateDAL(
                f"{data_path}/left-handed.json",
            )
        ),
        "near_empty": DataRepository(
            JsonAggregateDAL(
                f"{data_path}/near-empty.json",
            )
        ),
    }


@pytest.fixture(scope="module")
def report_meta_data_repository():
    return ReportMetaDataRepository(main.CONFIG["database"]["connection_str"])
