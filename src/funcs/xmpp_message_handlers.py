from read_config import Logger, cfg
import json
from slixmpp import ClientXMPP

from funcs.acknowledgement import generate_command_acknowledge, generate_message_state_acknowledge
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


def CIR_message_handler(client: ClientXMPP, msg):
    """
    Handler function used by CIR-type client.
    Based on message type recieved from the RO responds with
    Acknowledge Command or simply gets the Acknowledge Message
    """
    sender = msg["from"]
    message_content = msg["body"]
    message_type = msg["type"]
    Logger.info(f"Arrived message type {message_type} from {sender}. \n Content: {message_content}")
    message_dict: dict = json.loads(message_content)
    message_istance = CirRoMessage(**message_dict)

    if message_istance is None:
        Logger.error(f"No message was parsed from message {message_content}")
        raise ValueError("No message was parsed}")
    message_type = message_istance.ADUtype
    data_unit = message_istance.DataUnit
    if isinstance(
        data_unit,
        (
            CommandLimitPowerDuration,
            CommandLimitPowerUntil,
            CommandSuspendDuration,
            CommandSuspendUntil,
        ),
    ):
        acknowledgement = generate_command_acknowledge(data_unit=data_unit)
        response = acknowledgement.json()
        Logger.info(f"Sending command acknoledgement {response}")
        client.send_message(mto=sender, mbody=response)
    elif isinstance(data_unit, AcknowledgeMeasureState):
        Logger.info(f"Recieved acknowledgement to message {data_unit.UUID}")
    else:
        Logger.error(
            f"CIR {cfg.node} succesfully parsed incoming message but associeted data_unit is not coherent. Please notify library authors."
        )


def RO_message_handler(client: ClientXMPP, msg):
    """
    Handler function used by RO-type client.
    Based on message type recieved from the CIR responds with
    Acknowledge Command or simply gets the Acknowledge Message
    """
    sender = msg["from"]
    message_content = msg["body"]
    message_type = msg["type"]
    Logger.info(f"Arrived message type {message_type} from {sender}. \n Content: {message_content}")
    message_dict: dict = json.loads(message_content)
    message_istance = CirRoMessage(**message_dict)

    if message_istance is None:
        Logger.error(f"No message was parsed from message {message_content}")
        raise ValueError("No message was parsed}")
    message_type = message_istance.ADUtype
    data_unit = message_istance.DataUnit
    if isinstance(
        data_unit,
        (CyclicMeasure, SpontaneousMeasure, StateAlarm),
    ):
        acknowledgement = generate_message_state_acknowledge(data_unit=data_unit)
        response = acknowledgement.json()
        Logger.info(f"Sending command acknoledgement {response}")
        client.send_message(mto=sender, mbody=response)

    elif isinstance(data_unit, AcknowledgeCommand):
        Logger.info(f"Recieved acknowledgement to message {data_unit.UUID}")
    else:
        Logger.error(
            f"Remote Operator {client.jid} succesfully parsed incoming message but associeted data_unit is not coherent. \
                    Please notify library authors."
        )


def presence_handler(client: ClientXMPP, msg):
    """
    Handler which automatically authorizes subscription requests
    from authorized jids.
    """
    sender = msg["from"]
    presence_type = msg["type"]
    if presence_type == "subscribe":
        client.send_presence(pto=sender, ptype=presence_type)
