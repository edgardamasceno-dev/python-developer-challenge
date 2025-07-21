import structlog
from structlog.processors import JSONRenderer, TimeStamper, add_log_level


def setup_logging(log_level: str = "INFO"):
    structlog.configure(
        processors=[
            add_log_level,
            TimeStamper(fmt="iso"),
            JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )