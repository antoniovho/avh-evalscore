# Evalscore

Contract-first Python service for authoring and executing reproducible LLM
evaluations. It uses standalone Python libraries and exposes DeepEval `G_EVAL` adapters.

The OpenAPI source is at
`/home/avelascohorcajada/personal-knowmad/app-devtools/apis/avh-evalscore/rest`.

## Development

```bash
cd code
uv sync --extra dev
make verify
uv run uvicorn evalscore.main:create_application --factory --reload
```
