"""Application-wide Opyoid injector."""

from opyoid import Injector

from evalscore.domain.domain_module import DomainModule
from evalscore.infrastructure.infrastructure_module import InfrastructureModule

_injector: Injector | None = None


def get_injector() -> Injector:
    """Return the process-wide injector, building it only when first required."""
    global _injector
    if _injector is None:
        _injector = Injector([DomainModule, InfrastructureModule])
    return _injector
