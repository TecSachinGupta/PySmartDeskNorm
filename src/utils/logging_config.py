import logging

_LOG_LEVEL = logging.INFO


def configure_logging(level=_LOG_LEVEL):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        force=True,
    )
    return logging.getLogger()


def get_logger(name: str | None = None):
    logger_name = name or __name__
    return logging.getLogger(logger_name)
