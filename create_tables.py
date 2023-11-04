import logging
import os

from sqlalchemy import URL, create_engine

from src.orms import meta

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)


logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.curdir, "test_sqlite3.db")


def _create_tables() -> None:
    logger.info("Creating Tables .....")
    db_url = URL.create(drivername="sqlite", database=DB_PATH)
    logger.info(f"DB URL {db_url}")
    engine = create_engine(db_url, echo=True)

    with engine.begin() as connection:
        return_code = meta.create_all(connection, checkfirst=True)
        logger.info(f"return_code {return_code}")
    engine.dispose()


if __name__ == "__main__":
    _create_tables()
