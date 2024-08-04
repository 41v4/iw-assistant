import logging


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - CUSTOM LOGGING - %(message)s",
    )
    return logging.getLogger(__name__)


logger = setup_logger()
