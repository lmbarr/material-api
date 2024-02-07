import random
import time
from celery import Celery
from celery.utils.log import get_task_logger

from constants import MONGO_URI, BROKER_URI

logger = get_task_logger(__name__)

app = Celery('tasks', broker=BROKER_URI, backend=MONGO_URI)


@app.task()
def fooness(formula):
    logger.info('Starting calculations on formula ' + formula)
    time.sleep(15)
    logger.info('Ending calculations on formula ' + formula)
    return random.uniform(10.5, 75.5)
