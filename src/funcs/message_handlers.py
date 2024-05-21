import xmpp
from typing import List
from read_config import Logger, cfg
import json
import uuid
import time
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
from enums.project_enums import AcknowledgeADUEnums, CommandsADUEnums, MessageADUEnums


def CIR_message_handler(client, stanza):
    """
    Handler function used by CIR-type client.
    Based on message type recieved from the RO responds with
    Acknowledge Command or simply gets the Acknowledge Message
    """
    sender = stanza.getFrom()
    message_type = stanza.getType()
    message_content = stanza.getBody()
    Logger.info(f"Arrived message type {message_type} from {sender}. \n Content: {message_content}")
    message_dict: dict = json.loads(message_content)

    try:
        message_istance = CirRoMessage(**message_dict)
        adu_type = message_istance.ADUtype
        data_unit = message_istance.DataUnit

        # MESSAGE IS CORRECT
        if isinstance(data_unit, AcknowledgeMeasureState):
            Logger.info(f"Recieved acknowledgement to message {data_unit.UUID}")
            return
        elif isinstance(
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
            client.send(xmpp.Message(sender, response, typ=adu_type))

        else:
            Logger.error(
                f"CIR {cfg.node} succesfully parsed incoming message but associeted data_unit is not coherent. Please notify library authors."
            )
            return
    except Exception as e:
        Logger.error(f"Recieved uncorrect message format from {sender}. \n Error while parsing: {e}")
        adu_type = message_dict.get("ADUtype", None)
        data_unit = message_dict.get("DataUnit", None)
        if data_unit is None:
            data_unit = {"UUID": str(uuid.uuid4()), "Timetag": int(time.time())}

        if adu_type == AcknowledgeADUEnums.ACKNOWLEDGE_MEASURE.value:
            # WRONG MEASURE ACKNOWLEDGE DATAUNIT
            Logger.error(f"Recieved wrong DataUnit in acknowledge message {data_unit}")
            return
        elif adu_type in [field.value for field in CommandsADUEnums]:
            # WRONG COMMAND DATAUNIT
            Logger.error(f"Recieved wrong command DataUnit {data_unit}")
            data_unit["Ack"] = False
            data_unit["Cause"] = 3
            response_dict = {"ADUtype": AcknowledgeADUEnums.ACKNOWLEDGE_COMMAND.value, "DataUnit": data_unit}
            response = json.dumps(response_dict)
            Logger.info(f"Sending wrong command acknoledgement {response}")
            client.send(xmpp.Message(sender, response, typ=adu_type))

        else:
            # WRONG ADUTYPE
            Logger.error(f"Recieved wrong ADU key {adu_type}")
            try:
                uuid_string = uuid.UUID(data_unit["UUID"], version=4)
            except ValueError:
                uuid_string = uuid.uuid4()
            data_unit["UUID"] = str(uuid_string)
            data_unit["Timetag"] = int(time.time())
            data_unit["Ack"] = False
            data_unit["Cause"] = 3
            response_dict = {"ADUtype": AcknowledgeADUEnums.ACKNOWLEDGE_COMMAND.value, "DataUnit": data_unit}
            response = json.dumps(response_dict)
            client.send(xmpp.Message(sender, response, typ=adu_type))
            return


def RO_message_handler(client, stanza):
    """
    Handler function used by RO-type client.
    Based on message type recieved from the CIR responds with
    Acknowledge Command or simply gets the Acknowledge Message
    """
    sender = stanza.getFrom()
    message_type = stanza.getType()
    message_content = stanza.getBody()
    Logger.info(f"Arrived message type {message_type} from {sender}. \n Content: {message_content}")
    message_dict: dict = json.loads(message_content)
    try:
        message_istance = CirRoMessage(**message_dict)
        message_type = message_istance.ADUtype
        data_unit = message_istance.DataUnit

        # MESSAGE IS CORRECT
        if isinstance(data_unit, AcknowledgeCommand):
            Logger.info(f"Recieved acknowledgement to message {data_unit.UUID}")
            return
        elif isinstance(
            data_unit,
            (CyclicMeasure, SpontaneousMeasure, StateAlarm),
        ):
            acknowledgement = generate_message_state_acknowledge(data_unit=data_unit)
            response = acknowledgement.json()
            Logger.info(f"Sending command acknoledgement {response}")
            client.send(xmpp.Message(sender, response, typ=message_type))

        else:
            Logger.error(
                f"Remote Operator {client.getName()} succesfully parsed incoming message but associeted data_unit is not coherent. \
                        Please notify library authors."
            )
            return
    except Exception as e:  # TODO Considerare il caso di acknowledge sbagliato
        Logger.error(f"Recieved uncorrect message format from {sender}. \n Error while parsing: {e}")
        adu_type = message_dict.get("ADUtype", None)
        data_unit = message_dict.get("DataUnit", None)

        try:
            uuid_string = uuid.UUID(data_unit["UUID"], version=4)
        except ValueError:
            uuid_string = uuid.uuid4()
        data_unit_response = {"UUID": str(uuid_string), "Timetag": int(time.time()), "Value": False}

        if adu_type == AcknowledgeADUEnums.ACKNOWLEDGE_COMMAND.value:
            # WRONG COMMAND ACKNOWLEDGE DATAUNIT
            Logger.error(f"Recieved wrong acknowledge command DataUnit {data_unit}")
            return
        elif adu_type in [field.value for field in MessageADUEnums]:
            # WRONG MESSAGE DATAUNIT
            Logger.error(f"Recieved wrong CIR message DataUnit {data_unit}")
            response_dict = {"ADUtype": AcknowledgeADUEnums.ACKNOWLEDGE_MEASURE.value, "DataUnit": data_unit_response}
            response = json.dumps(response_dict)
            client.send(xmpp.Message(sender, response, typ=adu_type))
        else:
            # WRONG ADUTYPE
            Logger.error(f"Recieved wrong ADU key {adu_type}")
            try:  # TODO: cancel this try-except
                uuid_string = uuid.UUID(data_unit["UUID"], version=4)
            except ValueError:
                uuid_string = uuid.uuid4()

            response_dict = {"ADUtype": AcknowledgeADUEnums.ACKNOWLEDGE_MEASURE.value, "DataUnit": data_unit_response}
            response = json.dumps(response_dict)
            client.send(xmpp.Message(sender, response, typ=adu_type))
            return


def handle_presences(jids: List[str]):
    """
    Returns a stanza handler function which automatically authorizes
    incoming presence requests from the provided jids.
    """

    def handler(client, stanza):
        """
        Handler which automatically authorizes subscription requests
        from authorized jids.
        """
        sender = stanza.getFrom()
        presence_type = stanza.getType()
        if presence_type == "subscribe":
            if any([sender.bareMatch(x) for x in jids]):
                client.send(xmpp.Presence(to=sender, typ="subscribed"))

    return handler
