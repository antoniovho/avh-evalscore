"""Environment-driven configuration for Evalscore."""

from pydantic import AnyHttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class PostgresDatabaseSettings(BaseSettings):
    """PostgreSQL connection settings loaded from the runtime environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DATABASE_",
        extra="ignore",
    )

    host: str
    port: int = 5432
    name: str
    user: str
    password: SecretStr
    pool_size: int = 5
    max_overflow: int = 10

    @property
    def connection_url(self) -> URL:
        """Build the async database URL without exposing its password in logs."""
        return URL.create(
            "postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


class LiteLLMProfile(BaseSettings):
    """Credential and endpoint values for a LiteLLM target or DeepEval judge model."""

    api_key: SecretStr
    api_base: AnyHttpUrl | None = None


class HttpTargetProfile(BaseSettings):
    """Fixed HTTP target endpoint that a persisted profile may invoke."""

    endpoint: AnyHttpUrl
    authorization: SecretStr | None = None
    timeout_seconds: float = Field(default=30.0, gt=0, le=300)


class AillmRuntimeProfile(BaseSettings):
    """One AILLM Runtime profile whose virtual key remains in the environment."""

    api_base: AnyHttpUrl
    api_key: SecretStr
    timeout_seconds: float = Field(default=120.0, gt=0, le=300)
    max_agent_turns: int = Field(default=8, ge=1, le=20)


class ProviderProfilesSettings(BaseSettings):
    """Named model and target profiles loaded from environment, never persisted in resources."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PROVIDERS_",
        extra="ignore",
    )

    litellm_profiles: dict[str, LiteLLMProfile] = Field(default_factory=dict)
    http_target_profiles: dict[str, HttpTargetProfile] = Field(default_factory=dict)
    aillm_runtime_profiles: dict[str, AillmRuntimeProfile] = Field(default_factory=dict)


class AuthSettings(BaseSettings):
    """OpenID Connect token validation settings loaded from the runtime environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AUTH_",
        extra="ignore",
    )

    issuer: str
    audience: str
    jwks_url: AnyHttpUrl
    jwks_cache_seconds: int = Field(default=300, ge=30, le=3600)


class WorkerSettings(BaseSettings):
    """Polling behavior for the in-process asynchronous evaluation worker."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="WORKER_",
        extra="ignore",
    )

    idle_poll_seconds: float = Field(default=1.0, gt=0, le=60)
