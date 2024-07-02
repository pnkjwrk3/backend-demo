import logging
import os
from sqlalchemy import create_engine
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def check_database_connection():
    try:
        database_url = os.getenv("DATABASE_URL")
        engine = create_engine(database_url)
        engine.connect()
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    check_database_connection()
