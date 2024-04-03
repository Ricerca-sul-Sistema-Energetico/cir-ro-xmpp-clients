from enums.project_enums import (
    MessageADUEnums,
    CommandsADUEnums,
    AcknowledgeADUEnums,
)
from data_models.data_units import (
    CyclicMeasure,
    SpontaneousMeasure,
    StateAlarm,
    CommandLimitPowerDuration,
    CommandLimitPowerUntil,
    CommandSuspendDuration,
    CommandSuspendUntil,
    AcknowledgeMeasureState,
    AcknowledgeCommand,
)
from typing import Union
from pydantic import BaseModel, validator

association_adu = {
    MessageADUEnums.CYCLIC_MEASURE.value: CyclicMeasure,
    MessageADUEnums.SPONT_MEASURE.value: SpontaneousMeasure,
    MessageADUEnums.STATE_ALARM.value: StateAlarm,
    CommandsADUEnums.PWR_MAX_CSI_DURATION.value: CommandLimitPowerDuration,
    CommandsADUEnums.PWR_MAX_CSI_UNTIL.value: CommandLimitPowerUntil,
    CommandsADUEnums.SUSPEND_DURATION.value: CommandSuspendDuration,
    CommandsADUEnums.SUSPEND_UNTIL.value: CommandSuspendUntil,
    AcknowledgeADUEnums.ACKNOWLEDGE_MEASURE.value: AcknowledgeMeasureState,
    AcknowledgeADUEnums.ACKNOWLEDGE_COMMAND.value: AcknowledgeCommand,
}


class CirRoMessage(BaseModel):
    ADUtype: str
    DataUnit: Union[
        CyclicMeasure,
        SpontaneousMeasure,
        StateAlarm,
        CommandLimitPowerDuration,
        CommandLimitPowerUntil,
        CommandSuspendDuration,
        CommandSuspendUntil,
        AcknowledgeMeasureState,
        AcknowledgeCommand,
    ]

    @validator("ADUtype")
    def ensure_existing_adutype(cls, value: str):
        adu_messages = [item.value for item in MessageADUEnums]
        adu_commands = [item.value for item in CommandsADUEnums]
        adu_acknowledge = [item.value for item in AcknowledgeADUEnums]

        if value not in adu_messages + adu_commands + adu_acknowledge:
            raise ValueError(f"Not valid ADU type in the message! Recieved: {value}")

        return value

    @validator("DataUnit")
    def ensure_correct_data_unit(cls, value, values):

        if association_adu[values["ADUtype"]] is not type(value):
            type_found = type(value).__name__
            raise ValueError(
                f"Wrong association ADU type with Dataunit Content! Adu: {value} \n DataUnit: {type_found}"
            )
        return value
