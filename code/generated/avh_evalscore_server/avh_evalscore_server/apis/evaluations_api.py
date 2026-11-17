# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from avh_evalscore_server.apis.evaluations_api_base import BaseEvaluationsApi
import avh_evalscore_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)
from avh_evalscore_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field
from typing import Optional
from typing_extensions import Annotated
from uuid import UUID
from avh_evalscore_server.models.create_evaluation_case_request import CreateEvaluationCaseRequest
from avh_evalscore_server.models.create_evaluation_request import CreateEvaluationRequest
from avh_evalscore_server.models.error_details import ErrorDetails
from avh_evalscore_server.models.evaluation import Evaluation
from avh_evalscore_server.models.evaluation_case import EvaluationCase
from avh_evalscore_server.models.evaluation_case_kind import EvaluationCaseKind
from avh_evalscore_server.models.evaluation_case_list_response import EvaluationCaseListResponse
from avh_evalscore_server.models.evaluation_case_sort_by import EvaluationCaseSortBy
from avh_evalscore_server.models.evaluation_list_response import EvaluationListResponse
from avh_evalscore_server.models.evaluation_sort_by import EvaluationSortBy
from avh_evalscore_server.models.sort_order import SortOrder
from avh_evalscore_server.models.target_kind import TargetKind
from avh_evalscore_server.models.update_evaluation_request import UpdateEvaluationRequest
from avh_evalscore_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = avh_evalscore_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)

@router.get(
    "/v1/evaluations",
    responses={
        200: {"model": EvaluationListResponse, "description": "Evaluations"},
        400: {"model": ErrorDetails, "description": "The request is invalid."},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluations"],
    summary="List evaluations",
    response_model_by_alias=True,
)
async def list_evaluations(
    offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")] = Query(0, description="Number of records to skip.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")] = Query(20, description="Maximum records to return.", alias="limit", ge=1, le=100),
    order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")] = Query('DESC', description="Direction applied to the selected sort field.", alias="order"),
    sort_by: Annotated[Optional[EvaluationSortBy], Field(description="Field used to order evaluation suites.")] = Query('CREATED_AT', description="Field used to order evaluation suites.", alias="sortBy"),
    name: Annotated[Optional[Annotated[str, Field(strict=True, min_length=1, max_length=255)]], Field(description="Case-insensitive partial match on the evaluation name.")] = Query(None, description="Case-insensitive partial match on the evaluation name.", alias="name", min_length=1, max_length=255),
    target_kind: Annotated[Optional[TargetKind], Field(description="Return only evaluations with this target kind.")] = Query(None, description="Return only evaluations with this target kind.", alias="targetKind"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationListResponse:
    """Returns a paginated list of evaluation definitions available for execution."""
    if not BaseEvaluationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationsApi.subclasses[0]().list_evaluations(offset, limit, order, sort_by, name, target_kind)

@router.post(
    "/v1/evaluations",
    responses={
        201: {"model": Evaluation, "description": "Evaluation created"},
        400: {"model": ErrorDetails, "description": "The request is invalid."},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=201,
    tags=["Evaluations"],
    summary="Create an evaluation",
    response_model_by_alias=True,
)
async def create_evaluation(
    create_evaluation_request: CreateEvaluationRequest = Body(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Evaluation:
    """Creates an evaluation definition with a configured target and evaluation engine."""
    if not BaseEvaluationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationsApi.subclasses[0]().create_evaluation(create_evaluation_request)

@router.get(
    "/v1/evaluations/{evaluationId}",
    responses={
        200: {"model": Evaluation, "description": "Evaluation"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluations"],
    summary="Get an evaluation",
    response_model_by_alias=True,
)
async def get_evaluation(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Evaluation:
    """Returns the current configuration of the requested evaluation definition."""
    if not BaseEvaluationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationsApi.subclasses[0]().get_evaluation(evaluationId)

@router.patch(
    "/v1/evaluations/{evaluationId}",
    responses={
        200: {"model": Evaluation, "description": "Evaluation updated"},
        400: {"model": ErrorDetails, "description": "The request is invalid."},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluations"],
    summary="Update an evaluation",
    response_model_by_alias=True,
)
async def update_evaluation(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    update_evaluation_request: UpdateEvaluationRequest = Body(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Evaluation:
    """Applies a partial update to an evaluation definition without changing its identity."""
    if not BaseEvaluationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationsApi.subclasses[0]().update_evaluation(evaluationId, update_evaluation_request)

@router.get(
    "/v1/evaluations/{evaluationId}/cases",
    responses={
        200: {"model": EvaluationCaseListResponse, "description": "Evaluation cases"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluations"],
    summary="List evaluation cases",
    response_model_by_alias=True,
)
async def list_evaluation_cases(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")] = Query(0, description="Number of records to skip.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")] = Query(20, description="Maximum records to return.", alias="limit", ge=1, le=100),
    order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")] = Query('DESC', description="Direction applied to the selected sort field.", alias="order"),
    sort_by: Annotated[Optional[EvaluationCaseSortBy], Field(description="Field used to order evaluation cases.")] = Query('CREATED_AT', description="Field used to order evaluation cases.", alias="sortBy"),
    kind: Annotated[Optional[EvaluationCaseKind], Field(description="Return only cases of this kind.")] = Query(None, description="Return only cases of this kind.", alias="kind"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationCaseListResponse:
    """Returns a paginated list of cases belonging to the requested evaluation."""
    if not BaseEvaluationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationsApi.subclasses[0]().list_evaluation_cases(evaluationId, offset, limit, order, sort_by, kind)

@router.post(
    "/v1/evaluations/{evaluationId}/cases",
    responses={
        201: {"model": EvaluationCase, "description": "Evaluation case created"},
        400: {"model": ErrorDetails, "description": "The request is invalid."},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=201,
    tags=["Evaluations"],
    summary="Create an evaluation case",
    response_model_by_alias=True,
)
async def create_evaluation_case(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    create_evaluation_case_request: CreateEvaluationCaseRequest = Body(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationCase:
    """Adds a single-turn, multi-turn, or trajectory case to an evaluation definition."""
    if not BaseEvaluationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationsApi.subclasses[0]().create_evaluation_case(evaluationId, create_evaluation_case_request)

@router.get(
    "/v1/evaluations/{evaluationId}/cases/{caseId}",
    responses={
        200: {"model": EvaluationCase, "description": "Evaluation case"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluations"],
    summary="Get an evaluation case",
    response_model_by_alias=True,
)
async def get_evaluation_case(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    caseId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation case.")] = Path(..., description="UUID of the evaluation case."),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationCase:
    """Returns one case from the requested evaluation definition."""
    if not BaseEvaluationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationsApi.subclasses[0]().get_evaluation_case(evaluationId, caseId)

@router.patch(
    "/v1/evaluations/{evaluationId}/cases/{caseId}",
    responses={
        200: {"model": EvaluationCase, "description": "Evaluation case updated"},
        400: {"model": ErrorDetails, "description": "The request is invalid."},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluations"],
    summary="Update an evaluation case",
    response_model_by_alias=True,
)
async def update_evaluation_case(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    caseId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation case.")] = Path(..., description="UUID of the evaluation case."),
    create_evaluation_case_request: CreateEvaluationCaseRequest = Body(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationCase:
    """Replaces the input and expectations of an existing case in an evaluation."""
    if not BaseEvaluationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationsApi.subclasses[0]().update_evaluation_case(evaluationId, caseId, create_evaluation_case_request)
