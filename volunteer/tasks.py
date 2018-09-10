from background_task import background
from logging import getLogger

logger = getLogger(__name__)

@background(schedule=15)
def check_any_event_ended(message):
    """Check whether some event is ended and we need to send peer-review notification"""
    print("checking", message)
    logger.debug('demo_task. message={0}'.format(message))
