import asyncio
import os
from typing import Callable

from constants.app_constants import (MONGODB_ANALYTICS_COLLECTION_NAME,
                                     MONGODB_FEEDBACK_COLLECTION_NAME,
                                     MONGODB_NAME)

import utils.mongo_db_util


def run_in_background(called_func: Callable):
    """
    Runs the passed callable as a background event.

    Args:
        called_func (Callable): function or method
    """
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, called_func, *args, *kwargs)
    return wrapped


@run_in_background
def perform_analytics(data):
    mongodb = utils.mongo_db_util.MongoDB(os.getenv(MONGODB_NAME))
    mongodb.insert(mongodb.db[os.getenv(
        MONGODB_ANALYTICS_COLLECTION_NAME)], data)


@run_in_background
def save_feedback(data):
    mongodb = utils.mongo_db_util.MongoDB(os.getenv(MONGODB_NAME))
    mongodb.insert(mongodb.db[os.getenv(
        MONGODB_FEEDBACK_COLLECTION_NAME)], data)
