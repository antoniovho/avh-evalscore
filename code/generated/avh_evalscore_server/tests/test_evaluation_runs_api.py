# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field  # noqa: F401
from typing import Optional, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from uuid import UUID  # noqa: F401
from avh_evalscore_server.models.error_details import ErrorDetails  # noqa: F401
from avh_evalscore_server.models.evaluation_result_list_response import EvaluationResultListResponse  # noqa: F401
from avh_evalscore_server.models.evaluation_result_sort_by import EvaluationResultSortBy  # noqa: F401
from avh_evalscore_server.models.evaluation_run import EvaluationRun  # noqa: F401
from avh_evalscore_server.models.evaluation_run_list_response import EvaluationRunListResponse  # noqa: F401
from avh_evalscore_server.models.evaluation_run_sort_by import EvaluationRunSortBy  # noqa: F401
from avh_evalscore_server.models.evaluation_run_status import EvaluationRunStatus  # noqa: F401
from avh_evalscore_server.models.sort_order import SortOrder  # noqa: F401


def test_list_evaluation_case_runs(client: TestClient):
    """Test case for list_evaluation_case_runs

    List evaluation case runs
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'DESC'),     ("sort_by", 'CREATED_AT'),     ("status", avh_evalscore_server.EvaluationRunStatus())]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/evaluations/{evaluationId}/cases/{caseId}/runs".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d'), caseId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_schedule_evaluation_case_run(client: TestClient):
    """Test case for schedule_evaluation_case_run

    Schedule one evaluation case
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/evaluations/{evaluationId}/cases/{caseId}/runs".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d'), caseId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_evaluation_runs(client: TestClient):
    """Test case for list_evaluation_runs

    List evaluation runs
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'DESC'),     ("sort_by", 'CREATED_AT'),     ("status", avh_evalscore_server.EvaluationRunStatus())]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/evaluations/{evaluationId}/runs".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_schedule_evaluation_run(client: TestClient):
    """Test case for schedule_evaluation_run

    Schedule an evaluation run
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/evaluations/{evaluationId}/runs".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_evaluation_run(client: TestClient):
    """Test case for get_evaluation_run

    Get an evaluation run
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/evaluation-runs/{runId}".format(runId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_evaluation_run_results(client: TestClient):
    """Test case for list_evaluation_run_results

    List immutable evaluation results
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'DESC'),     ("sort_by", 'CREATED_AT'),     ("passed", True),     ("case_id", UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),     ("min_score", 3.4),     ("max_score", 3.4)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/evaluation-runs/{runId}/results".format(runId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_cancel_evaluation_run(client: TestClient):
    """Test case for cancel_evaluation_run

    Cancel an evaluation run
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/evaluation-runs/{runId}/cancellations".format(runId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

