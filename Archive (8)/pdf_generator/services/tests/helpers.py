import os
import csv
import json
import shutil
from enum import Enum
from tempfile import NamedTemporaryFile
from typing import Dict, List, Optional, Tuple

from tinydb import TinyDB

import main
from pdf_generator.models.db_models import Visual
from pdf_generator.VisualGenerator import VisualGenerator
from pdf_generator.services.JsonAggregateDAL import JsonAggregateDAL
from pdf_generator.services.ReportMetaDataRepository import ReportMetaDataRepository
from pdf_generator.services.dataRepository import DataRepository


def get_distinct_visuals_ids() -> List[Tuple]:
    distinct_visuals = {}
    meta_data = ReportMetaDataRepository(main.CONFIG["database"]["connection_str"])
    for visual in meta_data.get_all_visuals():
        key = (visual.template_id, visual.data_source_id)

        if distinct_visuals.get(key) is None:
            distinct_visuals[key] = visual.id

    return list(distinct_visuals.values())


def read_data_source_outputs() -> List[Tuple]:
    db = TinyDB("src/pdf_generator/services/tests/sample_data/db.json")
    data_source_outputs = []

    for visual in db.all():
        data_source_outputs.append((visual.pop("id"), visual))
    return data_source_outputs


def read_data_source_outputs_csv() -> List[Tuple]:
    data_source_outputs: Dict[int, Dict] = {}

    name_keys_mapping = {
        "left-handed": "left_handed",
        "right-handed": "right_handed",
        "near-empty": "near_empty",
    }
    for file_name in ("left-handed", "right-handed", "near-empty"):
        with open(
            os.path.join(
                os.getcwd(),
                f"src/pdf_generator/services/tests/sample_data/{file_name}.csv",
            )
        ) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_source_outputs[int(row["id"])] = data_source_outputs.get(
                    int(row["id"]), {}
                )
                data_source_outputs[int(row["id"])][
                    name_keys_mapping[file_name]
                ] = json.loads(row["output"])

    return list(data_source_outputs.items())


def serialize_data(data: Dict) -> Dict:
    for key, value in data.items():
        if isinstance(value, Enum):
            data[key] = value.value

    return json.loads(json.dumps(data))


def get_visual_serialized_data(visual: Visual, data_repo: DataRepository):
    data_source = visual.get_data_source()
    data_dict = data_source(
        data_repo,
        **VisualGenerator.parse_args(visual.data_source_args),
    )
    for key, value in data_dict.items():
        if isinstance(value, Enum):
            data_dict[key] = value.value
    return data_dict


def update_csv_test_cases(json_file_name: str, visual_id: Optional[int] = None) -> None:
    test_files_path = "src/pdf_generator/services/tests/sample_data"
    json_file_full_path = os.path.join(
        os.getcwd(),
        f"{test_files_path}/{json_file_name}.json",
    )
    csv_file_full_path = f"{test_files_path}/{json_file_name}.csv"
    tempfile = NamedTemporaryFile(mode="w", delete=False)

    with open(csv_file_full_path) as csv_file, tempfile:
        data_repository = DataRepository(JsonAggregateDAL(json_file_full_path))
        fieldnames = ["id", "output"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        reader = csv.DictReader(tempfile, fieldnames=fieldnames)
        meta_data = ReportMetaDataRepository(main.CONFIG["database"]["connection_str"])

        # Update every row in the file
        if visual_id is None:
            visuals = meta_data.get_all_visuals()[:-1]
            writer.writeheader()
            for visual in visuals:
                writer.writerow(
                    {
                        "id": visual.id,
                        "output": json.dumps(
                            get_visual_serialized_data(visual, data_repository)
                        ),
                    }
                )

        # Update one row in the file
        else:
            for row in reader:
                if row["id"] == visual_id:
                    visual = meta_data.get_visual_by_id(visual_id)

                    row["output"] = json.dumps(
                        get_visual_serialized_data(visual, data_repository)
                    )
                row = {"id": row["id"], "output": row["output"]}
                writer.writerow(row)

        # Override the old file
        shutil.move(tempfile.name, csv_file_full_path)


def update_outputs_db():
    from pdf_generator.services.tests.conftest import (
        data_repositories,
        report_meta_data_repository,
    )

    db = TinyDB("src/pdf_generator/services/tests/sample_data/db.json")
    db.drop_tables()
    data_repos = data_repositories()
    meta_data = report_meta_data_repository()
    for visual in meta_data.get_all_visuals():
        if visual.id == 111:
            continue

        visual_data = {
            "id": visual.id,
        }
        data_source = visual.get_data_source()
        for name, data_repo in data_repos.items():
            data_dict = data_source(
                data_repo,
                **VisualGenerator.parse_args(visual.data_source_args),
            )
            for key, value in data_dict.items():
                if isinstance(value, Enum):
                    data_dict[key] = value.value

            visual_data[name] = data_dict
        db.insert(visual_data)
