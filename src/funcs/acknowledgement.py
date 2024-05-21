from data_models.cir_ro_message import (
    CirRoMessage,
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
from enums.project_enums import AcknowledgeADUEnums
from typing import Union
import time
from typing import Literal


def generate_command_acknowledge(
    data_unit: Union[
        CommandLimitPowerDuration,
        CommandSuspendDuration,
        CommandLimitPowerUntil,
        CommandSuspendUntil,
    ],
    acknowledge_result: bool = True,
    cause: Literal[0, 1, 2, 3] = 0,
):
    if data_unit is not None:
        acknowledge_dict = data_unit.dict()
        acknowledge_dict["Ack"] = acknowledge_result
        acknowledge_dict["Cause"] = cause
        acknowledge_data_unit = AcknowledgeCommand(**acknowledge_dict)

        acknowledgement_message = CirRoMessage(
            ADUtype=AcknowledgeADUEnums.ACKNOWLEDGE_COMMAND.value, DataUnit=acknowledge_data_unit
        )

    return acknowledgement_message


def generate_message_state_acknowledge(
    data_unit: Union[CyclicMeasure, SpontaneousMeasure, StateAlarm],
):
    acknowledge_data_unit = AcknowledgeMeasureState(UUID=data_unit.UUID, Timetag=int(time.time()), Value=True)
    acknowledge_message = CirRoMessage(
        ADUtype=AcknowledgeADUEnums.ACKNOWLEDGE_MEASURE.value, DataUnit=acknowledge_data_unit
    )

    return acknowledge_message
