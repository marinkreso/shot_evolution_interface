from typing import Callable
import pytest
import inspect

from pdf_generator.VisualGenerator import VisualGenerator

from pdf_generator.services.tests.helpers import (
    get_distinct_visuals_ids,
    read_data_source_outputs,
    serialize_data,
)


@pytest.mark.parametrize(
    "test_repo,expected", [("left_handed", True), ("right_handed", False)]
)
def test_is_lefthanded(data_repositories, test_repo, expected):
    assert data_repositories[test_repo].is_lefthanded() == expected


@pytest.mark.parametrize("visual_id", get_distinct_visuals_ids())
def test_returned_data_keys_matching_templates_signature_keys(
    data_repositories, report_meta_data_repository, visual_id
):
    # Fetch visual data from the database
    visual = report_meta_data_repository.get_visual_by_id(visual_id)

    data_repository = data_repositories["near_empty"]
    data_source: Callable = visual.get_data_source()
    data_dict = data_source(
        data_repository, **VisualGenerator.parse_args(visual.data_source_args)
    )
    data_keys = data_dict.keys()
    template_inspection = inspect.getfullargspec(visual.get_template())

    # Remove keys given by the generator and keys with default values
    keys_given_by_generator = ["player_name"]
    template_keys = {
        key for key in template_inspection.args if key not in keys_given_by_generator
    }
    data_keys = {key for key in data_keys if key not in template_inspection.kwonlyargs}

    assert data_keys == template_keys


@pytest.mark.parametrize("visual_id,expected_output", read_data_source_outputs())
@pytest.mark.parametrize("test_repo", ["left_handed", "right_handed", "near_empty"])
def test_data_source_returned_data_with_desired_output(
    data_repositories,
    report_meta_data_repository,
    visual_id,
    expected_output,
    test_repo,
):
    visual = report_meta_data_repository.get_visual_by_id(visual_id)
    data_source: Callable = visual.get_data_source()
    data_dict = data_source(
        data_repositories[test_repo],
        **VisualGenerator.parse_args(visual.data_source_args)
    )
    assert serialize_data(data_dict) == expected_output[test_repo]
