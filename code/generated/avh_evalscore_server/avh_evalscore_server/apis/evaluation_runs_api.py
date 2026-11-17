# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from avh_evalscore_server.apis.evaluation_runs_api_base import BaseEvaluationRunsApi
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
from typing import Optional, Union
from typing_extensions import Annotated
from uuid import UUID
from avh_evalscore_server.models.error_details import ErrorDetails
from avh_evalscore_server.models.evaluation_result_list_response import EvaluationResultListResponse
from avh_evalscore_server.models.evaluation_result_sort_by import EvaluationResultSortBy
from avh_evalscore_server.models.evaluation_run import EvaluationRun
from avh_evalscore_server.models.evaluation_run_list_response import EvaluationRunListResponse
from avh_evalscore_server.models.evaluation_run_sort_by import EvaluationRunSortBy
from avh_evalscore_server.models.evaluation_run_status import EvaluationRunStatus
from avh_evalscore_server.models.sort_order import SortOrder
from avh_evalscore_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = avh_evalscore_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)

@router.get(
    "/v1/evaluations/{evaluationId}/cases/{caseId}/runs",
    responses={
        200: {"model": EvaluationRunListResponse, "description": "Evaluation case runs"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluation Runs"],
    summary="List evaluation case runs",
    response_model_by_alias=True,
)
async def list_evaluation_case_runs(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    caseId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation case.")] = Path(..., description="UUID of the evaluation case."),
    offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")] = Query(0, description="Number of records to skip.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")] = Query(20, description="Maximum records to return.", alias="limit", ge=1, le=100),
    order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")] = Query('DESC', description="Direction applied to the selected sort field.", alias="order"),
    sort_by: Annotated[Optional[EvaluationRunSortBy], Field(description="Field used to order evaluation runs.")] = Query('CREATED_AT', description="Field used to order evaluation runs.", alias="sortBy"),
    status: Annotated[Optional[EvaluationRunStatus], Field(description="Return only runs in this lifecycle state.")] = Query(None, description="Return only runs in this lifecycle state.", alias="status"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationRunListResponse:
    """Returns a paginated history of runs whose immutable snapshot contains the case."""
    if not BaseEvaluationRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationRunsApi.subclasses[0]().list_evaluation_case_runs(evaluationId, caseId, offset, limit, order, sort_by, status)

@router.post(
    "/v1/evaluations/{evaluationId}/cases/{caseId}/runs",
    responses={
        202: {"model": EvaluationRun, "description": "Evaluation case run accepted"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=202,
    tags=["Evaluation Runs"],
    summary="Schedule one evaluation case",
    response_model_by_alias=True,
)
async def schedule_evaluation_case_run(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    caseId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation case.")] = Path(..., description="UUID of the evaluation case."),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationRun:
    """Captures the current evaluation configuration and the requested owned case, then schedules its asynchronous execution. The resulting run contains a single immutable case snapshot."""
    if not BaseEvaluationRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationRunsApi.subclasses[0]().schedule_evaluation_case_run(evaluationId, caseId)

@router.get(
    "/v1/evaluations/{evaluationId}/runs",
    responses={
        200: {"model": EvaluationRunListResponse, "description": "Evaluation runs"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluation Runs"],
    summary="List evaluation runs",
    response_model_by_alias=True,
)
async def list_evaluation_runs(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")] = Query(0, description="Number of records to skip.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")] = Query(20, description="Maximum records to return.", alias="limit", ge=1, le=100),
    order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")] = Query('DESC', description="Direction applied to the selected sort field.", alias="order"),
    sort_by: Annotated[Optional[EvaluationRunSortBy], Field(description="Field used to order evaluation runs.")] = Query('CREATED_AT', description="Field used to order evaluation runs.", alias="sortBy"),
    status: Annotated[Optional[EvaluationRunStatus], Field(description="Return only runs in this lifecycle state.")] = Query(None, description="Return only runs in this lifecycle state.", alias="status"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationRunListResponse:
    """Returns a paginated list of historical and active runs for an evaluation."""
    if not BaseEvaluationRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationRunsApi.subclasses[0]().list_evaluation_runs(evaluationId, offset, limit, order, sort_by, status)

@router.post(
    "/v1/evaluations/{evaluationId}/runs",
    responses={
        202: {"model": EvaluationRun, "description": "Evaluation run accepted"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=202,
    tags=["Evaluation Runs"],
    summary="Schedule an evaluation run",
    response_model_by_alias=True,
)
async def schedule_evaluation_run(
    evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")] = Path(..., description="UUID of the evaluation."),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationRun:
    """Captures the current evaluation definition and schedules it for asynchronous processing."""
    if not BaseEvaluationRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationRunsApi.subclasses[0]().schedule_evaluation_run(evaluationId)

@router.get(
    "/v1/evaluation-runs/{runId}",
    responses={
        200: {"model": EvaluationRun, "description": "Evaluation run"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluation Runs"],
    summary="Get an evaluation run",
    response_model_by_alias=True,
)
async def get_evaluation_run(
    runId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation run.")] = Path(..., description="UUID of the evaluation run."),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationRun:
    """Returns the status, immutable configuration snapshot, and failure detail of one run."""
    if not BaseEvaluationRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationRunsApi.subclasses[0]().get_evaluation_run(runId)

@router.get(
    "/v1/evaluation-runs/{runId}/results",
    responses={
        200: {"model": EvaluationResultListResponse, "description": "Evaluation results"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        422: {"model": ErrorDetails, "description": "The request is syntactically valid but violates a domain rule."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluation Runs"],
    summary="List immutable evaluation results",
    response_model_by_alias=True,
)
async def list_evaluation_run_results(
    runId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation run.")] = Path(..., description="UUID of the evaluation run."),
    offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")] = Query(0, description="Number of records to skip.", alias="offset", ge=0),
    limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")] = Query(20, description="Maximum records to return.", alias="limit", ge=1, le=100),
    order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")] = Query('DESC', description="Direction applied to the selected sort field.", alias="order"),
    sort_by: Annotated[Optional[EvaluationResultSortBy], Field(description="Field used to order evaluation results.")] = Query('CREATED_AT', description="Field used to order evaluation results.", alias="sortBy"),
    passed: Annotated[Optional[bool], Field(description="Return only passing or failing result attempts.")] = Query(None, description="Return only passing or failing result attempts.", alias="passed"),
    case_id: Annotated[Optional[Annotated[UUID, Field(strict=True)]], Field(description="Return only result attempts for this evaluation case.")] = Query(None, description="Return only result attempts for this evaluation case.", alias="caseId"),
    min_score: Annotated[Optional[Annotated[float, Field(le=1, ge=0)]], Field(description="Inclusive lower score bound.")] = Query(None, description="Inclusive lower score bound.", alias="minScore"),
    max_score: Annotated[Optional[Annotated[float, Field(le=1, ge=0)]], Field(description="Inclusive upper score bound.")] = Query(None, description="Inclusive upper score bound.", alias="maxScore"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationResultListResponse:
    """Returns a paginated list of result attempts produced by the requested run."""
    if not BaseEvaluationRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationRunsApi.subclasses[0]().list_evaluation_run_results(runId, offset, limit, order, sort_by, passed, case_id, min_score, max_score)

@router.post(
    "/v1/evaluation-runs/{runId}/cancellations",
    responses={
        200: {"model": EvaluationRun, "description": "Evaluation run cancelled"},
        401: {"model": ErrorDetails, "description": "Authentication is required or failed."},
        404: {"model": ErrorDetails, "description": "The requested resource was not found."},
        409: {"model": ErrorDetails, "description": "The operation conflicts with the current state of the resource."},
        500: {"model": ErrorDetails, "description": "An unexpected server error occurred."},
    },
    status_code=200,
    tags=["Evaluation Runs"],
    summary="Cancel an evaluation run",
    response_model_by_alias=True,
)
async def cancel_evaluation_run(
    runId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation run.")] = Path(..., description="UUID of the evaluation run."),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> EvaluationRun:
    """Requests cancellation of a run that has not reached a terminal state."""
    if not BaseEvaluationRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseEvaluationRunsApi.subclasses[0]().cancel_evaluation_run(runId)
