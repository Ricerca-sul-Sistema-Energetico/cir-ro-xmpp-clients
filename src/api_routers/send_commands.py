from fastapi import APIRouter
from data_models.cir_ro_message import (
    CirRoMessage,
    CommandLimitPowerDuration,
    CommandLimitPowerUntil,
    CommandSuspendDuration,
    CommandSuspendUntil,
)
from enums.project_enums import CommandsADUEnums
from read_config import Logger
from factory_clients import xmpp_client


router = APIRouter(
    prefix="",
    tags=["Send Commands"],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Not Found"},
        500: {"description": "XMPP client error"},
    },
)


@router.post("/send_limit_pwr_duration")
async def send_limit_pwr_duration(node: str, domain: str, data_unit: CommandLimitPowerDuration):

    message = CirRoMessage(ADUtype=CommandsADUEnums.PWR_MAX_CSI_DURATION.value, DataUnit=data_unit)
    message_body = message.json()
    Logger.info(f"Client ready to send to {node}@{domain} command: {message_body}")
    sent_attempt = await xmpp_client.send_message(node=node, domain=domain, message_type="message", body=message_body)
    return sent_attempt


@router.post("/send_limit_pwr_until")
async def send_limit_pwr_until(node: str, domain: str, data_unit: CommandLimitPowerUntil):

    message = CirRoMessage(ADUtype=CommandsADUEnums.PWR_MAX_CSI_UNTIL.value, DataUnit=data_unit)
    message_body = message.json()
    Logger.info(f"Client ready to send to {node}@{domain} command: {message_body}")
    sent_attempt = await xmpp_client.send_message(node=node, domain=domain, message_type="message", body=message_body)
    return sent_attempt


@router.post("/send_suspend_duration")
async def send_suspend_duration(node: str, domain: str, data_unit: CommandSuspendDuration):

    message = CirRoMessage(ADUtype=CommandsADUEnums.SUSPEND_DURATION.value, DataUnit=data_unit)
    message_body = message.json()
    Logger.info(f"Client ready to send to {node}@{domain} command: {message_body}")
    sent_attempt = await xmpp_client.send_message(node=node, domain=domain, message_type="message", body=message_body)
    return sent_attempt


@router.post("/send_suspend_until")
async def send_suspend_until(node: str, domain: str, data_unit: CommandSuspendUntil):

    message = CirRoMessage(ADUtype=CommandsADUEnums.SUSPEND_UNTIL.value, DataUnit=data_unit)
    message_body = message.json()
    Logger.info(f"Client ready to send to {node}@{domain} command: {message_body}")
    sent_attempt = await xmpp_client.send_message(node=node, domain=domain, message_type="message", body=message_body)
    return sent_attempt
