from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ProjecType(str, Enum):
    DEPLOYABLE = "DEPLOYABLE"
    INMEMORY = "INMEMORY"
    SINGLESHOT = "SINGLESHOT"


class ProjecStatus(str, Enum):
    INIT = "INIT"
    DATALOAD = "DEPLOYABLE"
    PREPROCESS = "PREPROCESS"
    POSTPROCESS = "POSTPROCESS"


class Dtypes(str, Enum):
    INTERGER = "integers"
    FLOAT = "float"
    BOOLEAN = "bool"
    CATEGORICAL = "categorical"
    DATE = "date"


class ColumnType(str, Enum):
    FEATURES = "features"
    TARGET = "target"
    INDEX = "index"
    UNIQUEID = "unique-id"


class ImputationScheme(str, Enum):
    MEAN = "mean"
    MEDIAN = "median"
    MODE = "mode"
    VALUE = "value"


class ColumnsDescription(BaseModel):
    name: str
    col_type: ColumnType
    dtype: Dtypes
    mean: Optional[float] = Field(default=None)
    median: Optional[float] = Field(default=None)
    mode: Optional[float] = Field(default=None)
    null_count: Optional[int] = Field(default=None)
    unique_valus: Optional[int] = Field(default=None)
    imputation_scheme: ImputationScheme


class TargetStat(BaseModel):
    target_distributations: str


OUTLIER_DETECTION_SCHEME = Literal["Z_SCORE", "IQR"]


class CleaningStratagy(BaseModel):
    drop_duplicate_rows: bool
    drop_duplicate_column: bool
    rename_duplicate_columns: bool
    null_colums_drop_stratagy: float
    outlier_detection_scheme: OUTLIER_DETECTION_SCHEME
    drop_outlier: bool
    z_score_threshold: float
    iqr_range: float
    impute_null_values: bool


class PreprocessingStratagy(BaseModel):
    trnsfrom_binary_column: bool
    remove_datetime_column: bool
    split_datetime_column: bool


class DatasetDescriptor(BaseModel):
    row_count: int = Field(ge=0)
    cloumns_info: List[ColumnsDescription] = Field(default_factory=list)
    duplicate_row_count: int = Field(default=0, ge=0)
    duplicate_columns: List[str] = Field(default_factory=list)
    outlier_count: int = Field(ge=0)
    is_imbalance: Optional[bool] = Field(default=None)
