from typing import Literal
from pydantic import BaseModel, conint


class DataObjectMeasure(BaseModel):
    Value: float
    Invalidity: Literal[0, 1, 2]  # Nell adu stato deve essere solo 1 o 2
    ErrorCode: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]  # Nell'Adu stato deve essere nullo
    Timetag: conint(gt=0)  # type: ignore


# TODO: inserire i check relativi a Invalidity ed Errorcode


class DataObjectSateAlarm(BaseModel):
    Value: float
    Invalidity: bool
    Timetag: conint(gt=0)  # type: ignore
