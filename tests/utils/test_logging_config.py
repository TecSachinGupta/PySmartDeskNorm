from constants import PAGE_ID_DASHBOARD, SIGNAL_NAVIGATE
from utils.logging_config import configure_logging, get_logger


def test_logging_helpers_are_available():
    configure_logging()
    logger = get_logger("phase3.test")
    assert logger.name == "phase3.test"
    assert SIGNAL_NAVIGATE == "navigate"
    assert PAGE_ID_DASHBOARD == "dashboard"
