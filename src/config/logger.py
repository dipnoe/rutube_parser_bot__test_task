import logging

from config import settings

logging.basicConfig(
    filename=settings.logfile,
    level=logging.INFO,
    format="%(asctime)s: %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)
