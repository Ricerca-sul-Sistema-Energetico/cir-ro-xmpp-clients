from data_models.cir_ro_message import CirRoMessage, CyclicMeasure, SpontaneousMeasure, StateAlarm
from enums.project_enums import MessageADUEnums
from fastapi import HTTPException, APIRouter
from factory_clients import xmpp_client
from read_config import Logger
from slixmpp.jid import JID
import asyncio
import threading

router = APIRouter(
    prefix="",
    tags=["Send Measures"],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Not Found"},
        500: {"description": "XMPP client error"},
    },
)
send_event = threading.Event()


@router.post("/send_cyclic_measure")
async def send_cyclic_measure(node: str, domain: str, data_unit: CyclicMeasure):
    try:
        message = CirRoMessage(ADUtype=MessageADUEnums.CYCLIC_MEASURE.value, DataUnit=data_unit)
        message_body = message.json()
        Logger.info(f"Client ready to send to {node}@{domain} message: {message_body}")
        destination = node + "@" + domain
        destination = JID(jid=destination)
        xmpp_client.send_message(mto=destination, mbody=message_body)
        return True
    except Exception as e:
        Logger.error(f"Failed sending Cyclic measure: {e}")


@router.post("/send_spontaneous_measure")
async def send_spontaneous_measure(node: str, domain: str, data_unit: SpontaneousMeasure):
    try:
        message = CirRoMessage(ADUtype=MessageADUEnums.SPONT_MEASURE.value, DataUnit=data_unit)
        message_body = message.json()
        Logger.info(f"Client ready to send to {node}@{domain} message: {message_body}")
        destination = node + "@" + domain
        xmpp_client.send_message(mto=destination, mbody=message_body)
        return True
    except Exception as e:
        Logger.error(f"Failed sending Spontaneous measure: {e}")


@router.post("/send_statealarm_measure")
async def send_statealarm_measure(node: str, domain: str, data_unit: StateAlarm):

    try:
        message = CirRoMessage(ADUtype=MessageADUEnums.STATE_ALARM.value, DataUnit=data_unit)
        message_body = message.json()
        Logger.info(f"Client ready to send to {node}@{domain} message: {message_body}")
        destination = node + "@" + domain
        xmpp_client.send_message(mto=destination, mbody=message_body)
        return True
    except Exception as e:
        Logger.error(f"Failed sending State/Alarm: {e}")
