from typing import Literal
from pydantic import BaseModel, conint


class DataObjectMeasure(BaseModel):
    Value: int
    Invalidity: Literal[0, 1, 2]
    ErrorCode: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8]
    Timetag: conint(gt=0)  # type: ignore


# TODO: inserire i check relativi a Invalidity ed Errorcode (p. 35 PAS)


class DataObjectSateAlarm(BaseModel):
    Value: int
    Invalidity: bool
    Timetag: conint(gt=0)  # type: ignore
