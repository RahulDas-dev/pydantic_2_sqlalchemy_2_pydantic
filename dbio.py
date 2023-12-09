import os
import logging
from typing import Dict, Optional

from sqlalchemy import URL, create_engine, insert, select
from sqlalchemy.orm import Session, sessionmaker

from src.orms import Projects
from src.pydantic_model import (
    ColumnsDescription,
    ColumnType,
    DatasetDescriptor,
    Dtypes,
    ImputationScheme,
    ProjecStatus,
    ProjecType,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def insert_project(db: Session, object_in: Dict) -> Optional[Projects]:
    query_stmt = insert(Projects).values(**object_in).returning(Projects)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as err:
        db.rollback()
        logger.error(f"Session id {id(db)}| Error while Insert, Error {err}")
        data = None
    else:
        logger.info(f"Session id {id(db)}| Sucessfully inserted, id {data.id}")
    finally:
        return data


def select_project(db: Session, project_id: int) -> Optional[Projects]:
    query_stmt = select(Projects).where(Projects.id == project_id)
    status, data = None, None
    try:
        status = db.execute(query_stmt)
        data = status.scalars().one()
    except Exception as err:
        db.rollback()
        logger.error(f"Session id {id(db)}| Error while Insert, Error {err}")
        data = None
    else:
        logger.info(f"Session id {id(db)}| Sucessfully Selected, id {data.id}")
    finally:
        return data


if __name__ == "__main__":
    dataset = DatasetDescriptor(
        row_count=100,
        duplicate_columns=[],
        duplicate_row_count=0,
        outlier_count=0,
        is_imbalance=False,
        cloumns_info=[
            ColumnsDescription(
                name="job_type",
                col_type=ColumnType.FEATURES,
                dtype=Dtypes.CATEGORICAL,
                mean=None,
                median=None,
                mode=None,
                null_count=0,
                unique_valus=5,
                imputation_scheme=ImputationScheme.MODE,
            )
        ],
    )
    logger.info(f"dataset {dataset.model_dump()}")
    object_in = {
        "title": "Example Project 1",
        "descriptions": "Example Project 1 description",
        "ptype": ProjecType.DEPLOYABLE,
        "status": ProjecStatus.INIT,
        "dataset_info": dataset,
    }
    DB_PATH = os.path.join(os.curdir, "test_sqlite3.db")
    db_url = URL.create(drivername="sqlite", database=DB_PATH)
    logger.info(f"DB URL {db_url}")
    engine = create_engine(db_url, echo=False)
    Session = sessionmaker(engine)
    with Session.begin() as session:
        data = insert_project(db=session, object_in=object_in)

        # logger.info(f'data {data}')
        project = select_project(db=session, project_id=data.id)
        logger.info(f"dataset_info {project.ptype}, {project.dataset_info}")
        
