import logging.handlers
import sys

from . import constants

_log_dir = constants.LOGS_DIR
if not _log_dir.exists():
    _log_dir.mkdir()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(constants.APP_NAME)
