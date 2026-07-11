import logging, sys
from .config import settings

def configure_logging():
    logging.basicConfig(
        level = settings.log_level,
        stream=sys.stderr,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )