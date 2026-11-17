# Evalscore Backend

Python backend for authoring deterministic LLM evaluation suites and executing
them asynchronously. The API contract source is maintained separately at
`app-devtools/apis/avh-evalscore/rest`.

The architecture keeps pure domain models in `domain/`, input and output ports
in `application/ports/`, use-case implementations in `application/use_cases/`,
and integrations in `infrastructure/adapters/`. No company framework is used.

DeepEval is the only evaluation engine. It currently exposes its `G_EVAL`
metric, configured with an LLM-as-a-judge model. The selected model is passed
to DeepEval's official LiteLLM integration, so it can be an OpenAI, Anthropic,
Gemini, Azure, local, or LiteLLM Proxy model; LiteLLM is not an alternative
evaluation engine.

Provider profiles reference only runtime secrets. Evaluation definitions persist
a profile name and model, never API keys or raw endpoints.

When a profile defines a LiteLLM Gateway URL, Evalscore checks its `/v1/models`
catalogue when a suite is created or updated and again immediately before a run.
The virtual key must be allowed to see both the selected judge model and, for a
LiteLLM target, the selected target model. HTTP targets are reported as
availability-unknown because their generic contract cannot expose an internal
model catalogue.

## Local setup

Create a local `.env` from `.env.example` and supply a PostgreSQL database plus the OIDC issuer
used to validate access tokens. Provider profile credentials belong in the runtime secret store and
are never sent by API callers.

```bash
uv sync --extra dev
uv run alembic upgrade head
uv run uvicorn evalscore.main:create_application --factory --host 127.0.0.1 --port 8080
```

The service exposes its command routes under `/v1`. Every API request requires a bearer token
accepted by the configured JWT issuer, audience, and JWKS endpoint.

`PROVIDERS_LITELLM_PROFILES` and `PROVIDERS_HTTP_TARGET_PROFILES` are JSON maps.
See `.env.example` for their shape; supply real credentials through the local
environment or deployment secret store.
