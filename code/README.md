# Evalscore Backend

Python backend for authoring deterministic LLM evaluation suites and executing
them asynchronously. The source OpenAPI contract is maintained in the
[`antoniovho/app-devtools`](https://github.com/antoniovho/app-devtools)
repository, under `apis/avh-evalscore/rest`.

The architecture keeps pure domain models in `domain/`, input and output ports
in `application/ports/`, use-case implementations in `application/use_cases/`,
and integrations in `infrastructure/adapters/`. No company framework is used.

DeepEval is the evaluation engine. It currently exposes its `G_EVAL` metric,
configured with an LLM-as-a-judge model. The selected judge is supplied through
DeepEval's LiteLLM integration, so it can be an OpenAI, Anthropic, Gemini,
Azure, local, or LiteLLM Proxy model.

Provider profiles reference only runtime secrets. Evaluation definitions persist
a profile name and model, never API keys or raw endpoints.

When a profile defines a LiteLLM Gateway URL, Evalscore checks its `/v1/models`
catalogue when a suite is created or updated and again immediately before a run.
The virtual key must be allowed to see both the selected judge model and, for a
LiteLLM target, the selected target model. HTTP targets are reported as
availability-unknown because their generic contract cannot expose an internal
model catalogue.

Every LiteLLM target invocation now persists a sanitized `MODEL` trace step:
the OpenAI-compatible request (`model` and `messages`) and normalized response
(including any tool calls) are stored as evaluation evidence. HTTP targets can
return their complete multi-step trace envelope, including `MODEL`, `TOOL`, and
`AGENT` steps. This is the same request/response trace principle used by the
local playground, but modelled as a provider-neutral domain artifact so that
trajectory, tool-use, skills, and orchestration checks do not depend on a UI.

The public application mounts the generated `avh_evalscore_server` routers.
`EvaluationsController` and `EvaluationRunsController` implement their base
interfaces and delegate only to application ports; `EvaluationRestMapper` is
the explicit boundary between generated transport types and domain values. A
background worker runs in the ASGI process and claims scheduled evaluation runs
from PostgreSQL.

## Local setup

### Prerequisites

- Python 3.12 or later, managed with [uv](https://docs.astral.sh/uv/)
- Docker Compose for the local PostgreSQL instance

### Configure and start PostgreSQL

Create the local configuration from the example. It is preconfigured for the
local Compose database. Replace the OIDC and provider placeholders before
making authenticated requests or executing an evaluation.

```bash
cp .env.example .env
cd resources/compose
docker compose up -d
docker compose ps
cd ../..
```

The Compose package creates a clean database from the ordered SQL scripts in
`resources/compose/postgres/init/`. The application never creates or migrates
tables at runtime. Its connection settings, initialization order, and reset
procedure are documented in
[`resources/compose/README.md`](resources/compose/README.md).

### Install and run the API

```bash
uv sync --extra dev
uv run uvicorn evalscore.main:create_application --factory --host 127.0.0.1 --port 8080
```

The service exposes its command routes under `/v1`. Its interactive OpenAPI
documentation is available at <http://127.0.0.1:8080/docs> and ReDoc at
<http://127.0.0.1:8080/redoc>. Every API request requires a bearer token
accepted by the configured JWT issuer, audience, and JWKS endpoint.

`PROVIDERS_LITELLM_PROFILES` and `PROVIDERS_HTTP_TARGET_PROFILES` are JSON maps.
See `.env.example` for their shape; supply real credentials through the local
environment or deployment secret store.

## Contract and generated server

The generated package in `generated/avh_evalscore_server/` is an implementation
detail of the published OpenAPI contract. Do not edit its generated router or
model files manually. When a new `avh-evalscore` contract release is available,
update the version, tag, artifact checksum in `pyproject.toml`, then run:

```bash
uv run --no-sync contract-sync avh-evalscore
uv run --no-sync generate-source --rest-server --api avh-evalscore-server
uv lock
uv sync --extra dev
```

The handwritten REST controllers and transport/domain mapper belong under
`evalscore/infrastructure/adapters/input/rest/`; they consume the regenerated
API base interfaces.

## Verification

The project Makefile provides the normal local checks:

```bash
make test
make lint
make verify
```

`make coverage` additionally produces terminal and XML coverage reports. The
unit suite covers domain invariants, use cases, model availability checks, and
the generated-transport boundary.
