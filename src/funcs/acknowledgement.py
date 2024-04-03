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


def generate_command_acknowledge(
    data_unit: Union[
        CommandLimitPowerDuration,
        CommandSuspendDuration,
        CommandLimitPowerUntil,
        CommandSuspendUntil,
    ],
):

    if isinstance(data_unit, (CommandLimitPowerDuration, CommandSuspendDuration)):
        command_duration = data_unit.Duration  # type: ignore
    if isinstance(data_unit, (CommandLimitPowerUntil, CommandSuspendUntil)):
        command_duration = round(data_unit.Tmax - data_unit.Timetag)  # type: ignore
    acknowledge_data_unit = AcknowledgeCommand(
        UUID=data_unit.UUID, Timetag=int(time.time()), Duration=command_duration, Ack=True, Cause=1
    )
    acknowledgement_message = CirRoMessage(
        ADUtype=AcknowledgeADUEnums.ACKNOWLEDGE_COMMAND.value, DataUnit=acknowledge_data_unit
    )
    return acknowledgement_message


def generate_message_state_acknowledge(
    data_unit: Union[CyclicMeasure, SpontaneousMeasure, StateAlarm],
):
    acknowledge_data_unit = AcknowledgeMeasureState(UUID=data_unit.UUID, Timetag=int(time.time()))
    acknowledge_message = CirRoMessage(
        ADUtype=AcknowledgeADUEnums.ACKNOWLEDGE_MEASURE.value, DataUnit=acknowledge_data_unit
    )

    return acknowledge_message
