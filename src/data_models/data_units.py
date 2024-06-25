from pydantic import BaseModel, conint, validator, Field
from typing import Dict, Literal, Optional
import uuid
from enums.project_enums import CyclicEnums, SpontaneousEnums, StateAlarmEnums
from data_models.data_object import DataObjectMeasure, DataObjectSateAlarm


# Message from CIR to RO
class CyclicMeasure(BaseModel):
    UUID: uuid.UUID
    Timetag: conint(gt=0)  # type: ignore
    Data: Dict[str, DataObjectMeasure]

    @validator("Data")
    def validate_dataobject_keys(cls, value: dict):

        if set(value.keys()) != {enum.value for enum in CyclicEnums}:
            raise ValueError("Not all keys are present in Cyclic Measure Dataobject")
        return value


class SpontaneousMeasure(BaseModel):
    UUID: uuid.UUID
    Timetag: conint(gt=0)  # type: ignore
    Data: Dict[str, DataObjectMeasure]

    @validator("Data")
    def validate_dataobject_keys(cls, value: dict):
        if set(value.keys()) != {enum.value for enum in SpontaneousEnums}:
            raise ValueError("Not all keys are present in Spontaneous Measure Dataobject")
        return value


class StateAlarm(BaseModel):
    UUID: uuid.UUID
    Timetag: conint(gt=0)  # type: ignore
    Data: Dict[str, DataObjectSateAlarm]

    @validator("Data")
    def validate_dataobject_keys(cls, value: dict):
        if set(value.keys()) != {enum.value for enum in StateAlarmEnums}:
            raise ValueError("Not all keys are present in State-Alarm Dataobject")
        return value


# Commands from RO to CIR
class CommandLimitPowerDuration(BaseModel):
    """
    PAS pg. 33, riga 698, keyword: LD_CIR/CSIDWMX1.WLimPctSpt.ctlVal.
    Limite alla potenza massima [W] dell’infrastruttura di ricarica da garantire per tutta la durata di tempo in [s]
    dall'invio del comando.
    """

    class Config:
        extra = "forbid"

    UUID: uuid.UUID
    Timetag: int = Field(description="unix timestamp of when the command was sent", gt=0)
    MaximumPower: int = Field(description="maximum power limit [W] for the recharging infrastructure", ge=0)
    Duration: int = Field(description="validity duration [s] of the command, from the Timetag instant", gt=0)


class CommandLimitPowerUntil(BaseModel):
    """
    PAS pg. 33, riga 701, keyword: LD_CIR/CSIDWMX2.WLimPctSpt.ctlVal.
    Limite alla potenza massima [W] dell’infrastruttura di ricarica da mantenere per durata di tempo [s] dalla
    ricezione del comando.
    """

    class Config:
        extra = "forbid"

    UUID: uuid.UUID
    Timetag: int = Field(description="unix timestamp of when the command was sent", gt=0)
    MaximumPower: int = Field(description="maximum power limit [W] for the recharging infrastructure", ge=0)
    Tmax: int = Field(description="unix timestamp until which the command must be enforced", gt=0)

    @validator("Tmax")
    def ensure_positive_command_duration(cls, value, values):
        if values["Timetag"] >= value:
            raise ValueError(f"Given power setpoint ending in the past! \n {cls.json()}")
        return value


class CommandSuspendDuration(BaseModel):
    """
    PAS pg. 34, riga 704, keyword: LD_CIR/CSIDESE1.ClcStr.ctlVal.
    Sospensione totale del servizio di ricarica da garantire per tutta la durata di tempo in [s] dall'invio del comando.
    """

    class Config:
        extra = "forbid"

    UUID: uuid.UUID
    Timetag: int = Field(description="unix timestamp of when the command was sent", gt=0)
    Duration: int = Field(description="validity duration [s] of the command, from the Timetag instant", gt=0)


class CommandSuspendUntil(BaseModel):
    """
    PAS pg. 34, riga 706, keyword: LD_CIR/CSIDESE2.ClcStr.ctlVal.
    Sospensione totale del servizio di ricarica da garantire fino al tempo indicato.
    """

    class Config:
        extra = "forbid"

    UUID: uuid.UUID
    Timetag: int = Field(description="unix timestamp of when the command was sent", gt=0)
    Tmax: int = Field(description="unix timestamp until which the command must be enforced", gt=0)

    @validator("Tmax")
    def ensure_positive_command_duration(cls, value, values):
        if values["Timetag"] >= value:
            raise ValueError(f"Given power suspension ending in the past! \n {cls.json()}")
        return value


# Acknoledgements
class AcknowledgeMeasureState(BaseModel):
    """Messaggio di acknowledge in conseguenza ad una misura oppure uno stato"""

    class Config:
        extra = "forbid"

    UUID: uuid.UUID
    Timetag: conint(gt=0)  # type: ignore
    Value: bool


class AcknowledgeCommand(BaseModel):
    """Messaggio di acknowledge seguito alla ricezione di un comando"""

    UUID: uuid.UUID
    Timetag: conint(gt=0)  # type: ignore
    MaximumPower: Optional[int] = Field(description="maximum power limit [W] for the recharging infrastructure", ge=0)
    Duration: Optional[conint(gt=0)]  # type: ignore
    Tmax: Optional[int] = Field(description="unix timestamp until which the command must be enforced", gt=0)
    Ack: bool
    Cause: Literal[0, 1, 2]
