# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

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

class BaseEvaluationsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseEvaluationsApi.subclasses = BaseEvaluationsApi.subclasses + (cls,)
    async def list_evaluations(
        self,
        offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")],
        order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")],
        sort_by: Annotated[Optional[EvaluationSortBy], Field(description="Field used to order evaluation suites.")],
        name: Annotated[Optional[Annotated[str, Field(strict=True, min_length=1, max_length=255)]], Field(description="Case-insensitive partial match on the evaluation name.")],
        target_kind: Annotated[Optional[TargetKind], Field(description="Return only evaluations with this target kind.")],
    ) -> EvaluationListResponse:
        """Returns a paginated list of evaluation definitions available for execution."""
        ...


    async def create_evaluation(
        self,
        create_evaluation_request: CreateEvaluationRequest,
    ) -> Evaluation:
        """Creates an evaluation definition with a configured target and evaluation engine."""
        ...


    async def get_evaluation(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
    ) -> Evaluation:
        """Returns the current configuration of the requested evaluation definition."""
        ...


    async def update_evaluation(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
        update_evaluation_request: UpdateEvaluationRequest,
    ) -> Evaluation:
        """Applies a partial update to an evaluation definition without changing its identity."""
        ...


    async def list_evaluation_cases(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
        offset: Annotated[Optional[Annotated[int, Field(ge=0)]], Field(description="Number of records to skip.")],
        limit: Annotated[Optional[Annotated[int, Field(le=100, ge=1)]], Field(description="Maximum records to return.")],
        order: Annotated[Optional[SortOrder], Field(description="Direction applied to the selected sort field.")],
        sort_by: Annotated[Optional[EvaluationCaseSortBy], Field(description="Field used to order evaluation cases.")],
        kind: Annotated[Optional[EvaluationCaseKind], Field(description="Return only cases of this kind.")],
    ) -> EvaluationCaseListResponse:
        """Returns a paginated list of cases belonging to the requested evaluation."""
        ...


    async def create_evaluation_case(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
        create_evaluation_case_request: CreateEvaluationCaseRequest,
    ) -> EvaluationCase:
        """Adds a single-turn, multi-turn, or trajectory case to an evaluation definition."""
        ...


    async def get_evaluation_case(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
        caseId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation case.")],
    ) -> EvaluationCase:
        """Returns one case from the requested evaluation definition."""
        ...


    async def update_evaluation_case(
        self,
        evaluationId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation.")],
        caseId: Annotated[Annotated[UUID, Field(strict=True)], Field(description="UUID of the evaluation case.")],
        create_evaluation_case_request: CreateEvaluationCaseRequest,
    ) -> EvaluationCase:
        """Replaces the input and expectations of an existing case in an evaluation."""
        ...
