# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

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

class BaseEvaluationRunsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseEvaluationRunsApi.subclasses = BaseEvaluationRunsApi.subclasses + (cls,)
    async def list_evaluation_case_runs(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
        caseId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation case.")],
        offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")],
        order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")],
        sort_by: Annotated[Optional[EvaluationRunSortBy], Field(description="Field used to order evaluation runs.")],
        status: Annotated[Optional[EvaluationRunStatus], Field(description="Return only runs in this lifecycle state.")],
    ) -> EvaluationRunListResponse:
        """Returns a paginated history of runs whose immutable snapshot contains the case."""
        ...


    async def schedule_evaluation_case_run(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
        caseId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation case.")],
    ) -> EvaluationRun:
        """Captures the current evaluation configuration and the requested owned case, then schedules its asynchronous execution. The resulting run contains a single immutable case snapshot."""
        ...


    async def list_evaluation_runs(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
        offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")],
        order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")],
        sort_by: Annotated[Optional[EvaluationRunSortBy], Field(description="Field used to order evaluation runs.")],
        status: Annotated[Optional[EvaluationRunStatus], Field(description="Return only runs in this lifecycle state.")],
    ) -> EvaluationRunListResponse:
        """Returns a paginated list of historical and active runs for an evaluation."""
        ...


    async def schedule_evaluation_run(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
    ) -> EvaluationRun:
        """Captures the current evaluation definition and schedules it for asynchronous processing."""
        ...


    async def get_evaluation_run(
        self,
        runId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation run.")],
    ) -> EvaluationRun:
        """Returns the status, immutable configuration snapshot, and failure detail of one run."""
        ...


    async def list_evaluation_run_results(
        self,
        runId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation run.")],
        offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")],
        order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")],
        sort_by: Annotated[Optional[EvaluationResultSortBy], Field(description="Field used to order evaluation results.")],
        passed: Annotated[Optional[bool], Field(description="Return only passing or failing result attempts.")],
        case_id: Annotated[Optional[Annotated[UUID, Field(strict=True)]], Field(description="Return only result attempts for this evaluation case.")],
        min_score: Annotated[Optional[Annotated[float, Field(le=1, ge=0)]], Field(description="Inclusive lower score bound.")],
        max_score: Annotated[Optional[Annotated[float, Field(le=1, ge=0)]], Field(description="Inclusive upper score bound.")],
    ) -> EvaluationResultListResponse:
        """Returns a paginated list of result attempts produced by the requested run."""
        ...


    async def cancel_evaluation_run(
        self,
        runId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation run.")],
    ) -> EvaluationRun:
        """Requests cancellation of a run that has not reached a terminal state."""
        ...
