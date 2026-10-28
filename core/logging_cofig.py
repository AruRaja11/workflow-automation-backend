import logging 
import logging.config 
import os 
from contextvars import ContextVar
from pathlib import Path

request_id_context: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get()
        return True


def setup_logging() -> None:
    log_level = os.getenv('LOG_LEVEL', "INFO").upper()

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "standard": {
                "format": (
                    "%(asctime)s | %(levelname)-8s | "
                    "%(request_id)s | %(name)s | %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "filters": {
            "request_id": {
                "()": RequestIdFilter,
            },
        },
        
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "filters": ["request_id"],
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "standard",
                "filters": ["request_id"],
                "filename": str(log_dir / "app.log"),
                "maxBytes": 5_000_000,
                "backupCount": 3,
                "encoding": "utf-8",
            },
        },

        "root": {
            "level": log_level,
            "handlers": ["console", "file"],
        },
    })
    