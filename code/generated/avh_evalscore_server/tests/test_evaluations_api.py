# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field  # noqa: F401
from typing import Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from uuid import UUID  # noqa: F401
from avh_evalscore_server.models.create_evaluation_case_request import CreateEvaluationCaseRequest  # noqa: F401
from avh_evalscore_server.models.create_evaluation_request import CreateEvaluationRequest  # noqa: F401
from avh_evalscore_server.models.error_details import ErrorDetails  # noqa: F401
from avh_evalscore_server.models.evaluation import Evaluation  # noqa: F401
from avh_evalscore_server.models.evaluation_case import EvaluationCase  # noqa: F401
from avh_evalscore_server.models.evaluation_case_kind import EvaluationCaseKind  # noqa: F401
from avh_evalscore_server.models.evaluation_case_list_response import EvaluationCaseListResponse  # noqa: F401
from avh_evalscore_server.models.evaluation_case_sort_by import EvaluationCaseSortBy  # noqa: F401
from avh_evalscore_server.models.evaluation_list_response import EvaluationListResponse  # noqa: F401
from avh_evalscore_server.models.evaluation_sort_by import EvaluationSortBy  # noqa: F401
from avh_evalscore_server.models.sort_order import SortOrder  # noqa: F401
from avh_evalscore_server.models.target_kind import TargetKind  # noqa: F401
from avh_evalscore_server.models.update_evaluation_request import UpdateEvaluationRequest  # noqa: F401


def test_list_evaluations(client: TestClient):
    """Test case for list_evaluations

    List evaluations
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'DESC'),     ("sort_by", 'CREATED_AT'),     ("name", 'name_example'),     ("target_kind", avh_evalscore_server.TargetKind())]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/evaluations",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_evaluation(client: TestClient):
    """Test case for create_evaluation

    Create an evaluation
    """
    create_evaluation_request = avh_evalscore_server.CreateEvaluationRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/evaluations",
    #    headers=headers,
    #    json=create_evaluation_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_evaluation(client: TestClient):
    """Test case for get_evaluation

    Get an evaluation
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/evaluations/{evaluationId}".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_evaluation(client: TestClient):
    """Test case for update_evaluation

    Update an evaluation
    """
    update_evaluation_request = avh_evalscore_server.UpdateEvaluationRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PATCH",
    #    "/v1/evaluations/{evaluationId}".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    json=update_evaluation_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_evaluation_cases(client: TestClient):
    """Test case for list_evaluation_cases

    List evaluation cases
    """
    params = [("offset", 0),     ("limit", 20),     ("order", 'DESC'),     ("sort_by", 'CREATED_AT'),     ("kind", avh_evalscore_server.EvaluationCaseKind())]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/evaluations/{evaluationId}/cases".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_evaluation_case(client: TestClient):
    """Test case for create_evaluation_case

    Create an evaluation case
    """
    create_evaluation_case_request = avh_evalscore_server.CreateEvaluationCaseRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/v1/evaluations/{evaluationId}/cases".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    json=create_evaluation_case_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_evaluation_case(client: TestClient):
    """Test case for get_evaluation_case

    Get an evaluation case
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/v1/evaluations/{evaluationId}/cases/{caseId}".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d'), caseId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_evaluation_case(client: TestClient):
    """Test case for update_evaluation_case

    Update an evaluation case
    """
    create_evaluation_case_request = avh_evalscore_server.CreateEvaluationCaseRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PATCH",
    #    "/v1/evaluations/{evaluationId}/cases/{caseId}".format(evaluationId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d'), caseId=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #    json=create_evaluation_case_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

