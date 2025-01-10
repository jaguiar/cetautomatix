import logging
from app.config.settings import settings

## Use the same logging config as the AlbertApi one
logging.basicConfig(format="%(levelname)s:%(asctime)s:%(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)
