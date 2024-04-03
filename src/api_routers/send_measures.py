from data_models.cir_ro_message import CirRoMessage, CyclicMeasure, SpontaneousMeasure, StateAlarm
from enums.project_enums import MessageADUEnums
from fastapi import HTTPException, APIRouter
from factory_clients import xmpp_client
from read_config import Logger


router = APIRouter(
    prefix="",
    tags=["Send Measures"],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Not Found"},
        500: {"description": "XMPP client error"},
    },
)


@router.post("/send_cyclic_measure")
async def send_cyclic_measure(node: str, domain: str, data_unit: CyclicMeasure):

    message = CirRoMessage(ADUtype=MessageADUEnums.CYCLIC_MEASURE.value, DataUnit=data_unit)
    message_body = message.json()
    Logger.info(f"Client ready to send to {node}@{domain} message: {message_body}")
    sent_attempt = await xmpp_client.send_message(node=node, domain=domain, message_type="message", body=message_body)
    return sent_attempt


@router.post("/send_spontaneous_measure")
async def send_spontaneous_measure(node: str, domain: str, data_unit: SpontaneousMeasure):

    message = CirRoMessage(ADUtype=MessageADUEnums.SPONT_MEASURE.value, DataUnit=data_unit)
    message_body = message.json()
    Logger.info(f"Client ready to send to {node}@{domain} message: {message_body}")
    sent_attempt = await xmpp_client.send_message(node=node, domain=domain, message_type="message", body=message_body)
    return sent_attempt


@router.post("/send_statealarm_measure")
async def send_statealarm_measure(node: str, domain: str, data_unit: StateAlarm):

    message = CirRoMessage(ADUtype=MessageADUEnums.STATE_ALARM.value, DataUnit=data_unit)
    message_body = message.json()
    Logger.info(f"Client ready to send to {node}@{domain} message: {message_body}")
    sent_attempt = await xmpp_client.send_message(node=node, domain=domain, message_type="message", body=message_body)
    return sent_attempt
